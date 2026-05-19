# 🤖 AI Robot Car

A voice-controlled AI robotic vehicle that understands natural language commands, interprets them using a Large Language Model (LLM), detects objects using YOLOv8, and executes actions on an ESP32 microcontroller.

---

## 🏗️ System Architecture

```
User Voice
    ↓
Audio Listener (sounddevice)
    ↓
Speech-to-Text (AssemblyAI)
    ↓
LLM Interpreter (Groq – LLaMA 3.1 8B)
    ↓
Mission Planner
    ↓
Robot Transport Layer
    ↓
ESP32 (Serial/WiFi)
    ↓
Motors / LED / Actuators
```

**Parallel Vision Pipeline:**
```
ESP32-CAM → MJPEG Stream → PC (YOLOv8) → HTTP POST → Raspberry Pi → Mission Planner
```

---

## 🧩 Hardware Components

| Component | Role |
|---|---|
| ESP32-CAM (AI Thinker) | Camera streaming + motor control |
| Raspberry Pi | AI brain (speech, LLM, planning) |
| PC / Laptop | YOLOv8 object detection node |
| L298N Motor Driver | DC motor control |
| DC Motors (x2) | Robot movement |

---

## 📁 Repository Structure

```
AI-robot-car/
│
├── main.py                    # Main runtime loop (Raspberry Pi)
├── requirements.txt           # Python dependencies
├── .env                       # API keys (DO NOT commit)
├── .gitignore
├── README.md
│
├── src/
│   ├── speech/
│   │   ├── audio_listener.py  # Mic capture
│   │   └── stt_engine.py      # AssemblyAI STT
│   │
│   ├── llm/
│   │   └── llm_interface.py   # Groq LLM command parser
│   │
│   ├── planner/
│   │   └── mission_planner.py # Central decision logic
│   │
│   ├── core/
│   │   ├── world_state.py     # In-memory object detection state
│   │   └── robot_transport.py # Hardware abstraction layer
│   │
│   ├── controllers/
│   │   ├── led_controller.py  # LED control
│   │   └── motor_controller.py# Motor control
│   │
│   ├── hardware/
│   │   └── serial_interface.py# USB serial to ESP32
│   │
│   └── vision/
│       ├── detection_server.py# Flask server receives YOLO detections
│       └── yolo_stream.py     # PC-side YOLO inference script
│
├── firmware/
│   ├── esp32_cam/
│   │   └── esp32_cam.ino      # ESP32-CAM camera stream firmware
│   └── esp32_motor/
│       └── esp32_motor.ino    # ESP32 motor + LED command firmware
│
├── tests/
│   ├── test_audio.py
│   ├── test_stt.py
│   ├── test_llm.py
│   ├── test_serial.py
│   └── test_led_controller.py
│
├── config/
│   └── settings.py            # Centralized config
│
└── docs/
    └── wiring.md              # Hardware wiring guide
```

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/AI-robot-car.git
cd AI-robot-car
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API keys
```bash
cp .env.example .env
# Edit .env and add your keys
```

### 5. Flash ESP32 firmware
- Open `firmware/esp32_cam/esp32_cam.ino` in Arduino IDE
- Set your WiFi SSID and password
- Flash to AI Thinker ESP32-CAM

- Open `firmware/esp32_motor/esp32_motor.ino`
- Flash to your motor-control ESP32

### 6. Run the vision node (on PC)
```bash
python src/vision/yolo_stream.py
```

### 7. Run the main loop (on Raspberry Pi)
```bash
python main.py
```

---

## 🎤 Example Voice Commands

| Voice Input | Robot Action |
|---|---|
| "Turn on the LED" | LED_ON |
| "Turn off the LED" | LED_OFF |
| "Move forward" | MOVE_FORWARD |
| "Turn left" | TURN_LEFT |
| "Stop" | STOP |
| "Follow the person" | Vision-guided tracking loop |
| "Move towards the bottle" | Single-step navigation |

---

## 🧪 Running Tests

Always run from the project root:
```bash
python -m tests.test_audio
python -m tests.test_stt
python -m tests.test_llm
python -m tests.test_serial
python -m tests.test_led_controller
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:
```
ASSEMBLYAI_API_KEY=your_assemblyai_key_here
GROQ_API_KEY=your_groq_key_here
ESP32_SERIAL_PORT=/dev/ttyUSB0
ESP32_STREAM_URL=http://192.168.x.x:81/stream
DETECTION_SERVER_PORT=5050
```

---

## 📡 Detection Message Format (PC → Raspberry Pi)

```json
{
  "timestamp": 1710000000,
  "detections": [
    {
      "object": "person",
      "confidence": 0.82,
      "bbox": [120, 90, 310, 420]
    }
  ]
}
```

---

## 📊 Performance

| Stage | Latency |
|---|---|
| Audio recording | ~4 s |
| AssemblyAI STT | ~1–2 s |
| Groq LLM inference | <1 s |
| ESP32 execution | instant |
| **Total voice pipeline** | **~5–7 s** |

| Vision Stage | Latency |
|---|---|
| ESP32 capture | ~50–80 ms |
| Wi-Fi transfer | ~20–40 ms |
| YOLOv8n inference (CPU) | ~40–120 ms |
| **Vision total** | **~150–250 ms** |

---

## 🔮 Roadmap

- [x] Voice command pipeline
- [x] LLM intent parsing
- [x] Vision detection pipeline
- [x] World state management
- [x] Mission planner
- [ ] Motor control integration
- [ ] Obstacle avoidance
- [ ] Vision-guided navigation loop
- [ ] Raspberry Pi full deployment

---

## 📄 License

MIT License
