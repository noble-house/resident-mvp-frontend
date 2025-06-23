import streamlit as st
import requests
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import av
import tempfile
import os

BACKEND_URL = "https://resident-mvp-backend-production.up.railway.app"

st.set_page_config(page_title="Resident Interview Transcriber", layout="centered")
st.title("Resident Interview Transcriber")

st.markdown("You can either upload a pre-recorded interview or record one now to generate a structured resident profile.")

# === Option 1: Upload Audio ===
st.subheader("📁 Upload an Audio File")
uploaded_file = st.file_uploader("Upload (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"])

# === Option 2: Record Audio ===
st.subheader("🎙️ Or Record Interview Live")

class AudioProcessor(AudioProcessorBase):
    def __init__(self) -> None:
        self.buffer = b""

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.buffer += frame.to_ndarray().tobytes()
        return frame

ctx = webrtc_streamer(
    key="record_audio",
    mode=WebRtcMode.SENDONLY,
    media_stream_constraints={"audio": True, "video": False},
    audio_processor_factory=AudioProcessor,
)

# === Button: Transcribe ===
if st.button("Transcribe Interview"):
    if uploaded_file:
        st.info("Using uploaded file for transcription...")
        file_data = uploaded_file.read()
        filename = uploaded_file.name
    elif ctx and ctx.state.playing and ctx.audio_processor and ctx.audio_processor.buffer:
        st.info("Using recorded audio...")
        wav_path = os.path.join(tempfile.gettempdir(), "recorded_audio.wav")
        with open(wav_path, "wb") as f:
            f.write(ctx.audio_processor.buffer)
        file_data = open(wav_path, "rb").read()
        filename = "recorded_audio.wav"
    else:
        st.warning("Please upload or record audio before clicking Transcribe.")
        st.stop()

    with st.spinner("Transcribing..."):
        files = {"file": (filename, file_data, "audio/wav")}
        response = requests.post(f"{BACKEND_URL}/upload-audio", files=files)

        if response.status_code == 200:
            transcript = response.json().get("transcript", "")
            st.session_state["transcript"] = transcript
            st.success("Transcription complete!")
            st.text_area("Transcript:", transcript, height=200)
        else:
            st.error("Transcription failed. Try again.")

# === Button: Generate Profile ===
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
