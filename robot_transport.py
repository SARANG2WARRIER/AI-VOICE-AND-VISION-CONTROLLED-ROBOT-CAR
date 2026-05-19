"""
RobotTransport – hardware abstraction layer.
Sends string commands to the ESP32 via serial (USB).
Swap this class out to use WiFi/MQTT/ROS2 without changing other modules.
"""

import time
from src.hardware.serial_interface import SerialInterface


class RobotTransport:

    def __init__(self, serial: SerialInterface = None):
        self._serial = serial  # injected or lazily created

    # ── Public API ────────────────────────────────────────────────────────────

    def connect(self):
        """Open the serial connection."""
        if self._serial:
            self._serial.connect()

    def send(self, command: str):
        """
        Send a command string to the ESP32.
        Examples: "MOVE_FORWARD", "LED_ON", "STOP"
        """
        print(f"[Transport] → {command}")
        if self._serial and self._serial.is_connected():
            self._serial.send(command)
        else:
            # Simulation mode – print only
            print(f"[Transport][SIM] Command: {command}")

    def close(self):
        if self._serial:
            self._serial.close()
