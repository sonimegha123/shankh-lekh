import streamlit as st
import os
from transcriber import transcribe_audio
import tempfile
import shutil

st.set_page_config(page_title="ShankhLekh: Audio Transcriber & Summarizer", layout="centered")

st.title("🎧 ShankhLekh")
st.markdown("Upload your audio file, and we’ll transcribe + summarize it.")

uploaded_file = st.file_uploader("Upload an M4A or WAV file", type=["m4a", "wav"])

if uploaded_file is not None:
    with st.spinner("Saving and processing audio file..."):

        temp_dir = tempfile.mkdtemp()
        temp_audio_path = os.path.join(temp_dir, uploaded_file.name)

        with open(temp_audio_path, "wb") as f:
            f.write(uploaded_file.read())

    if st.button(" Transcribe and Summarize"):
        with st.spinner("Transcribing... this may take a few minutes depending on audio length."):

            # Use your function from transcriber.py
            transcribe_audio(temp_audio_path)

            full_transcript_path = os.path.join("/Volumes/Elements/shankhLekh/", "full_transcript.txt")

            if os.path.exists(full_transcript_path):
                # with open(full_transcript_path, "r", encoding="utf-8") as f:
                #     transcript = f.read()
                # st.subheader("📜 Full Transcript")
                # st.text_area("Transcript", transcript, height=300)

                st.subheader(" Summary")
                from transcriber import summarize_transcript
                summary = summarize_transcript(full_transcript_path)
                st.write(summary)

                st.download_button("📝 Download Summary", data=summary, file_name="summary.txt")
            else:
                st.error("Transcript not found.")
