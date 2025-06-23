import streamlit as st
import requests
from opal_form_ui import render_opal_form, generate_opal_pdf_from_form

# === Config ===
BACKEND_URL = "https://resident-mvp-backend-production.up.railway.app"
st.set_page_config(page_title="Resident Interview Transcriber", layout="wide")
st.title("🧓 Resident Interview Transcriber")

st.markdown("""
Upload a pre-recorded resident interview to:
- 🎙️ Transcribe it into readable text  
- 📄 Auto-generate a profile  
- ✍️ Edit the OPAL Life Story Form  
- 📥 Download the filled PDF
""")

# === Step 1: Upload & Transcribe ===
uploaded_file = st.file_uploader("📁 Upload Audio (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"])

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
                st.session_state.transcript = transcript
                st.success("✅ Transcription complete!")
                st.text_area("📝 Transcript Preview:", transcript, height=200)
            else:
                st.error("❌ Transcription failed.")
    else:
        st.warning("⚠️ Please upload a valid audio file.")

# === Step 2: Generate Profile and Load Form ===
if "transcript" in st.session_state:
    if st.button("📄 Generate Profile and Load OPAL Form"):
        with st.spinner("Generating structured profile..."):
            payload = {"transcript": st.session_state["transcript"]}
            response = requests.post(f"{BACKEND_URL}/generate-profile", json=payload)

            if response.status_code == 200:
                result = response.json()
                st.subheader("🧪 DEBUG: Raw Profile JSON")
                st.json(result)

                profile = result.get("profile", {})

                # Save entire form dict to session_state
                st.session_state.opal_form = {
                    "name": profile.get("name", ""),
                    "age": profile.get("age", ""),
                    "previous_location": profile.get("previous_location", ""),
                    "morning_routine": profile.get("morning_routine", ""),
                    "evening_routine": profile.get("evening_routine", ""),
                    "interests": (
                        ", ".join(profile["interests"]) if isinstance(profile.get("interests"), list) else profile.get("interests", "")
                    ),
                    "hobbies": profile.get("hobbies", ""),
                    "life_events": profile.get("life_events", ""),
                    "family_history": profile.get("family_history", ""),
                    "community_roles": profile.get("community_roles", "")
                }

                st.success("✅ Profile generated and loaded into OPAL Form")
            else:
                st.error("❌ Profile generation failed.")

# === Step 3: Editable Form UI ===
st.markdown("---")
st.header("✍️ Review & Edit OPAL Life Story Form")
render_opal_form()

# === Step 4: Generate & Download PDF ===
st.markdown("### 📥 Download Finalized PDF")
if st.button("📩 Generate & Download OPAL Life Story PDF"):
    with st.spinner("Generating your OPAL PDF..."):
        pdf_bytes = generate_opal_pdf_from_form()
        if pdf_bytes:
            name = st.session_state.get("opal_form", {}).get("name", "Resident")
            st.download_button(
                label="⬇️ Download OPAL Life Story PDF",
                data=pdf_bytes,
                file_name=f"{name}_OPAL_Life_Story.pdf",
                mime="application/pdf"
            )
        else:
            st.error("❌ Failed to generate the PDF. Template might be missing.")
