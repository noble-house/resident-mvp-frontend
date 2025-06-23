import streamlit as st

def render_primefit_form(primefit_data, primefit_pdf_url):
    form_data = primefit_data.copy()

    with st.form("primefit_form"):
        form_data["resident_name"] = st.text_input("Resident Name", form_data.get("resident_name", ""))
        form_data["wellness_goals"] = st.multiselect(
            "Wellness Goals",
            ["Improve Mobility", "Reduce Pain", "Stay Independent", "Social Engagement", "Strength & Balance"],
            default=form_data.get("wellness_goals", [])
        )
        form_data["activity_level"] = st.selectbox(
            "Current Activity Level",
            ["Low", "Moderate", "High"],
            index=["Low", "Moderate", "High"].index(form_data.get("activity_level", "Low"))
        )
        form_data["preferred_activities"] = st.multiselect(
            "Preferred Activities",
            ["Yoga", "Walking", "Group Classes", "Resistance Training", "Swimming"],
            default=form_data.get("preferred_activities", [])
        )
        form_data["mobility_limitations"] = st.text_input("Mobility Limitations", form_data.get("mobility_limitations", ""))
        form_data["medical_conditions"] = st.text_input("Medical Conditions", form_data.get("medical_conditions", ""))
        form_data["activity_time_preference"] = st.selectbox(
            "Preferred Time for Activities",
            ["Morning", "Afternoon", "Evening"],
            index=["Morning", "Afternoon", "Evening"].index(form_data.get("activity_time_preference", "Morning"))
        )
        form_data["group_or_individual"] = st.radio(
            "Group or Individual Activities?",
            ["Group", "Individual", "Both"],
            index=["Group", "Individual", "Both"].index(form_data.get("group_or_individual", "Group"))
        )
        form_data["injuries_or_surgeries"] = st.text_area("Past Injuries or Surgeries", form_data.get("injuries_or_surgeries", ""))
        form_data["activity_history"] = st.text_area("Activity History", form_data.get("activity_history", ""))
        form_data["exercise_barriers"] = st.text_area("Barriers to Exercise", form_data.get("exercise_barriers", ""))

        st.form_submit_button("💾 Save")

    # Debug JSON
    st.markdown("### 🧾 Raw PrimeFit JSON")
    st.json(form_data)

    if primefit_pdf_url:
        st.markdown(f"📄 [Download PrimeFit Wellness PDF]({primefit_pdf_url})")
