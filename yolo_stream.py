"""
yolo_stream.py – PC-side vision node.
Reads MJPEG stream from ESP32-CAM, runs YOLOv8n inference,
displays results, and POSTs detections to the Raspberry Pi detection server.

Run with:
    python src/vision/yolo_stream.py

Requirements:
    pip install ultralytics opencv-python numpy requests
"""

import time
import requests
import numpy as np
import cv2
from ultralytics import YOLO

from config.settings import (
    ESP32_STREAM_URL,
    YOLO_CONFIDENCE,
    YOLO_FPS_LIMIT,
    DETECTION_SERVER_PORT,
)

# ── Config ────────────────────────────────────────────────────────────────────
PI_DETECTION_URL = f"http://raspberrypi.local:{DETECTION_SERVER_PORT}/detections"
SEND_TO_PI       = True   # set False to disable network posting

model = YOLO("yolov8n.pt")


# ── MJPEG stream reader ───────────────────────────────────────────────────────

def read_stream(url: str):
    """Generator: yields raw JPEG bytes from an MJPEG stream."""
    stream = requests.get(url, stream=True, timeout=10)
    buf    = b""
    for chunk in stream.iter_content(chunk_size=1024):
        buf  += chunk
        start = buf.find(b"\xff\xd8")
        end   = buf.find(b"\xff\xd9")
        if start != -1 and end != -1 and end > start:
            jpg = buf[start : end + 2]
            buf = buf[end + 2 :]
            yield jpg


# ── Detection posting ─────────────────────────────────────────────────────────

def post_detections(detections: list):
    payload = {"timestamp": time.time(), "detections": detections}
    try:
        requests.post(PI_DETECTION_URL, json=payload, timeout=1)
    except Exception as e:
        print(f"[Vision] POST failed: {e}")


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    print(f"[Vision] Connecting to: {ESP32_STREAM_URL}")
    print("[Vision] Press Q to quit\n")

    last_post = 0.0
    min_interval = 1.0 / YOLO_FPS_LIMIT

    for jpg_bytes in read_stream(ESP32_STREAM_URL):
        np_arr = np.frombuffer(jpg_bytes, dtype=np.uint8)
        frame  = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if frame is None:
            continue

        results    = model(frame, verbose=False)[0]
        detections = []

        for box in results.boxes:
            conf  = float(box.conf[0])
            label = model.names[int(box.cls[0])]

            if conf < YOLO_CONFIDENCE:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            detections.append({
                "object":     label,
                "confidence": round(conf, 2),
                "bbox":       [x1, y1, x2, y2],
            })

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame, f"{label} {conf:.0%}",
                (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (0, 255, 0), 2,
            )

        if detections:
            print(f"[Vision] Detected: {detections}")

        # Rate-limited POST to Raspberry Pi
        now = time.time()
        if SEND_TO_PI and detections and (now - last_post) >= min_interval:
            post_detections(detections)
            last_post = now

        cv2.imshow("ESP32-CAM + YOLOv8", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
