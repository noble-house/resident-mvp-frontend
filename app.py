import streamlit as st
import requests
from opal_form_ui import render_opal_form, generate_opal_pdf_from_form
from primefit_form_ui import render_primefit_form

# === Config ===
BACKEND_URL = "https://resident-mvp-backend-production.up.railway.app"
st.set_page_config(page_title="Resident Interview Transcriber", layout="wide")
st.title("🧓 Resident Interview Transcriber")

st.markdown("""
Upload a pre-recorded resident interview to:
- 🎙️ Transcribe it into readable text  
- 📄 Auto-generate a profile  
- ✍️ Edit the OPAL Life Story and PrimeFit Wellness forms  
- 📥 Download filled PDFs
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

# === Step 2: Generate Profile and Load Forms ===
if "transcript" in st.session_state:
    if st.button("📄 Generate Profile and Load Forms"):
        with st.spinner("Generating structured profile..."):
            payload = {"transcript": st.session_state["transcript"]}
            response = requests.post(f"{BACKEND_URL}/generate-profile", json=payload)

            if response.status_code == 200:
                result = response.json()
                st.session_state.profile_data = result

                st.subheader("🧪 DEBUG: Raw Profile JSON")
                st.json(result)

                opal_raw = result.get("profile", {}).get("OPAL Life Story Fields", {})

                # Safe extraction
                def safe_get(obj, keys, default=""):
                    for key in keys:
                        obj = obj.get(key, {}) if isinstance(obj, dict) else {}
                    return obj if isinstance(obj, str) else default

                st.session_state.opal_form = {
                    "name": opal_raw.get("full_name", ""),
                    "age": opal_raw.get("age_or_dob", ""),
                    "birthplace": opal_raw.get("birthplace", ""),
                    "previous_residence": opal_raw.get("previous_residence", ""),
                    "career": opal_raw.get("career", ""),
                    "military_service": bool(opal_raw.get("military_service")),
                    "military_branch": opal_raw.get("military_service", {}).get("branch", "") if opal_raw.get("military_service") else "",
                    "military_duration": opal_raw.get("military_service", {}).get("duration", "") if opal_raw.get("military_service") else "",
                    "hobbies_interests": opal_raw.get("hobbies_interests", ""),
                    "favorites_music": opal_raw.get("favorites", {}).get("music", "") if opal_raw.get("favorites") else "",
                    "favorites_movies": opal_raw.get("favorites", {}).get("movies", "") if opal_raw.get("favorites") else "",
                    "favorites_books": opal_raw.get("favorites", {}).get("books", "") if opal_raw.get("favorites") else "",
                    "achievements": opal_raw.get("achievements", ""),
                    "daily_routine": opal_raw.get("daily_routine", ""),
                    "religion_beliefs": opal_raw.get("religion_beliefs", ""),
                    "important_people": opal_raw.get("important_people", ""),
                    "health_conditions": opal_raw.get("health_conditions", ""),
                    "mobility_needs": opal_raw.get("mobility_needs", ""),
                    "communication": opal_raw.get("communication", ""),
                    "likes_dislikes": opal_raw.get("likes_dislikes", ""),
                    "notes": opal_raw.get("notes", "")
                }

                primefit_raw = result.get("profile", {}).get("PrimeFit Wellness Fields", {})
                st.session_state.primefit_form = {
                    "resident_name": primefit_raw.get("resident_name", ""),
                    "wellness_goals": primefit_raw.get("wellness_goals", []),
                    "activity_level": primefit_raw.get("activity_level", ""),
                    "preferred_activities": primefit_raw.get("preferred_activities", []),
                    "mobility_limitations": primefit_raw.get("mobility_limitations", ""),
                    "medical_conditions": primefit_raw.get("medical_conditions", ""),
                    "activity_time_preference": primefit_raw.get("activity_time_preference", ""),
                    "group_or_individual": primefit_raw.get("group_or_individual", ""),
                    "injuries_or_surgeries": primefit_raw.get("injuries_or_surgeries", ""),
                    "activity_history": primefit_raw.get("activity_history", ""),
                    "exercise_barriers": primefit_raw.get("exercise_barriers", "")
                }

                st.success("✅ Profile generated and forms loaded.")
            else:
                st.error("❌ Profile generation failed.")

# === Tabbed UI for OPAL and PrimeFit ===
if "opal_form" in st.session_state and "primefit_form" in st.session_state:
    tab1, tab2 = st.tabs(["🧓 OPAL Life Story", "🏃 PrimeFit Wellness"])

    with tab1:
        st.header("✍️ Review & Edit OPAL Life Story Form")
        render_opal_form()

        st.markdown("### 📥 Download OPAL Life Story PDF")
        if st.button("📩 Generate & Download OPAL PDF"):
            with st.spinner("Generating OPAL PDF..."):
                pdf_bytes = generate_opal_pdf_from_form()
                if pdf_bytes:
                    name = st.session_state.opal_form.get("name", "Resident")
                    st.download_button(
                        label="⬇️ Download OPAL Life Story PDF",
                        data=pdf_bytes,
                        file_name=f"{name}_OPAL_Life_Story.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("❌ Failed to generate the OPAL PDF.")

    with tab2:
        st.header("✍️ Review & Edit PrimeFit Wellness Profile")
        render_primefit_form(st.session_state.primefit_form, "")
