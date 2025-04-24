from ultralytics import YOLO
from pathlib import Path
import cv2

# Load the model from the same folder as this script
model_path = Path(__file__).resolve().parent / "yolov8n.pt"
model = YOLO(str(model_path))

def detect_fight_bounds(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_idx = 0
    start_time, end_time = None, None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % int(fps * 3) == 0:  # every ~3 seconds
            results = model(frame, verbose=False)
            for r in results:
                people = sum(1 for c in r.boxes.cls.tolist() if c == 0)
                if people >= 2:
                    time_sec = frame_idx / fps
                    start_time = time_sec if start_time is None else start_time
                    end_time = time_sec
        frame_idx += 1

    cap.release()
    return int(start_time or 0), int(end_time or 0)

def detect_highlight_times(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_idx = 0
    highlights = set()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % int(fps * 2) == 0:
            results = model(frame, verbose=False)
            for r in results:
                if any(c in [0, 1] for c in r.boxes.cls.tolist()):
                    highlights.add(int(frame_idx / fps))
                    break
        frame_idx += 1

    cap.release()
    return sorted(highlights)
