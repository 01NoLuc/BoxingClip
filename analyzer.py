from ultralytics import YOLO
import cv2

def detect_highlight_times(video_path):
    model = YOLO("yolov8n.pt")  # Load model inside the function

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    highlight_times = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)
        for r in results:
            classes = r.boxes.cls.tolist()
            if any(c in [0, 1] for c in classes):  # Detect person/fight presence
                seconds = frame_idx / fps
                highlight_times.append(seconds)
                break

        frame_idx += 30  # Skip every ~1 second at 30fps for speed

    cap.release()

    return sorted(set(int(t) for t in highlight_times))
