#!/usr/bin/env python3
"""
Copy WAV files to sorting-task/audio/ for the web interface.

Searches for SMPC-01.wav ... SMPC-27.wav in (in order):
  1. ../simuli_set_normalized/
  2. ../simuli_set/
  3. ../reference_set/
  4. Custom path: set SOURCE_DIR below

Run: python copy_audio.py
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
AUDIO_DEST = SCRIPT_DIR / "audio"

# Set to your folder with SMPC-01.wav, SMPC-02.wav, etc. (or None to use defaults)
SOURCE_DIR = None  # e.g. Path(r"X:\path\to\your\audio")

SOURCES = [
    SOURCE_DIR,
    PROJECT_ROOT / "simuli_set_normalized",
    PROJECT_ROOT / "simuli_set",
    PROJECT_ROOT / "reference_set",
]
SOURCES = [s for s in SOURCES if s is not None]

def main():
    AUDIO_DEST.mkdir(exist_ok=True)
    print(f"Copying to {AUDIO_DEST}\n")
    copied = 0
    for i in range(1, 28):
        name = f"SMPC-{i:02d}.wav"
        dst = AUDIO_DEST / name
        for src_dir in SOURCES:
            if not src_dir.exists():
                continue
            src = src_dir / name
            if src.exists():
                import shutil
                shutil.copy2(src, dst)
                print(f"  {name} <- {src_dir.name}/")
                copied += 1
                break
        else:
            print(f"  {name} - NOT FOUND")
    print(f"\nCopied {copied}/27 files to {AUDIO_DEST}")

if __name__ == "__main__":
    main()
