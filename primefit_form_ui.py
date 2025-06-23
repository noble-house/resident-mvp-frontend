import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def render_primefit_form(data, notes_summary):
    with st.form("primefit_form"):
        col1, col2 = st.columns(2)
        with col1:
            data["resident_name"] = st.text_input("Resident Name", data.get("resident_name", ""))
            data["activity_level"] = st.selectbox("Activity Level", ["Low", "Moderate", "High"], index=["Low", "Moderate", "High"].index(data.get("activity_level", "Moderate")))
            data["mobility_limitations"] = st.text_input("Mobility Limitations", data.get("mobility_limitations", ""))
            data["activity_time_preference"] = st.selectbox("Preferred Activity Time", ["Morning", "Afternoon", "Evening"], index=["Morning", "Afternoon", "Evening"].index(data.get("activity_time_preference", "Morning")))
            data["group_or_individual"] = st.radio("Group or Individual Activities?", ["Group", "Individual"], index=["Group", "Individual"].index(data.get("group_or_individual", "Group")))
        with col2:
            data["medical_conditions"] = st.text_area("Medical Conditions", data.get("medical_conditions", ""))
            data["injuries_or_surgeries"] = st.text_area("Injuries or Surgeries", data.get("injuries_or_surgeries", ""))
            data["activity_history"] = st.text_area("Activity History", data.get("activity_history", ""))
            data["exercise_barriers"] = st.text_area("Barriers to Exercise", data.get("exercise_barriers", ""))

        data["wellness_goals"] = st.multiselect("Wellness Goals", ["Flexibility", "Strength", "Balance", "Cardio", "Endurance"], default=data.get("wellness_goals", []))
        data["preferred_activities"] = st.multiselect("Preferred Activities", ["Walking", "Yoga", "Swimming", "Group Classes", "Strength Training"], default=data.get("preferred_activities", []))

        data["notes"] = st.text_area("🏁 AI Wellness Summary (Auto)", notes_summary or "", height=200)

        st.session_state.primefit_form = data
        st.form_submit_button("💾 Save Changes")

def generate_primefit_pdf_from_form():
    data = st.session_state.get("primefit_form", {})
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "PrimeFit Wellness Interest Profile")
    c.setFont("Helvetica", 11)
    y -= 30

    for key, value in data.items():
        if y < 60:
            c.showPage()
            y = height - 40
        display_val = ", ".join(value) if isinstance(value, list) else value
        c.drawString(40, y, f"{key.replace('_', ' ').capitalize()}: {display_val}")
        y -= 20

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
