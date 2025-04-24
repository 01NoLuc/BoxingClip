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

        if frame_idx % int(fps * 2) == 0:  # Every 2 seconds
            results = model(frame, verbose=False)
            for r in results:
                classes = r.boxes.cls.tolist()
                people = sum(1 for c in classes if c == 0)
                if people >= 2:
                    seconds = frame_idx / fps
                    if start_time is None:
                        print(f"[🟢 START] Detected at {seconds}s")
                        start_time = seconds
                    print(f"[🟢 UPDATE] Detected at {seconds}s")
                    end_time = seconds

        frame_idx += 1

    cap.release()

    if start_time is None or end_time is None:
        print("[❌ ERROR] Could not detect clear fight bounds.")
        return 0, int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps)  # default to full video

    print(f"[✅ BOUNDS] Fight from {start_time}s to {end_time}s")
    return int(start_time), int(end_time)


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
                if any(c in [0, 1] for c in classes):  # person or glove/etc
                    seconds = frame_idx / fps
                    highlight_times.append(int(seconds))
                    break

        frame_idx += 1

    cap.release()
    return sorted(set(highlight_times))
