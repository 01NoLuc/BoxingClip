from moviepy.editor import VideoFileClip
import os

def crop_and_export_clips(video_path, times, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    clips = []

    for i, start_time in enumerate(times):
        end_time = start_time + 10  # Each clip is 10 seconds

        clip = VideoFileClip(video_path).subclip(start_time, end_time)

        # Crop to center square for vertical video format
        width, height = clip.size
        side = min(width, height)
        x_center = width // 2
        y_center = height // 2
        clip = clip.crop(x1=x_center - side//2, y1=y_center - side//2, width=side, height=side)

        # Resize for reels/shorts (9:16 aspect ratio)
        vertical_clip = clip.resize(height=1280).resize(width=720)

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
        clips.append(output_path)

    return clips


def trim_video(video_path, start_time, end_time, output_path="trimmed_fight.mp4"):
    clip = VideoFileClip(video_path).subclip(start_time, end_time)
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4, verbose=False, logger=None)
    return output_path
