import yt_dlp
import os

def download_video(url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "%(title).70s.%(ext)s")

    ydl_opts = {
        'format': 'mp4/bestaudio[ext=m4a]/best',
        'outtmpl': output_path,
        'quiet': False,
        'noplaylist': True,
        'postprocessors': [],
        'merge_output_format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            filepath = filepath.replace(".webm", ".mp4").replace(".mkv", ".mp4")
            if not os.path.exists(filepath) or os.path.getsize(filepath) < 1000:
                raise Exception("The downloaded file is empty or corrupted.")
            return filepath
    except Exception as e:
        raise Exception(f"❌ Download failed: {e}")
