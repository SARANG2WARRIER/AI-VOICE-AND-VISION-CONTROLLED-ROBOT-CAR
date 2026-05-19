"""
main.py – AI Robot Car main runtime loop.
Runs on Raspberry Pi.

Pipeline:
    Microphone → STT → LLM → MissionPlanner → ESP32

Usage:
    python main.py
"""

from src.speech.audio_listener import AudioListener
from src.speech.stt_engine     import STTEngine
from src.llm.llm_interface     import LLMInterface
from src.planner.mission_planner import MissionPlanner
from src.hardware.serial_interface import SerialInterface
from src.core.robot_transport  import RobotTransport


def main():
    print("=== AI Robot Car Starting ===\n")

    # ── Initialise modules ────────────────────────────────────────────────────
    serial    = SerialInterface()
    serial.connect()

    transport = RobotTransport(serial)
    listener  = AudioListener()
    stt       = STTEngine()
    llm       = LLMInterface()
    planner   = MissionPlanner(transport)

    print("System ready. Say a command!\n")

    # ── Main loop ─────────────────────────────────────────────────────────────
    try:
        while True:
            # 1. Record voice
            audio = listener.listen()

            # 2. Speech → text
            text = stt.transcribe(audio)
            if not text:
                print("[Main] Nothing heard, listening again...\n")
                continue

            print(f"[Main] Heard: {text}")

            # 3. Text → command JSON
            command = llm.parse(text)
            print(f"[Main] Command: {command}\n")

            # 4. Execute via planner
            planner.plan(command)

    except KeyboardInterrupt:
        print("\n[Main] Shutting down...")
        planner.stop_current_task()
        transport.send("STOP")
        transport.close()
        print("[Main] Done.")


if __name__ == "__main__":
    main()
