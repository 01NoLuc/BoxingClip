import streamlit as st
import os
import time
import threading
from downloader import download_video
from analyzer import detect_highlight_times, detect_fight_bounds
from clipper import crop_and_export_clips, trim_video

st.set_page_config(page_title="Boxing Clip Generator", layout="wide")

# Optional: Custom styling if you have a CSS file
if os.path.exists("luxury_style.css"):
    with open("luxury_style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 class='luxury-title'>🥊 Boxing Clip Generator</h1>", unsafe_allow_html=True)

url = st.text_input("Paste YouTube Video URL below:", placeholder="https://www.youtube.com/watch?v=...")

# Step tracker
total_steps = 5
step = 0
progress_bar = st.progress(0)

def update_progress(status_message):
    global step
    step += 1
    st.write(status_message)
    progress_bar.progress(step / total_steps)

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
            st.image("static/loader.gif", width=250)  # Optional animated placeholder
            time.sleep(0.2)
        thread.join()

        if result["error"]:
            status.update(label=f"❌ Download error: {result['error']}", state="error")
            st.stop()

        video_path = result["video_path"]
        status.update(label="✅ Download complete", state="complete")
        update_progress("✅ Download Complete")

    if not os.path.exists(video_path):
        st.error("Video file not found. Download may have failed.")
        st.stop()

    st.info("🔪 Trimming to fight only...")
    try:
        start, end = detect_fight_bounds(video_path)
        trimmed_video = trim_video(video_path, start, end)
        update_progress("✅ Fight Trimmed")
    except Exception as e:
        st.error(f"❌ Trimming failed: {e}")
        st.stop()

    st.info("🧠 Analyzing highlights...")
    try:
        times = detect_highlight_times(trimmed_video)
        if not times:
            st.warning("⚠️ No highlights detected. Try a different video.")
            st.stop()
        update_progress("✅ Highlights Detected")
    except Exception as e:
        st.error(f"❌ Highlight detection failed: {e}")
        st.stop()

    st.info(f"✂️ Generating {len(times[:6])} highlight clips...")
    try:
        clips = crop_and_export_clips(trimmed_video, times)
        if not clips:
            st.warning("⚠️ No clips were successfully generated.")
            st.stop()
        update_progress("✅ Clips Exported")
    except Exception as e:
        st.error(f"❌ Clip export failed: {e}")
        st.stop()

    st.success("🚀 All clips ready!")
    st.markdown("### 🎞️ Preview Clips")
    for i, clip_path in enumerate(clips):
        st.video(clip_path)
        with st.expander(f"Optional: Download Clip {i+1}"):
            with open(clip_path, "rb") as f:
                st.download_button(
                    label=f"⬇️ Download Clip {i+1}",
                    data=f,
                    file_name=os.path.basename(clip_path),
                    mime="video/mp4"
                )
    update_progress("✅ All Done")

else:
    st.caption("⚠️ Paste a valid YouTube video URL and click Start.")
