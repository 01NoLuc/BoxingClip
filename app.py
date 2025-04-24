import streamlit as st
from downloader import download_video
from analyzer import detect_highlight_times
from clipper import crop_and_export_clips

st.set_page_config(page_title="Boxing Clip Generator", layout="centered")

st.title("🥊 Boxing Clip Generator")

url = st.text_input("Paste YouTube Video URL below:")

if st.button("Start") and url:
    with st.spinner("📥 Downloading video..."):
        try:
            video_path = download_video(url)
            st.success("✅ Downloaded!")

            st.info("🧠 Analyzing highlights...")
            times = detect_highlight_times(video_path)

            st.info("✂️ Generating highlight clips...")
            clips = crop_and_export_clips(video_path, times)

            st.success("🚀 All clips ready!")

            for clip_path in clips:
                st.video(clip_path)
                with open(clip_path, "rb") as clip_file:
                    st.download_button(
                        label="Download Clip",
                        data=clip_file,
                        file_name=clip_path.split("/")[-1],
                        mime="video/mp4"
                    )
        except Exception as e:
            st.error(f"❌ Error occurred: {e}")
else:
    st.caption("⚠️ Make sure to paste a valid YouTube video link.")
