import streamlit as st
import json
import requests

def render_primefit_form(primefit_data, pdf_url):
    st.subheader("📋 PrimeFit Wellness Profile Preview")

    with st.form("primefit_form"):
        resident_name = st.text_input("Resident Name", primefit_data.get("resident_name", ""))
        wellness_goals = st.multiselect("Wellness Goals", 
                                        options=["Improve Strength", "Increase Flexibility", "Boost Endurance", "Weight Loss", "Balance", "Mobility", "Other"],
                                        default=primefit_data.get("wellness_goals", []))
        activity_level = st.selectbox("Current Activity Level", 
                                      ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"],
                                      index=["Sedentary", "Lightly Active", "Moderately Active", "Very Active"].index(primefit_data.get("activity_level", "Sedentary")))
        preferred_activities = st.multiselect("Preferred Activities", 
                                              options=["Walking", "Stretching", "Balance Training", "Group Classes", "Strength Training", "Cardio", "Water Aerobics", "Chair Exercises", "Other"],
                                              default=primefit_data.get("preferred_activities", []))
        mobility_limitations = st.text_area("Mobility Limitations", primefit_data.get("mobility_limitations", ""))
        medical_conditions = st.text_area("Medical Conditions", primefit_data.get("medical_conditions", ""))
        activity_time_preference = st.radio("Preferred Activity Time", 
                                            ["Morning", "Afternoon", "Evening", "No Preference"],
                                            index=["Morning", "Afternoon", "Evening", "No Preference"].index(primefit_data.get("activity_time_preference", "No Preference")))
        group_or_individual = st.radio("Prefers Group or Individual Exercise", 
                                       ["Group", "Individual", "Both"],
                                       index=["Group", "Individual", "Both"].index(primefit_data.get("group_or_individual", "Both")))
        injuries_or_surgeries = st.text_area("Injuries or Surgeries", primefit_data.get("injuries_or_surgeries", ""))
        activity_history = st.text_area("Activity History", primefit_data.get("activity_history", ""))
        exercise_barriers = st.text_area("Barriers to Exercise", primefit_data.get("exercise_barriers", ""))

        submitted = st.form_submit_button("✅ Save Changes (not implemented)")
    
    st.markdown("---")

    # Debug JSON
    st.subheader("🛠 Raw Debug JSON")
    debug_json = {
        "resident_name": resident_name,
        "wellness_goals": wellness_goals,
        "activity_level": activity_level,
        "preferred_activities": preferred_activities,
        "mobility_limitations": mobility_limitations,
        "medical_conditions": medical_conditions,
        "activity_time_preference": activity_time_preference,
        "group_or_individual": group_or_individual,
        "injuries_or_surgeries": injuries_or_surgeries,
        "activity_history": activity_history,
        "exercise_barriers": exercise_barriers
    }
    st.code(json.dumps(debug_json, indent=2), language="json")

    # PDF Download
    if pdf_url:
        st.markdown(f"[📥 Download PrimeFit PDF]({pdf_url})", unsafe_allow_html=True)
