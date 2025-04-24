from moviepy.editor import VideoFileClip
import os

def crop_and_export_clips(video_path, times, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    clips = []

    for i, start_time in enumerate(times[:6]):  # Cap at top 6 highlights
        end_time = start_time + 10  # 10-second clips
        try:
            clip = VideoFileClip(video_path).subclip(start_time, end_time)
            w, h = clip.size
            crop_x = max((w - h) // 2, 0)  # Center crop for vertical format
            vertical_clip = clip.crop(x1=crop_x, y1=0, x2=w-crop_x, y2=h)

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
        except Exception as e:
            print(f"❌ Failed to process clip {i+1}: {e}")

    return clips

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
        raise RuntimeError(f"❌ Trimming failed: {e}")
