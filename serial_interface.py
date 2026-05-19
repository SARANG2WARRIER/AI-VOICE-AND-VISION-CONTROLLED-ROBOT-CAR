"""
SerialInterface – USB serial communication with ESP32.
"""

import serial
import time

from config.settings import SERIAL_PORT, SERIAL_BAUD


class SerialInterface:

    def __init__(self, port: str = SERIAL_PORT, baud: int = SERIAL_BAUD):
        self.port   = port
        self.baud   = baud
        self._conn  = None

    # ── Public API ────────────────────────────────────────────────────────────

    def connect(self):
        """Open serial port."""
        try:
            self._conn = serial.Serial(self.port, self.baud, timeout=1)
            time.sleep(2)   # wait for ESP32 to reset
            print(f"[Serial] Connected: {self.port} @ {self.baud}")
        except serial.SerialException as e:
            print(f"[Serial] Connection failed: {e}")
            self._conn = None

    def send(self, command: str):
        """Send a newline-terminated command string."""
        if self._conn and self._conn.is_open:
            self._conn.write((command + "\n").encode("utf-8"))
            print(f"[Serial] Sent: {command}")
        else:
            print(f"[Serial] Not connected. Dropped: {command}")

    def is_connected(self) -> bool:
        return self._conn is not None and self._conn.is_open

    def close(self):
        if self._conn and self._conn.is_open:
            self._conn.close()
            print("[Serial] Connection closed.")
