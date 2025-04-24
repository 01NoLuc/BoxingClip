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

# Steps
total_steps = 5
step = 0
progress_bar = st.progress(0)
def update_progress(): progress_bar.progress(step / total_steps)

if st.button("Start") and url:
    with st.status("📥 Downloading video... Please wait", expanded=True) as status:
        result = {"video_path": None, "error": None}

        def download_wrapper():
            try:
                result["video_path"] = download_video(url)
            except Exception as e:
                result["error"] = str(e)

        thread = threading.Thread(target=download_wrapper)
        thread.start()
        while thread.is_alive():
            time.sleep(0.1)
        thread.join()

        if result["error"]:
            status.update(label=f"❌ Download error: {result['error']}", state="error")
            st.stop()

        video_path = result["video_path"]
        status.update(label="✅ Download complete", state="complete")
        step += 1
        update_progress()

    if not os.path.exists(video_path.split('%')[0]):
        st.error("⚠️ Video not found. Download may have failed.")
        st.stop()

    st.info("🔪 Trimming to fight only...")
    try:
        start, end = detect_fight_bounds(video_path)
        trimmed_video = trim_video(video_path, start, end)
        step += 1
        update_progress()
    except Exception as e:
        st.error(f"❌ Trimming failed: {e}")
        st.stop()

    st.info("🧠 Detecting highlights...")
    try:
        times = detect_highlight_times(trimmed_video)
        st.write("🕒 Highlight times:", times)
        if not times:
            st.warning("⚠️ No highlights detected.")
            st.stop()
        step += 1
        update_progress()
    except Exception as e:
        st.error(f"❌ Highlight detection failed: {e}")
        st.stop()

    st.info("✂️ Generating highlight clips...")
    try:
        clips = crop_and_export_clips(trimmed_video, times)
        if not clips:
            st.warning("⚠️ No clips created.")
            st.stop()
        step += 1
        update_progress()
    except Exception as e:
        st.error(f"❌ Clip creation failed: {e}")
        st.stop()

    st.success("🚀 Clips ready!")
    for i, clip_path in enumerate(clips):
        if os.path.exists(clip_path):
            st.video(clip_path)
            with open(clip_path, "rb") as f:
                st.download_button(f"⬇️ Download Clip {i+1}", f, file_name=os.path.basename(clip_path), mime="video/mp4")
        else:
            st.warning(f"❌ Missing clip: {clip_path}")
    step += 1
    update_progress()
else:
    st.caption("⚠️ Paste a YouTube URL and click Start.")
