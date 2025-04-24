from moviepy.editor import VideoFileClip
import os

def crop_and_export_clips(video_path, times, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    clips = []

    for i, start_time in enumerate(times):
        end_time = start_time + 10
        try:
            clip = VideoFileClip(video_path).subclip(start_time, end_time)
            w, h = clip.size
            target_w = int(h * 9 / 16)
            x1 = max(0, int((w - target_w) / 2))
            x2 = x1 + target_w
            vertical_clip = clip.crop(x1=x1, x2=x2)

            output_path = os.path.join(output_dir, f"clip_{i+1}.mp4")
            vertical_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                fps=30,
                threads=4,
                preset="medium",
                verbose=False,
                logger=None
            )
            clips.append(output_path)

        except Exception as e:
            print(f"❌ Failed to export clip {i+1}: {e}")

    return clips


def trim_video(video_path, start_time, end_time, output_path="trimmed_fight.mp4"):
    try:
        clip = VideoFileClip(video_path).subclip(start_time, end_time)
        clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=30,
            threads=4,
            preset="medium",
            verbose=False,
            logger=None
        )
        return output_path
    except Exception as e:
        print(f"❌ Failed to trim video: {e}")
        return video_path  # fallback
