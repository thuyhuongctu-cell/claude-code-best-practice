#!/usr/bin/env python3
"""
Voice Assistant Speaker
=============================================
Plays audio in *your own cloned voice* for the `voice-assistant` agent.

Two modes:
  1. Hook mode (clip playback) — reads Claude Code hook JSON on stdin, maps the
     hook event to a pre-recorded clip in .claude/voice/clips/, and plays it.
     Example (agent frontmatter): python3 speak.py
  2. Dynamic TTS mode (read-aloud) — synthesizes arbitrary text in your voice via
     a TTS provider, then plays it. Activates only when an API key + voice_id are
     configured in voice-config.json (or env). Without them it falls back to
     printing the text, so nothing ever breaks.
     Example: python3 speak.py --say "Tôi đã làm xong rồi."

Design goals (mirrors .claude/hooks/scripts/hooks.py):
  - Cross-platform audio playback (macOS / Linux / Windows).
  - ALWAYS exit 0 so a hook failure never interrupts Claude's work.
  - No third-party Python dependencies (urllib only).
"""

import sys
import json
import argparse
import platform
import subprocess
import tempfile
from pathlib import Path

try:
    import winsound  # Windows-only
except ImportError:
    winsound = None

# Paths: this script lives in .claude/hooks/scripts/
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[2]          # repo root (.claude/hooks/scripts -> repo)
VOICE_DIR = PROJECT_ROOT / ".claude" / "voice"
CLIPS_DIR = VOICE_DIR / "clips"
CONFIG_PATH = VOICE_DIR / "voice-config.json"

# Default: hook event -> clip basename (file lives at clips/<basename>.{wav,mp3})
DEFAULT_EVENT_CLIPS = {
    "Stop": "done",
    "SubagentStop": "subagent_done",
    "Notification": "notification",
    "PermissionRequest": "permission",
    "PostToolUseFailure": "error",
    "SessionStart": "hello",
}


def load_config():
    """Load voice-config.json; return {} on any problem (fail-soft)."""
    try:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"[speak] could not read config: {e}", file=sys.stderr)
    return {}


def get_audio_player():
    """Return the command list for the platform's audio player, or None."""
    system = platform.system()
    if system == "Darwin":
        return ["afplay"]
    if system == "Windows":
        return ["WINDOWS"]
    if system == "Linux":
        for player in (["paplay"], ["aplay"], ["ffplay", "-nodisp", "-autoexit"], ["mpg123", "-q"]):
            try:
                subprocess.run(["which", player[0]], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, check=True)
                return player
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
    return None


def play_file(file_path):
    """Play an audio file cross-platform. Returns True on success."""
    file_path = Path(file_path)
    if not file_path.exists():
        return False
    player = get_audio_player()
    if not player:
        return False
    try:
        if player[0] == "WINDOWS":
            if winsound and file_path.suffix.lower() == ".wav":
                winsound.PlaySound(str(file_path), winsound.SND_FILENAME | winsound.SND_NODEFAULT)
                return True
            # Non-WAV on Windows: best-effort via default app
            subprocess.Popen(["cmd", "/c", "start", "", str(file_path)],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        subprocess.Popen(player + [str(file_path)], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, start_new_session=True)
        return True
    except Exception as e:
        print(f"[speak] playback error: {e}", file=sys.stderr)
        return False


def play_clip(basename):
    """Play clips/<basename>.{wav,mp3}. WAV preferred (paplay can't do mp3)."""
    if not basename or "/" in basename or "\\" in basename or ".." in basename:
        return False
    for ext in (".wav", ".mp3"):
        candidate = CLIPS_DIR / f"{basename}{ext}"
        if candidate.exists():
            return play_file(candidate)
    return False


def synthesize_elevenlabs(text, cfg):
    """Synthesize `text` to an mp3 temp file via ElevenLabs. Return path or None."""
    import os
    import urllib.request

    tts = cfg.get("tts", {})
    api_key = os.environ.get("ELEVENLABS_API_KEY") or tts.get("api_key")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID") or tts.get("voice_id")
    if not api_key or not voice_id or voice_id.startswith("<"):
        return None  # not configured yet -> caller falls back to print

    model_id = tts.get("model_id", "eleven_multilingual_v2")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = json.dumps({"text": text, "model_id": model_id}).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload, method="POST",
        headers={"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            audio = resp.read()
        tmp = tempfile.NamedTemporaryFile(prefix="voice_", suffix=".mp3", delete=False)
        tmp.write(audio)
        tmp.close()
        return tmp.name
    except Exception as e:
        print(f"[speak] TTS request failed: {e}", file=sys.stderr)
        return None


def do_say(text, cfg):
    """Read text aloud in your voice if TTS is configured, else print it."""
    path = synthesize_elevenlabs(text, cfg)
    if path:
        play_file(path)
    else:
        # Fail-soft: scaffolding is wired but no API key/voice_id yet.
        print(text)


def main():
    parser = argparse.ArgumentParser(description="Speak in your cloned voice.")
    parser.add_argument("--say", type=str, default=None,
                        help="Text to read aloud (dynamic TTS mode).")
    parser.add_argument("--event", type=str, default=None,
                        help="Force a specific hook event clip (testing).")
    args = parser.parse_args()
    cfg = load_config()

    # 1) Dynamic read-aloud mode
    if args.say is not None:
        do_say(args.say, cfg)
        sys.exit(0)

    # 2) Determine the hook event (from --event or stdin JSON)
    event_name = args.event
    if not event_name:
        stdin_content = sys.stdin.read().strip() if not sys.stdin.isatty() else ""
        if stdin_content:
            try:
                event_name = json.loads(stdin_content).get("hook_event_name", "")
            except json.JSONDecodeError:
                event_name = ""

    if event_name:
        clip_map = {**DEFAULT_EVENT_CLIPS, **cfg.get("event_clips", {})}
        play_clip(clip_map.get(event_name))

    sys.exit(0)  # never interrupt Claude


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[speak] unexpected error: {e}", file=sys.stderr)
        sys.exit(0)
