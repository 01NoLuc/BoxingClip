from ultralytics import YOLO
import cv2
import os

# Auto-download the YOLOv8n model if it doesn't exist
if not os.path.exists("yolov8n.pt"):
    YOLO("yolov8n")  # this downloads and saves the model

model = YOLO("yolov8n.pt")  # Load once globally


def detect_fight_bounds(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_idx = 0
    start_time, end_time = None, None

    print(f"[DEBUG] FPS: {fps}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % int(fps * 5) == 0:  # Check every ~5 seconds
            print(f"[DEBUG] Checking frame: {frame_idx}")
            results = model(frame, verbose=False)
            for r in results:
                people = sum(1 for c in r.boxes.cls.tolist() if c == 0)
                if people >= 2:
                    time_sec = frame_idx / fps
                    start_time = time_sec if start_time is None else start_time
                    end_time = time_sec
                    print(f"[DEBUG] Fight detected at {time_sec:.2f}s")

        frame_idx += 1

    cap.release()
    if start_time is None or end_time is None or end_time - start_time < 10:
        print("[DEBUG] No valid fight window found.")
        return 0, 10  # fallback to avoid crash

    print(f"[DEBUG] Final fight bounds: Start {start_time:.2f}s → End {end_time:.2f}s")
    return int(start_time), int(end_time)


def detect_highlight_times(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_idx = 0
    highlights = set()

    print(f"[DEBUG] Analyzing for highlights at FPS: {fps}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % int(fps * 3) == 0:  # Every ~3 seconds
            print(f"[DEBUG] Checking highlight frame: {frame_idx}")
            results = model(frame, verbose=False)
            for r in results:
                if any(c in [0, 1] for c in r.boxes.cls.tolist()):  # Detect people/fighting
                    seconds = int(frame_idx / fps)
                    highlights.add(seconds)
                    print(f"[DEBUG] Highlight found at {seconds}s")
                    break

        frame_idx += 1

    cap.release()
    sorted_highlights = sorted(highlights)
    print(f"[DEBUG] Highlight timestamps: {sorted_highlights}")
    return sorted_highlights
