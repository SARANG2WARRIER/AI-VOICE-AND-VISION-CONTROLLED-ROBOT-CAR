# Hardware Wiring Guide

## ESP32 Motor Controller → L298N Motor Driver

| L298N Pin | ESP32 GPIO | Function |
|-----------|-----------|----------|
| IN1       | GPIO 26   | Left motor direction A |
| IN2       | GPIO 27   | Left motor direction B |
| IN3       | GPIO 14   | Right motor direction A |
| IN4       | GPIO 12   | Right motor direction B |
| ENA       | GPIO 25   | Left motor PWM speed |
| ENB       | GPIO 13   | Right motor PWM speed |
| GND       | GND       | Common ground |
| 5V        | VIN       | Power (from battery) |

## LED

| Component | ESP32 GPIO |
|-----------|-----------|
| LED +     | GPIO 4 (via 220Ω resistor) |
| LED -     | GND |

## ESP32-CAM

Flashed separately. Uses built-in OV2640 camera module.
No extra wiring needed beyond power (5V / GND).

## Power

- Robot battery (7.4V LiPo) → L298N 12V input
- L298N 5V out → ESP32 VIN
- Raspberry Pi powered separately via USB-C

## Serial Connection (Raspberry Pi → ESP32 Motor)

- USB cable from Raspberry Pi to ESP32 USB port
- Port appears as `/dev/ttyUSB0` or `/dev/ttyACM0`
- Set correct port in `.env`: `ESP32_SERIAL_PORT=/dev/ttyUSB0`
