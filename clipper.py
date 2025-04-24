from moviepy.editor import VideoFileClip
import os
from concurrent.futures import ThreadPoolExecutor

def crop_and_export_clips(video_path, times, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    clips = []

    def process_clip(i, start_time):
        try:
            end_time = start_time + 10
            clip = VideoFileClip(video_path).subclip(start_time, end_time)
            w, h = clip.size
            crop_x = max((w - h) // 2, 0)
            vertical = clip.crop(x1=crop_x, y1=0, x2=w-crop_x, y2=h)

            output_path = os.path.join(output_dir, f"clip_{i+1}.mp4")
            vertical.write_videofile(
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
            print(f"Clip {i+1} failed: {e}")
            return None

    with ThreadPoolExecutor(max_workers=6) as executor:
        results = executor.map(lambda p: process_clip(*p), enumerate(times[:6]))

    for clip_path in results:
        if clip_path:
            clips.append(clip_path)

    return clips

def trim_video_parallel(video_path, start_time, end_time, output_path="trimmed_fight.mp4"):
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
        raise RuntimeError(f"Trim failed: {e}")
