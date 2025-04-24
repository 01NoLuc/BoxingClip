import streamlit as st
import os
from moviepy.editor import VideoFileClip
import random

def show_preview_roulette(video_path, label="🎞 Previewing possible clips..."):
    if not os.path.exists(video_path):
        st.warning("Preview not available.")
        return

    try:
        clip = VideoFileClip(video_path)
        duration = int(clip.duration)

        st.subheader(label)
        num_previews = 3

        for i in range(num_previews):
            start = random.randint(0, max(0, duration - 10))
            preview_clip = clip.subclip(start, start + 5)
            preview_file = f"temp_preview_{i}.mp4"
            preview_clip.write_videofile(preview_file, codec="libx264", audio_codec="aac", verbose=False, logger=None)

            st.video(preview_file)

            # Clean up preview file
            os.remove(preview_file)

        clip.close()

    except Exception as e:
        st.error(f"Preview error: {e}")
