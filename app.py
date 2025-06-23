import streamlit as st
import requests
import tempfile
import os

BACKEND_URL = "https://resident-mvp-backend-production.up.railway.app"

st.set_page_config(page_title="Resident Interview Transcriber", layout="centered")
st.title("Resident Interview Transcriber")

st.markdown("Upload a pre-recorded resident interview to generate a structured profile.")

uploaded_file = st.file_uploader("Upload Audio (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"])

if st.button("Transcribe Interview"):
    if uploaded_file:
        st.info("Uploading file for transcription...")
        file_data = uploaded_file.read()
        filename = uploaded_file.name

        with st.spinner("Transcribing..."):
            files = {"file": (filename, file_data, "audio/wav")}
            response = requests.post(f"{BACKEND_URL}/upload-audio", files=files)

            if response.status_code == 200:
                transcript = response.json().get("transcript", "")
                st.session_state["transcript"] = transcript
                st.success("Transcription complete!")
                st.text_area("Transcript:", transcript, height=200)
            else:
                st.error("Transcription failed. Please try a different file.")
    else:
        st.warning("Please upload a valid audio file before clicking Transcribe.")

if "transcript" in st.session_state:
    if st.button("Generate Resident Profile"):
        with st.spinner("Generating profile..."):
            payload = {"transcript": st.session_state["transcript"]}
            response = requests.post(f"{BACKEND_URL}/generate-profile", json=payload)

            if response.status_code == 200:
                profile = response.json().get("profile", {})
                st.success("Resident Profile Generated:")
                st.json(profile)
            else:
                st.error("Profile generation failed.")
