# Meeting Transcriber

Local meeting recorder + transcriber. FastAPI backend, Alpine.js single-page UI.
Records your **microphone** and the **meeting audio** in parallel, mixes them to one
mono WAV, and transcribes with `mlx-whisper`. All output goes to `~/MeetingData`
(outside this repo, so it is never committed).

## Run

```bash
uv run uvicorn server:app --reload --port 8077
```

Open http://localhost:8077

## One-time macOS audio setup

To capture the *other participants'* audio you must route system output into
BlackHole, while still hearing it yourself. Do this once in **Audio MIDI Setup**:

1. If BlackHole doesn't appear in the device list, reload Core Audio:
   `sudo killall coreaudiod` (briefly interrupts all audio).
2. Open **Audio MIDI Setup** → **+** → **Create Multi-Output Device**.
   Check both **BlackHole 2ch** and your **speakers/headphones**.
3. During a meeting, set the system output (and/or the meeting app's speaker) to
   that Multi-Output Device. You hear the meeting *and* it flows into BlackHole.

In the UI:
- **Microphone** = your voice (e.g. MacBook Pro Microphone).
- **Meeting audio** = **BlackHole 2ch**.

Press Start before the meeting, Stop after. Then click Transcribe on the recording.

## Layout

- `server.py` — FastAPI app: device listing, recording/mixing, transcription endpoints.
- `static/index.html` — Alpine.js UI.
- `~/MeetingData/recordings/*.wav`, `~/MeetingData/transcripts/*.txt` — output.
