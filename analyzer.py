from ultralytics import YOLO
import cv2

def detect_fight_bounds(video_path):
    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    start_time = None
    end_time = None
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Analyze every 6 seconds instead of every 2 for speed
        if frame_idx % int(fps * 6) == 0:
            print(f"Analyzing frame {frame_idx}...")
            results = model(frame, verbose=False)
            for r in results:
                classes = r.boxes.cls.tolist()
                people = sum(1 for c in classes if c == 0)  # Class 0 = person
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

        if frame_idx % int(fps * 2) == 0:
            results = model(frame, verbose=False)
            for r in results:
                classes = r.boxes.cls.tolist()
                if any(c in [0, 1] for c in classes):  # 0: person, 1: boxing glove if trained
                    seconds = frame_idx / fps
                    highlight_times.append(int(seconds))
                    break

        frame_idx += 1

    cap.release()
    return sorted(set(highlight_times))
