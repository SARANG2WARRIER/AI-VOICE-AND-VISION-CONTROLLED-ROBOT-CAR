"""Test microphone audio capture."""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.speech.audio_listener import AudioListener

if __name__ == "__main__":
    listener = AudioListener()
    audio    = listener.listen()
    print(f"Audio length: {len(audio)} samples")
    print("Audio capture: OK")
