import streamlit as st
import os
from downloader import download_video
from analyzer import detect_highlight_times, detect_fight_bounds
from clipper import crop_and_export_clips, trim_video
import threading
import time

st.set_page_config(page_title="Boxing Clip Generator", layout="centered")
st.title("🥊 Boxing Clip Generator")

url = st.text_input("Paste YouTube Video URL below:")

if st.button("Start") and url:
    with st.status("📥 Downloading video... Please wait", expanded=True) as status:
        progress = st.progress(0)
        percent = 0

        result = {"video_path": None, "error": None}

        def download_wrapper():
            try:
                result["video_path"] = download_video(url)
            except Exception as e:
                result["error"] = str(e)

        thread = threading.Thread(target=download_wrapper)
        thread.start()

        while thread.is_alive():
            percent = min(percent + 1, 99)
            progress.progress(percent / 100.0)
            time.sleep(0.1)

        thread.join()

        if result["error"]:
            status.update(label=f"❌ Error during download: {result['error']}", state="error")
            st.stop()

        video_path = result["video_path"]
        progress.progress(1.0)
        status.update(label="✅ Download complete", state="complete")

    if not os.path.exists(video_path.split('%')[0]):
        st.error("Video file not found. Download may have failed.")
        st.stop()

    st.info("🔪 Trimming to fight only...")
    start, end = detect_fight_bounds(video_path)
    trimmed_video = trim_video(video_path, start, end)

    st.info("🧠 Analyzing highlights...")
    times = detect_highlight_times(trimmed_video)
    st.write("Highlight times detected:", times)

    if not times:
        st.warning("⚠️ No highlights detected. Try a different video.")
        st.stop()

    st.info(f"✂️ Generating {len(times)} highlight clips...")
    clips = crop_and_export_clips(trimmed_video, times)
    st.write("Generated clips:", clips)

    if not clips:
        st.warning("⚠️ No clips were successfully generated.")
        st.stop()

    st.success("🚀 All clips ready!")
    progress = st.progress(0)

    for i, clip_path in enumerate(clips):
        if os.path.exists(clip_path):
            st.video(clip_path)
            with open(clip_path, "rb") as clip_file:
                st.download_button(
                    label=f"⬇️ Download Clip {i+1}",
                    data=clip_file,
                    file_name=os.path.basename(clip_path),
                    mime="video/mp4"
                )
        else:
            st.warning(f"Clip not found: {clip_path}")
        progress.progress((i + 1) / len(clips))

else:
    st.caption("⚠️ Paste a valid YouTube video URL and click Start.")
