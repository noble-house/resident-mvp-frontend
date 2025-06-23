import streamlit as st
import requests

BACKEND_URL = "https://resident-mvp-backend-production.up.railway.app"

st.set_page_config(page_title="Resident Interview Transcriber", layout="centered")
st.title("🧓 Resident Interview Transcriber")

st.markdown("Upload a pre-recorded resident interview to generate a structured profile and auto-filled onboarding PDFs.")

# Step 1: File Upload & Transcription
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
        st.warning("⚠️ Please upload a valid audio file before clicking Transcribe.")

# Step 2: Profile + PDF Generation
if "transcript" in st.session_state:
    if st.button("📄 Generate Resident Profile & PDFs"):
        with st.spinner("Generating profile and PDFs..."):
            payload = {"transcript": st.session_state["transcript"]}
            response = requests.post(f"{BACKEND_URL}/generate-profile", json=payload)

            if response.status_code == 200:
                data = response.json()
                profile = data.get("profile", {})
                opal_pdf = data.get("opal_pdf")
                primefit_pdf = data.get("primefit_pdf")

                st.success("✅ Resident Profile Generated!")
                st.json(profile)

                # Show download links
                st.markdown("### 📥 Download Auto-Filled PDFs:")
                st.markdown(f"👉 [Download OPAL Life Story PDF]({BACKEND_URL}{opal_pdf})", unsafe_allow_html=True)
                st.markdown(f"👉 [Download PrimeFit Wellness Profile PDF]({BACKEND_URL}{primefit_pdf})", unsafe_allow_html=True)
            else:
                st.error("❌ Profile or PDF generation failed.")
