from moviepy.editor import VideoFileClip
import os

def crop_and_export_clips(video_path, times, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    clips = []

    for i, start_time in enumerate(times):
        end_time = start_time + 10  # 10-second clips
        try:
            clip = VideoFileClip(video_path).subclip(start_time, end_time)

            output_path = os.path.join(output_dir, f"clip_{i+1}.mp4")
            clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                verbose=False,
                logger=None
            )
            clips.append(output_path)
        except Exception as e:
            print(f"[❌ ERROR] Failed to process clip {i+1}: {e}")

    return clips


def trim_video(video_path, start_time, end_time, output_path="trimmed_fight.mp4"):
    try:
        if start_time >= end_time:
            print("[❌ WARNING] Invalid trim bounds. Using full video instead.")
            return video_path

        clip = VideoFileClip(video_path).subclip(start_time, end_time)
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        return output_path
    except Exception as e:
        print(f"[❌ TRIM ERROR] {e}")
        return video_path
