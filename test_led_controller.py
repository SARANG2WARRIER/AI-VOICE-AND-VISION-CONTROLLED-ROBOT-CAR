"""Test LED controller via serial."""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.hardware.serial_interface import SerialInterface
from src.controllers.led_controller import LEDController
import time

if __name__ == "__main__":
    ser = SerialInterface()
    ser.connect()
    led = LEDController(ser)

    led.execute("LED_ON")
    time.sleep(1)
    led.execute("LED_OFF")
    ser.close()
    print("LED controller test: OK")
