from moviepy.editor import VideoFileClip
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def crop_and_export_clips(video_path, times, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    clips = []

    def export_clip(index, start_time):
        end_time = start_time + 10
        try:
            clip = VideoFileClip(video_path).subclip(start_time, end_time)
            w, h = clip.size
            crop_x = max((w - h) // 2, 0)
            vertical_clip = clip.crop(x1=crop_x, y1=0, x2=w - crop_x, y2=h)

            output_path = os.path.join(output_dir, f"clip_{index+1}.mp4")
            vertical_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                preset="ultrafast",
                threads=2,
                verbose=False,
                logger=None
            )
            return output_path
        except Exception as e:
            print(f"Clip {index+1} failed: {e}")
            return None

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(export_clip, i, t) for i, t in enumerate(times[:6])]
        for future in as_completed(futures):
            result = future.result()
            if result:
                clips.append(result)

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
        print(f"Trimming failed: {e}")
        raise
