"""Test speech-to-text pipeline."""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.speech.audio_listener import AudioListener
from src.speech.stt_engine     import STTEngine

if __name__ == "__main__":
    listener = AudioListener()
    stt      = STTEngine()

    audio = listener.listen()
    text  = stt.transcribe(audio)
    print(f"Transcription: {text}")
