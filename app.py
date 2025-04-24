import streamlit as st
from downloader import download_video
from analyzer import detect_highlight_times
from clipper import crop_and_export_clips
import os

st.set_page_config(page_title="Boxing Clip Generator", layout="centered")
st.title("🥊 Boxing Clip Generator")

url = st.text_input("Paste YouTube Video URL below:")

if st.button("Start") and url:
    with st.spinner("📥 Downloading video..."):
        try:
            video_path = download_video(url)
            st.success("✅ Video downloaded!")

            if not os.path.exists(video_path.split('%')[0]):  # simple path check
                st.error("Video file not found. Download may have failed.")
                st.stop()

            st.info("🧠 Analyzing highlights...")
            times = detect_highlight_times(video_path)

            if not times:
                st.warning("⚠️ No highlights detected. Try a different video.")
                st.stop()

            st.info("✂️ Generating highlight clips...")
            clips = crop_and_export_clips(video_path, times)

            if not clips:
                st.warning("⚠️ No clips were successfully generated.")
                st.stop()

            st.success("🚀 All clips ready!")

            for clip_path in clips:
                if os.path.exists(clip_path):
                    st.video(clip_path)
                    with open(clip_path, "rb") as clip_file:
                        st.download_button(
                            label="Download Clip",
                            data=clip_file,
                            file_name=os.path.basename(clip_path),
                            mime="video/mp4"
                        )
                else:
                    st.warning(f"Clip not found: {clip_path}")

        except Exception as e:
            st.error(f"❌ Error occurred during processing: {e}")
            st.stop()

else:
    st.caption("⚠️ Paste a valid YouTube video URL and click Start.")
