"""
LEDController – translates planner LED commands to serial messages.
"""

from src.hardware.serial_interface import SerialInterface


class LEDController:

    def __init__(self, serial: SerialInterface):
        self._serial = serial

    def execute(self, command: str):
        if command == "LED_ON":
            self._serial.send("LED_ON")
        elif command == "LED_OFF":
            self._serial.send("LED_OFF")
        else:
            print(f"[LED] Unknown command: {command}")
