from moviepy.editor import VideoFileClip
import os

def trim_video(video_path, start, end):
    trimmed_path = video_path.replace(".mp4", "_trimmed.mp4")
    clip = VideoFileClip(video_path).subclip(start, end)
    clip.write_videofile(trimmed_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
    return trimmed_path

def crop_and_export_clips(video_path, times, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    clips = []

    for i, start_time in enumerate(times):
        end_time = start_time + 6  # Shorter clips for reels
        clip = VideoFileClip(video_path).subclip(start_time, end_time)
        output_path = os.path.join(output_dir, f"clip_{i+1}.mp4")
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        clips.append(output_path)

    return clips
