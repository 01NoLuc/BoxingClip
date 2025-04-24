from moviepy.editor import VideoFileClip
import os
from concurrent.futures import ThreadPoolExecutor

def process_clip(i, video_path, start_time, output_dir):
    end_time = start_time + 10
    try:
        clip = VideoFileClip(video_path).subclip(start_time, end_time)
        w, h = clip.size
        crop_x = max((w - h) // 2, 0)
        vertical_clip = clip.crop(x1=crop_x, y1=0, x2=w - crop_x, y2=h)

        output_path = os.path.join(output_dir, f"clip_{i+1}.mp4")
        vertical_clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=4,
            verbose=False,
            logger=None
        )
        return output_path
    except Exception as e:
        print(f"❌ Failed to export clip {i+1}: {e}")
        return None

def crop_and_export_clips(video_path, times, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    times = times[:6]  # Limit to top 6
    results = []

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [
            executor.submit(process_clip, i, video_path, t, output_dir)
            for i, t in enumerate(times)
        ]
        for f in futures:
            result = f.result()
            if result:
                results.append(result)

    return results

def trim_video(video_path, start_time, end_time, output_path="trimmed_fight.mp4"):
    try:
        clip = VideoFileClip(video_path).subclip(start_time, end_time)
        clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=4,
            verbose=False,
            logger=None
        )
        return output_path
    except Exception as e:
        print(f"❌ Trimming failed: {e}")
        return video_path
