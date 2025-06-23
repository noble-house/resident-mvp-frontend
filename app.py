import streamlit as st
import requests
import json

BACKEND_URL = "https://resident-mvp-backend-production.up.railway.app"

st.set_page_config(page_title="Resident Transcriber MVP", layout="centered")
st.title("🧠 Resident Interview Transcriber")

st.markdown("Upload a recorded interview to generate a resident profile using AI.")

# Step 1: Upload audio file
uploaded_file = st.file_uploader("Upload an audio file (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file, format="audio/mp3")
    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post(f"{BACKEND_URL}/upload-audio", files=files)
            if response.status_code == 200:
                transcript = response.json().get("transcript", "")
                st.session_state["transcript"] = transcript
                st.success("Transcription complete!")
                st.text_area("Transcript:", transcript, height=200)
            else:
                st.error("Transcription failed. Please check file type or try again.")

# Step 2: Generate profile from transcript
if "transcript" in st.session_state:
    if st.button("Generate Resident Profile"):
        with st.spinner("Generating profile from transcript..."):
            payload = {"transcript": st.session_state["transcript"]}
            response = requests.post(f"{BACKEND_URL}/generate-profile", json=payload)
            if response.status_code == 200:
                profile = response.json().get("profile", {})
                st.success("Profile generated!")
                st.json(profile)
            else:
                st.error("Profile generation failed.")
