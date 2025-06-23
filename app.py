import streamlit as st
import requests
from opal_form_ui import render_opal_form

BACKEND_URL = "https://resident-mvp-backend-production.up.railway.app"

st.set_page_config(page_title="Resident Interview Transcriber", layout="wide")
st.title("🧓 Resident Interview Transcriber")

tab1, tab2 = st.tabs(["🎙️ Transcription & OPAL Form", "📄 PrimeFit (Coming Soon)"])

with tab1:
    st.subheader("Step 1: Upload & Transcribe Interview")
    uploaded_file = st.file_uploader("Upload Audio (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"])

    if st.button("🎙️ Transcribe Interview"):
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
                    st.success("✅ Transcription complete!")
                    st.text_area("📝 Transcript Preview:", transcript, height=200)
                else:
                    st.error("❌ Transcription failed. Please try a different file.")
        else:
            st.warning("⚠️ Please upload a valid audio file.")

    if "transcript" in st.session_state:
        if st.button("📄 Generate Profile & Load OPAL Form"):
            with st.spinner("Generating structured profile..."):
                payload = {"transcript": st.session_state["transcript"]}
                response = requests.post(f"{BACKEND_URL}/generate-profile", json=payload)

                if response.status_code == 200:
                    profile = response.json().get("profile", {})
                    st.session_state["autofill_profile"] = profile
                    st.success("✅ Profile generated and loaded into OPAL Form below")
                else:
                    st.error("❌ Failed to generate profile.")

    st.divider()
    st.subheader("Step 2: Edit & Review OPAL Life Story Form")
    render_opal_form()

with tab2:
    st.warning("🛠️ PrimeFit Form integration is in progress. Coming soon!")
