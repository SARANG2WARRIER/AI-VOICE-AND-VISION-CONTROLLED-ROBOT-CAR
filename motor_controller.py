"""
MotorController – translates planner movement commands to serial messages.
Expects L298N-style motor driver connected to ESP32.
"""

from src.hardware.serial_interface import SerialInterface

VALID_COMMANDS = {
    "MOVE_FORWARD",
    "MOVE_BACKWARD",
    "TURN_LEFT",
    "TURN_RIGHT",
    "STOP",
}


class MotorController:

    def __init__(self, serial: SerialInterface):
        self._serial = serial

    def execute(self, command: str):
        if command in VALID_COMMANDS:
            self._serial.send(command)
        else:
            print(f"[Motor] Unknown command: {command}")

    def stop(self):
        self._serial.send("STOP")
