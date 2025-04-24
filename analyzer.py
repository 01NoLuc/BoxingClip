from ultralytics import YOLO
import cv2

def detect_fight_bounds(video_path):
    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    start_time, end_time = None, None
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % int(fps * 2) == 0:  # Check every ~2 seconds
            results = model(frame, verbose=False)
            for r in results:
                classes = r.boxes.cls.tolist()
                people = sum(1 for c in classes if c == 0)  # 'person' class
                if people >= 2:
                    seconds = frame_idx / fps
                    if start_time is None:
                        start_time = seconds
                    end_time = seconds

        frame_idx += 1

    cap.release()
    return int(start_time or 0), int(end_time or 0)


def detect_highlight_times(video_path):
    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    highlight_times = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % int(fps * 1.5) == 0:  # Check every ~1.5 seconds
            results = model(frame, verbose=False)
            for r in results:
                classes = r.boxes.cls.tolist()
                # Highlight if we detect a person or any action class
                if any(c in [0, 1] for c in classes):
                    seconds = frame_idx / fps
                    highlight_times.append(int(seconds))
                    break

        frame_idx += 1

    cap.release()
    return sorted(set(highlight_times))

