"""
AudioListener – captures microphone audio using sounddevice.
Stops automatically after silence or max duration.
"""

import numpy as np
import sounddevice as sd

from config.settings import (
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS,
    AUDIO_DTYPE,
    AUDIO_SILENCE_THRESHOLD,
    AUDIO_SILENCE_DURATION,
    AUDIO_MAX_DURATION,
)


class AudioListener:

    def __init__(
        self,
        sample_rate: int = AUDIO_SAMPLE_RATE,
        channels: int = AUDIO_CHANNELS,
        silence_threshold: float = AUDIO_SILENCE_THRESHOLD,
        silence_duration: float = AUDIO_SILENCE_DURATION,
        max_duration: float = AUDIO_MAX_DURATION,
        device: int = None,
    ):
        self.sample_rate       = sample_rate
        self.channels          = channels
        self.silence_threshold = silence_threshold
        self.silence_duration  = silence_duration
        self.max_duration      = max_duration
        self.device            = device  # set to mic device index if needed

    # ── Public API ────────────────────────────────────────────────────────────

    def listen(self) -> np.ndarray:
        """Block until speech is captured. Returns flat int16 numpy array."""
        print("Listening...")

        chunk_size           = 1024
        max_chunks           = int(self.max_duration * self.sample_rate / chunk_size)
        silence_chunks_needed = int(self.silence_duration * self.sample_rate / chunk_size)

        audio_chunks:  list   = []
        speech_detected: bool = False
        silence_count:   int  = 0

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype_str,
            blocksize=chunk_size,
            device=self.device,
        ) as stream:
            for _ in range(max_chunks):
                chunk, _ = stream.read(chunk_size)
                audio_chunks.append(chunk.copy())

                volume = np.abs(chunk).mean() / 32768.0  # normalise to 0‑1

                if volume > self.silence_threshold:
                    speech_detected = True
                    silence_count   = 0
                elif speech_detected:
                    silence_count += 1
                    if silence_count >= silence_chunks_needed:
                        break

        print("Recording complete")
        audio = np.concatenate(audio_chunks, axis=0).flatten()
        print(f"Audio length: {len(audio)} samples")
        return audio

    # ── Helpers ───────────────────────────────────────────────────────────────

    @property
    def dtype_str(self) -> str:
        return AUDIO_DTYPE
