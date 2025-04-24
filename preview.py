import cv2
import os

def get_preview_frames(video_path, output_folder="previews", max_frames=10, frame_interval=100):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []

    for i in range(0, frame_count, frame_interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break
        preview_path = os.path.join(output_folder, f"preview_{i}.jpg")
        cv2.imwrite(preview_path, frame)
        frames.append(preview_path)
        if len(frames) >= max_frames:
            break

    cap.release()
    return frames