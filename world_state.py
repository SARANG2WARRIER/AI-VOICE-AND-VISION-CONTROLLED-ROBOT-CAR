"""
WorldState – in-memory snapshot of the latest vision detections.
Updated by detection_server.py; read by mission_planner.py.
"""

import threading
import time


class WorldState:

    def __init__(self):
        self._lock       = threading.Lock()
        self.detections  = []   # list of dicts: {object, confidence, bbox}
        self.last_update = 0.0  # Unix timestamp of last detection push

    # ── Write ─────────────────────────────────────────────────────────────────

    def update(self, detections: list, timestamp: float = None):
        """Replace current detections with a new snapshot."""
        with self._lock:
            self.detections  = detections
            self.last_update = timestamp or time.time()

    # ── Read ──────────────────────────────────────────────────────────────────

    def get_objects(self) -> list:
        """Return list of all currently detected object dicts."""
        with self._lock:
            return list(self.detections)

    def get_object(self, label: str) -> dict | None:
        """Return the first detection matching label, or None."""
        with self._lock:
            for det in self.detections:
                if det.get("object", "").lower() == label.lower():
                    return dict(det)
        return None

    def is_fresh(self, max_age: float = 3.0) -> bool:
        """Return True if detections were updated within max_age seconds."""
        return (time.time() - self.last_update) < max_age


# Singleton instance shared across all modules
world_state = WorldState()
