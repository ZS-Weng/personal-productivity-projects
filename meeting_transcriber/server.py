import asyncio
import threading
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import soundfile as sf
import sounddevice as sd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# External, non-synced storage (outside the git repo)
DATA_DIR = Path.home() / "MeetingData"
RECORDINGS_DIR = DATA_DIR / "recordings"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 48000
WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"

STATIC_DIR = Path(__file__).parent / "static"


class Recorder:
    """Captures one or two input devices in parallel and mixes them to a mono WAV."""

    def __init__(self):
        self._lock = threading.Lock()
        self._streams: list[sd.InputStream] = []
        self._buffers: list[list[np.ndarray]] = []
        self.recording = False
        self.start_time: float | None = None
        self.name: str | None = None

    def _make_callback(self, slot: int):
        def callback(indata, frames, time_info, status):
            # indata is reused by PortAudio, so copy it
            self._buffers[slot].append(indata.copy())
        return callback

    def start(self, devices: list[int], name: str | None):
        with self._lock:
            if self.recording:
                raise RuntimeError("Already recording")
            self._streams = []
            self._buffers = [[] for _ in devices]
            for slot, dev in enumerate(devices):
                info = sd.query_devices(dev)
                channels = min(2, int(info["max_input_channels"]))
                if channels < 1:
                    raise RuntimeError(f"Device {dev} has no input channels")
                stream = sd.InputStream(
                    device=dev,
                    samplerate=SAMPLE_RATE,
                    channels=channels,
                    dtype="float32",
                    callback=self._make_callback(slot),
                )
                self._streams.append(stream)
            # Start all streams as close together as possible
            for stream in self._streams:
                stream.start()
            self.recording = True
            self.start_time = time.time()
            self.name = name or "meeting"

    def stop(self) -> Path:
        with self._lock:
            if not self.recording:
                raise RuntimeError("Not recording")
            for stream in self._streams:
                stream.stop()
                stream.close()
            buffers = self._buffers
            name = self.name
            self.recording = False
            self.start_time = None
            self._streams = []
            self._buffers = []

        # Downmix each source to mono float32
        mono_tracks = []
        for chunks in buffers:
            if not chunks:
                continue
            data = np.concatenate(chunks, axis=0)
            mono = data.mean(axis=1) if data.ndim > 1 else data
            mono_tracks.append(mono.astype(np.float32))

        if not mono_tracks:
            raise RuntimeError("No audio was captured")

        # Pad to the longest track, then sum
        length = max(len(t) for t in mono_tracks)
        mix = np.zeros(length, dtype=np.float32)
        for t in mono_tracks:
            mix[: len(t)] += t

        # Prevent clipping
        peak = float(np.max(np.abs(mix))) if mix.size else 0.0
        if peak > 1.0:
            mix /= peak

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe = "".join(c if c.isalnum() or c in "-_ " else "_" for c in (name or "meeting")).strip()
        filename = f"{stamp}_{safe}.wav"
        out_path = RECORDINGS_DIR / filename
        sf.write(out_path, mix, SAMPLE_RATE, subtype="PCM_16")
        return out_path

    def status(self) -> dict:
        elapsed = time.time() - self.start_time if self.recording and self.start_time else 0
        return {"recording": self.recording, "elapsed": round(elapsed, 1), "name": self.name}


recorder = Recorder()
app = FastAPI(title="Meeting Transcriber")


class StartRequest(BaseModel):
    mic: int | None = None
    system: int | None = None
    name: str | None = None


class TranscribeRequest(BaseModel):
    filename: str


@app.get("/api/devices")
def list_devices():
    devices = []
    for i, d in enumerate(sd.query_devices()):
        if d["max_input_channels"] > 0:
            devices.append({
                "index": i,
                "name": d["name"],
                "channels": d["max_input_channels"],
                "is_blackhole": "blackhole" in d["name"].lower(),
            })
    return {"devices": devices}


@app.get("/api/status")
def status():
    return recorder.status()


@app.post("/api/start")
def start(req: StartRequest):
    devices = [d for d in (req.mic, req.system) if d is not None]
    if not devices:
        raise HTTPException(400, "Select at least one input device")
    try:
        recorder.start(devices, req.name)
    except Exception as e:
        raise HTTPException(400, str(e))
    return recorder.status()


@app.post("/api/stop")
def stop():
    try:
        path = recorder.stop()
    except Exception as e:
        raise HTTPException(400, str(e))
    return {"filename": path.name}


@app.get("/api/recordings")
def recordings():
    items = []
    for f in sorted(RECORDINGS_DIR.glob("*.wav"), reverse=True):
        transcript = TRANSCRIPTS_DIR / f"{f.stem}.txt"
        items.append({
            "filename": f.name,
            "size_mb": round(f.stat().st_size / 1_000_000, 2),
            "created": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            "has_transcript": transcript.exists(),
        })
    return {"recordings": items}


@app.get("/audio/{filename}")
def audio(filename: str):
    path = (RECORDINGS_DIR / filename).resolve()
    if path.parent != RECORDINGS_DIR.resolve() or not path.exists():
        raise HTTPException(404, "Not found")
    return FileResponse(path, media_type="audio/wav")


def _transcribe(filename: str) -> str:
    import mlx_whisper

    audio_path = (RECORDINGS_DIR / filename).resolve()
    if audio_path.parent != RECORDINGS_DIR.resolve() or not audio_path.exists():
        raise FileNotFoundError(filename)
    result = mlx_whisper.transcribe(str(audio_path), path_or_hf_repo=WHISPER_MODEL)
    text = result["text"].strip()
    (TRANSCRIPTS_DIR / f"{audio_path.stem}.txt").write_text(text)
    return text


@app.post("/api/transcribe")
async def transcribe(req: TranscribeRequest):
    try:
        text = await asyncio.to_thread(_transcribe, req.filename)
    except FileNotFoundError:
        raise HTTPException(404, "Recording not found")
    return {"text": text}


@app.get("/api/transcript/{filename}")
def transcript(filename: str):
    stem = Path(filename).stem
    path = TRANSCRIPTS_DIR / f"{stem}.txt"
    if not path.exists():
        raise HTTPException(404, "No transcript")
    return {"text": path.read_text()}


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
