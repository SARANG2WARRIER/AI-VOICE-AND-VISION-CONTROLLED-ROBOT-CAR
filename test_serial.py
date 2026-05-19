"""Test serial communication with ESP32."""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.hardware.serial_interface import SerialInterface

if __name__ == "__main__":
    ser = SerialInterface()
    ser.connect()
    if ser.is_connected():
        ser.send("LED_ON")
        import time; time.sleep(1)
        ser.send("LED_OFF")
        ser.close()
        print("Serial test: OK")
    else:
        print("Serial not connected – check port in .env")
