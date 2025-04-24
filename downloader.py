import yt_dlp
import os

def download_video(url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "%(title).70s.%(ext)s")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'quiet': False,
        'noplaylist': True,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        },
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info).replace(".webm", ".mp4").replace(".mkv", ".mp4")
            if not os.path.exists(filepath) or os.path.getsize(filepath) < 1000:
                raise Exception("The downloaded file is empty or corrupted.")
            return filepath
    except Exception as e:
        raise Exception(f"❌ Download failed: {e}")
