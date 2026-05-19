"""
Central configuration for AI Robot Car.
All tuneable parameters live here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ────────────────────────────────────────────────────────────────
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY", "")
GROQ_API_KEY       = os.getenv("GROQ_API_KEY", "")

# ── Audio ────────────────────────────────────────────────────────────────────
AUDIO_SAMPLE_RATE      = 16000
AUDIO_CHANNELS         = 1
AUDIO_DTYPE            = "int16"
AUDIO_SILENCE_THRESHOLD = 0.01   # fraction of max int16
AUDIO_SILENCE_DURATION  = 1.5    # seconds of silence to stop
AUDIO_MAX_DURATION      = 8      # max recording seconds

# ── LLM ─────────────────────────────────────────────────────────────────────
GROQ_MODEL      = "llama-3.1-8b-instant"
GROQ_MAX_TOKENS = 60
GROQ_TEMPERATURE = 0

# ── Hardware / Serial ────────────────────────────────────────────────────────
SERIAL_PORT = os.getenv("ESP32_SERIAL_PORT", "/dev/ttyUSB0")
SERIAL_BAUD = int(os.getenv("ESP32_BAUD_RATE", 115200))

# ── Vision ───────────────────────────────────────────────────────────────────
ESP32_STREAM_URL      = os.getenv("ESP32_STREAM_URL", "http://192.168.1.100:81/stream")
DETECTION_SERVER_PORT = int(os.getenv("DETECTION_SERVER_PORT", 5050))
YOLO_CONFIDENCE       = 0.50
YOLO_FPS_LIMIT        = 1        # detections per second sent to Pi

# ── Frame dimensions (QVGA) ──────────────────────────────────────────────────
FRAME_WIDTH  = 320
FRAME_HEIGHT = 240
