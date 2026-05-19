"""
DetectionServer – Flask HTTP server running on Raspberry Pi.
Receives YOLO detection payloads from the PC vision node and
updates world_state so the mission planner can read them.

Run with:
    python -m src.vision.detection_server
"""

from flask import Flask, request, jsonify

from src.core.world_state import world_state
from config.settings import DETECTION_SERVER_PORT

app = Flask(__name__)


@app.route("/detections", methods=["POST"])
def receive_detections():
    """
    Expected payload:
    {
        "timestamp": 1710000000,
        "detections": [
            {"object": "person", "confidence": 0.82, "bbox": [120, 90, 310, 420]}
        ]
    }
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    detections = data.get("detections", [])
    timestamp  = data.get("timestamp")

    world_state.update(detections, timestamp)
    print(f"[DetectionServer] Updated: {detections}")

    return jsonify({"status": "ok", "count": len(detections)}), 200


@app.route("/state", methods=["GET"])
def get_state():
    """Debug endpoint – returns current world state."""
    return jsonify({
        "detections":  world_state.get_objects(),
        "last_update": world_state.last_update,
    })


if __name__ == "__main__":
    print(f"[DetectionServer] Listening on port {DETECTION_SERVER_PORT}")
    app.run(host="0.0.0.0", port=DETECTION_SERVER_PORT)
