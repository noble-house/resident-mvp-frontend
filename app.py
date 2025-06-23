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
                st.session_state.profile_data = response.json()
                st.success("✅ Profile generated and forms loaded.")
            else:
                st.error("❌ Profile generation failed.")

# === Step 3: Render Forms in Tabs ===
if "profile_data" in st.session_state:
    full_profile = st.session_state.profile_data.get("profile", {})
    opal_data = full_profile.get("OPAL Life Story Fields", {})
    primefit_data = full_profile.get("PrimeFit Wellness Profile Fields", {})

    tab1, tab2 = st.tabs(["🧓 OPAL Life Story", "🏃 PrimeFit Wellness"])

    # --- OPAL ---
    with tab1:
        st.header("✍️ Review & Edit OPAL Life Story Form")
        st.subheader("🧪 DEBUG: Raw OPAL JSON")
        st.json(opal_data)

        opal_form_data = {
            "name": opal_data.get("full_name", ""),
            "age": opal_data.get("age_or_dob", ""),
            "birthplace": opal_data.get("birthplace", ""),
            "previous_residence": opal_data.get("previous_residence", ""),
            "career": opal_data.get("career", ""),
            "military_service": opal_data.get("military_service", {}).get("has_served", False),
            "military_branch": opal_data.get("military_service", {}).get("branch", ""),
            "military_duration": opal_data.get("military_service", {}).get("duration", ""),
            "hobbies_interests": opal_data.get("hobbies_interests", ""),
            "favorites_music": opal_data.get("favorites", {}).get("music", ""),
            "favorites_movies": opal_data.get("favorites", {}).get("movies", ""),
            "favorites_books": opal_data.get("favorites", {}).get("books", ""),
            "achievements": opal_data.get("achievements", ""),
            "daily_routine": opal_data.get("daily_routine", ""),
            "religion_beliefs": opal_data.get("religion_beliefs", ""),
            "important_people": opal_data.get("important_people", ""),
            "health_conditions": opal_data.get("health_conditions", ""),
            "mobility_needs": opal_data.get("mobility_needs", ""),
            "communication": opal_data.get("communication", ""),
            "likes_dislikes": opal_data.get("likes_dislikes", ""),
            "notes": opal_data.get("notes", "")
        }

        updated_opal_form = render_opal_form(opal_form_data)
        st.session_state.opal_form = updated_opal_form

        st.markdown("### 📥 Download OPAL Life Story PDF")
        if st.button("📩 Generate & Download OPAL PDF"):
            with st.spinner("Generating OPAL PDF..."):
                pdf_bytes = generate_opal_pdf_from_form()
                if pdf_bytes:
                    st.download_button(
                        label="⬇️ Download OPAL Life Story PDF",
                        data=pdf_bytes,
                        file_name=f"{st.session_state.opal_form['name']}_OPAL_Life_Story.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("❌ Failed to generate the OPAL PDF.")

    # --- PrimeFit ---
    with tab2:
        st.header("✍️ Review & Edit PrimeFit Wellness Profile")
        st.subheader("🧪 DEBUG: Raw PrimeFit JSON")
        st.json(primefit_data)

        primefit_form_data = {
            "resident_name": primefit_data.get("resident_name", opal_data.get("full_name", "")),
            "wellness_goals": primefit_data.get("wellness_goals", []),
            "activity_level": primefit_data.get("activity_level", ""),
            "preferred_activities": primefit_data.get("preferred_activities", []),
            "mobility_limitations": primefit_data.get("mobility_limitations", ""),
            "medical_conditions": primefit_data.get("medical_conditions", ""),
            "activity_time_preference": primefit_data.get("activity_time_preference", ""),
            "group_or_individual": primefit_data.get("group_or_individual", ""),
            "injuries_or_surgeries": primefit_data.get("injuries_or_surgeries", ""),
            "activity_history": primefit_data.get("activity_history", ""),
            "exercise_barriers": primefit_data.get("exercise_barriers", "")
        }

        updated_primefit_form = render_primefit_form(primefit_form_data, opal_data.get("notes", ""))
        st.session_state.primefit_form = updated_primefit_form

        st.markdown("### 📥 Download PrimeFit Wellness PDF")
        if st.button("📩 Generate & Download PrimeFit PDF"):
            with st.spinner("Generating PrimeFit PDF..."):
                pdf_bytes = generate_primefit_pdf_from_form()
                if pdf_bytes:
                    st.download_button(
                        label="⬇️ Download PrimeFit Profile PDF",
                        data=pdf_bytes,
                        file_name=f"{st.session_state.primefit_form['resident_name']}_PrimeFit_Profile.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("❌ Failed to generate the PrimeFit PDF.")
