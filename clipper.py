from moviepy.editor import VideoFileClip
import os

def crop_and_export_clips(video_path, times, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    clips = []

    for i, start_time in enumerate(times):
        end_time = start_time + 10  # 10-second clips
        clip = VideoFileClip(video_path).subclip(start_time, end_time)

        output_path = os.path.join(output_dir, f"clip_{i+1}.mp4")
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        clips.append(output_path)

    return clips