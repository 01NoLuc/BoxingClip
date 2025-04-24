import streamlit as st
import os, time, threading
from downloader import download_video
from analyzer import detect_highlight_times, detect_fight_bounds
from clipper import crop_and_export_clips, trim_video_parallel

# Set up the page with a sleek, luxury design
st.set_page_config(page_title="Boxing Clip Generator", layout="wide")

st.markdown("""
    <style>
    body, .stApp {
        background-color: #000000;
        color: white;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stProgress > div > div > div {
        background-color: white !important;
    }
    .css-1v0mbdj { background-color: #111111; }
    .luxury-title {
        color: white;
        text-align: center;
        font-size: 2.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Add a luxury style header
st.markdown("<h1 class='luxury-title'>🥊 Boxing Clip Generator</h1>", unsafe_allow_html=True)

# Input field for YouTube URL
url = st.text_input("Paste YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=...")

# Progress bar setup
total_steps = 5
step = 0
progress_bar = st.progress(0)

def update_progress(label):
    global step
    step += 1
    st.write(label)
    progress_bar.progress(step / total_steps)

if st.button("Start") and url:
    # Step 1: Download video
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
            time.sleep(0.25)
        thread.join()

        if result["error"]:
            status.update(label=f"❌ Download error: {result['error']}", state="error")
            st.stop()

        video_path = result["video_path"]
        status.update(label="✅ Download complete", state="complete")
        update_progress("Download Complete")

    # Step 2: Trim to fight portion
    st.info("🔪 Trimming fight to remove unnecessary parts...")
    try:
        start, end = detect_fight_bounds(video_path)
        trimmed_video = trim_video_parallel(video_path, start, end)
        update_progress("Fight Trimmed")
    except Exception as e:
        st.error(f"❌ Trimming failed: {e}")
        st.stop()

    # Step 3: Detect highlights
    st.info("🧠 Detecting highlights...")
    try:
        times = detect_highlight_times(trimmed_video)
        if not times:
            st.warning("⚠️ No highlights detected.")
            st.stop()
        update_progress("Highlights Detected")
    except Exception as e:
        st.error(f"❌ Highlight detection failed: {e}")
        st.stop()

    # Step 4: Generate clips from detected highlight times
    st.info(f"✂️ Generating {len(times[:6])} clips...")
    try:
        clips = crop_and_export_clips(trimmed_video, times[:6])  # limit to 6 clips
        if not clips:
            st.warning("⚠️ No clips generated.")
            st.stop()
        update_progress("Clips Exported")
    except Exception as e:
        st.error(f"❌ Clip export failed: {e}")
        st.stop()

    # Step 5: Preview clips and provide download options
    st.success("🚀 All clips ready! Preview below:")
    for i, clip_path in enumerate(clips):
        st.video(clip_path)
        with st.expander(f"⬇️ Download Clip {i+1}"):
            with open(clip_path, "rb") as f:
                st.download_button(
                    label=f"Save Clip {i+1}",
                    data=f,
                    file_name=os.path.basename(clip_path),
                    mime="video/mp4"
                )
    update_progress("Complete")

else:
    st.caption("⚠️ Paste a valid YouTube link and click Start.")
