import sys
import mlx_whisper
from pathlib import Path

# External, non-synced storage
DATA_DIR = Path.home() / "MeetingData"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

if len(sys.argv) < 2:
    print("Usage: uv run python transcribe.py <audio_file>")
    sys.exit(1)

audio_path = Path(sys.argv[1]).expanduser().resolve()
if not audio_path.exists():
    print(f"File not found: {audio_path}")
    sys.exit(1)

print(f"Transcribing {audio_path.name}...")
result = mlx_whisper.transcribe(
    str(audio_path),
    path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
)

output_path = TRANSCRIPTS_DIR / f"{audio_path.stem}.txt"
output_path.write_text(result["text"])
print(f"Transcript saved to {output_path}")
print("\n--- Transcript preview ---")
print(result["text"][:500])
