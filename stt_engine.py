"""
STTEngine – converts a numpy audio array to text using AssemblyAI.
"""

import io
import wave
import tempfile
import os

import numpy as np
import assemblyai as aai

from config.settings import ASSEMBLYAI_API_KEY, AUDIO_SAMPLE_RATE


class STTEngine:

    def __init__(self):
        aai.settings.api_key = ASSEMBLYAI_API_KEY
        self.transcriber = aai.Transcriber(
            config=aai.TranscriptionConfig(
                speech_model=aai.SpeechModel.universal,
                language_code="en",
            )
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def transcribe(self, audio: np.ndarray) -> str:
        """
        Convert int16 numpy audio array → transcription string.
        Writes a temporary WAV, uploads to AssemblyAI, returns text.
        """
        wav_path = self._write_wav(audio)
        try:
            result = self.transcriber.transcribe(wav_path)
            text   = (result.text or "").strip()
            print(f"Recognized text: {text}")
            return text
        finally:
            os.remove(wav_path)

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _write_wav(audio: np.ndarray, sample_rate: int = AUDIO_SAMPLE_RATE) -> str:
        """Write numpy array to a temp WAV file and return its path."""
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)           # int16 = 2 bytes
            wf.setframerate(sample_rate)
            wf.writeframes(audio.tobytes())
        return tmp.name
