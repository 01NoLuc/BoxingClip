from moviepy.editor import VideoFileClip
import os
from concurrent.futures import ThreadPoolExecutor

# Function to export clips
def crop_and_export_clips_parallel(video_path, times, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    clips = []

    def process_clip(i, start_time):
        end_time = start_time + 10  # limit to 10 seconds
        try:
            clip = VideoFileClip(video_path).subclip(start_time, end_time)
            w, h = clip.size
            crop_x = max((w - h) // 2, 0)  # center crop for vertical
            vertical_clip = clip.crop(x1=crop_x, y1=0, x2=w-crop_x, y2=h)

            output_path = os.path.join(output_dir, f"clip_{i+1}.mp4")
            vertical_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                preset="ultrafast",  # 🔥 speed-up
                threads=4,
                verbose=False,
                logger=None
            )
            clips.append(output_path)
        except Exception as e:
            print(f"Failed to process clip {i+1}: {e}")

    # Process clips using threads for parallel execution
    with ThreadPoolExecutor() as executor:
        for i, start_time in enumerate(times[:6]):  # cap to top 6 clips
            executor.submit(process_clip, i, start_time)

    return clips

# Function to trim video using multiple threads
def trim_video_parallel(video_path, start_time, end_time, output_path="trimmed_fight.mp4"):
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
