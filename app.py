import streamlit as st
import requests
from opal_form_ui import render_opal_form, generate_opal_pdf_from_form
from primefit_form_ui import render_primefit_form, generate_primefit_pdf_from_form

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

# === Step 2: Generate Profile ===
if "transcript" in st.session_state:
    if st.button("📄 Generate Profile and Load Forms"):
        with st.spinner("Generating structured profile..."):
            payload = {"transcript": st.session_state["transcript"]}
            response = requests.post(f"{BACKEND_URL}/generate-profile", json=payload)

            if response.status_code == 200:
                result = response.json()
                st.session_state.profile_data = result
                st.success("✅ Profile generated and forms loaded.")
            else:
                st.error("❌ Profile generation failed.")

# === Step 3: Render Forms in Tabs ===
if "profile_data" in st.session_state:
    profile = st.session_state.profile_data.get("profile", {})

    tab1, tab2 = st.tabs(["🧓 OPAL Life Story", "🏃 PrimeFit Wellness"])

    # --- OPAL ---
    with tab1:
        st.header("✍️ Review & Edit OPAL Life Story Form")
        st.subheader("🧪 DEBUG: Raw OPAL JSON")
        st.json(profile.get("OPAL Life Story Fields", {}))

        opal_data = {
            "name": profile.get("full_name", ""),
            "age": profile.get("age_or_dob", ""),
            "birthplace": profile.get("birthplace", ""),
            "previous_residence": profile.get("previous_residence", ""),
            "career": profile.get("career", ""),
            "military_service": profile.get("military_service", {}).get("has_served", False),
            "military_branch": profile.get("military_service", {}).get("branch", ""),
            "military_duration": profile.get("military_service", {}).get("duration", ""),
            "hobbies_interests": profile.get("hobbies_interests", ""),
            "favorites_music": profile.get("favorites", {}).get("music", ""),
            "favorites_movies": profile.get("favorites", {}).get("movies", ""),
            "favorites_books": profile.get("favorites", {}).get("books", ""),
            "achievements": profile.get("achievements", ""),
            "daily_routine": profile.get("daily_routine", ""),
            "religion_beliefs": profile.get("religion_beliefs", ""),
            "important_people": profile.get("important_people", ""),
            "health_conditions": profile.get("health_conditions", ""),
            "mobility_needs": profile.get("mobility_needs", ""),
            "communication": profile.get("communication", ""),
            "likes_dislikes": profile.get("likes_dislikes", ""),
            "notes": profile.get("notes", "")
        }

        st.session_state.opal_form = opal_data
        render_opal_form()

        st.markdown("### 📥 Download OPAL Life Story PDF")
        if st.button("📩 Generate & Download OPAL PDF"):
            with st.spinner("Generating OPAL PDF..."):
                pdf_bytes = generate_opal_pdf_from_form()
                if pdf_bytes:
                    name = opal_data.get("name", "Resident")
                    st.download_button(
                        label="⬇️ Download OPAL Life Story PDF",
                        data=pdf_bytes,
                        file_name=f"{name}_OPAL_Life_Story.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("❌ Failed to generate the OPAL PDF.")

    # --- PrimeFit ---
    with tab2:
        st.header("✍️ Review & Edit PrimeFit Wellness Profile")
        st.subheader("🧪 DEBUG: Raw PrimeFit JSON")
        st.json(profile)

        primefit_data = {
            "resident_name": profile.get("resident_name", profile.get("full_name", "")),
            "wellness_goals": profile.get("wellness_goals", []),
            "activity_level": profile.get("activity_level", ""),
            "preferred_activities": profile.get("preferred_activities", []),
            "mobility_limitations": profile.get("mobility_limitations", ""),
            "medical_conditions": profile.get("medical_conditions", ""),
            "activity_time_preference": profile.get("activity_time_preference", ""),
            "group_or_individual": profile.get("group_or_individual", ""),
            "injuries_or_surgeries": profile.get("injuries_or_surgeries", ""),
            "activity_history": profile.get("activity_history", ""),
            "exercise_barriers": profile.get("exercise_barriers", "")
        }

        st.session_state.primefit_form = primefit_data
        render_primefit_form(primefit_data, profile.get("notes", ""))

        st.markdown("### 📥 Download PrimeFit Wellness PDF")
        if st.button("📩 Generate & Download PrimeFit PDF"):
            with st.spinner("Generating PrimeFit PDF..."):
                pdf_bytes = generate_primefit_pdf_from_form()
                if pdf_bytes:
                    name = primefit_data.get("resident_name", "Resident")
                    st.download_button(
                        label="⬇️ Download PrimeFit Profile PDF",
                        data=pdf_bytes,
                        file_name=f"{name}_PrimeFit_Profile.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("❌ Failed to generate the PrimeFit PDF.")
