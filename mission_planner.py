"""
MissionPlanner – central robot decision and behaviour module.
Reads LLM command JSON and world_state, dispatches to robot_transport.
"""

import time
import threading

from src.core.world_state import world_state
from config.settings import FRAME_WIDTH


class MissionPlanner:

    def __init__(self, transport):
        self.transport      = transport
        self._running_task  = None   # current background task thread
        self._stop_flag     = threading.Event()

    # ── Public API ────────────────────────────────────────────────────────────

    def plan(self, command: dict):
        """Interpret an LLM command dict and execute the appropriate behaviour."""
        if not command:
            print("[Planner] Empty command – ignoring.")
            return

        action = command.get("action", "").upper()
        target = command.get("target", "")

        print(f"[Planner] Action={action}  Target={target}")

        self.stop_current_task()

        if   action == "LED_ON":       self.transport.send("LED_ON")
        elif action == "LED_OFF":      self.transport.send("LED_OFF")
        elif action == "MOVE_FORWARD": self.transport.send("MOVE_FORWARD")
        elif action == "MOVE_BACKWARD":self.transport.send("MOVE_BACKWARD")
        elif action == "TURN_LEFT":    self.transport.send("TURN_LEFT")
        elif action == "TURN_RIGHT":   self.transport.send("TURN_RIGHT")
        elif action == "STOP":         self.transport.send("STOP")
        elif action == "MOVE_TOWARDS": self._run_bg(self._move_towards_once, target)
        elif action == "FOLLOW":       self._run_bg(self._follow_loop, target)
        else:
            print(f"[Planner] Unknown action: {action}")

    def stop_current_task(self):
        """Cancel any running background behaviour loop."""
        self._stop_flag.set()
        if self._running_task and self._running_task.is_alive():
            self._running_task.join(timeout=2)
        self._stop_flag.clear()

    # ── Navigation behaviours ─────────────────────────────────────────────────

    def move_towards(self, target: str):
        """Single-step navigation towards a detected object."""
        det = world_state.get_object(target)
        if det is None:
            print(f"[Planner] '{target}' not in view.")
            self.transport.send("STOP")
            return

        bbox     = det["bbox"]               # [x1, y1, x2, y2]
        center_x = (bbox[0] + bbox[2]) / 2
        frame_cx = FRAME_WIDTH / 2

        margin = FRAME_WIDTH * 0.15          # 15% tolerance band

        if center_x < frame_cx - margin:
            print(f"[Planner] {target} is LEFT")
            self.transport.send("TURN_LEFT")
        elif center_x > frame_cx + margin:
            print(f"[Planner] {target} is RIGHT")
            self.transport.send("TURN_RIGHT")
        else:
            print(f"[Planner] {target} is AHEAD")
            self.transport.send("MOVE_FORWARD")

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _move_towards_once(self, target: str):
        self.move_towards(target)

    def _follow_loop(self, target: str):
        """Continuously track a target until stop_current_task() is called."""
        last_ts = 0.0
        print(f"[Planner] Starting follow loop for '{target}'")
        while not self._stop_flag.is_set():
            if world_state.last_update != last_ts:
                last_ts = world_state.last_update
                self.move_towards(target)
            time.sleep(0.1)
        self.transport.send("STOP")
        print("[Planner] Follow loop stopped.")

    def _run_bg(self, fn, *args):
        self._running_task = threading.Thread(target=fn, args=args, daemon=True)
        self._running_task.start()
