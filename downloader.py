import yt_dlp
import os

def download_video(url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path
