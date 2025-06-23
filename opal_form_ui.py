import streamlit as st
from PIL import Image
import os

def render_opal_form():
    # Load background images for 7 pages
    pages = []
    for i in range(1, 8):
        img_path = f"opal_page_{i}.png"
        if os.path.exists(img_path):
            pages.append(Image.open(img_path))

    # Initialize session state for OPAL form
    if "opal_form" not in st.session_state:
        profile = st.session_state.get("autofill_profile", {})
        st.session_state.opal_form = {
            "name": profile.get("name", ""),
            "age": profile.get("age", ""),
            "previous_location": profile.get("previous_location", ""),
            "morning_routine": profile.get("morning_routine", ""),
            "evening_routine": profile.get("evening_routine", ""),
            "interests": ", ".join(profile.get("interests", []) if profile.get("interests") else []),
            "hobbies": profile.get("hobbies", ""),
            "life_events": profile.get("life_events", ""),
            "family_history": profile.get("family_history", ""),
            "community_roles": profile.get("community_roles", "")
        }

    # Page-wise layout and input overlays
    for i, page_img in enumerate(pages):
        st.markdown(f"### Page {i+1}")
        col1, col2 = st.columns([2, 3])
        with col1:
            st.image(page_img, use_column_width=True)
        with col2:
            with st.container():
                if i == 0:
                    st.session_state.opal_form["name"] = st.text_input("Resident Full Name", st.session_state.opal_form["name"])
                    st.session_state.opal_form["age"] = st.text_input("Age", st.session_state.opal_form["age"])
                    st.session_state.opal_form["previous_location"] = st.text_area("Previous Home Location", st.session_state.opal_form["previous_location"])
                elif i == 1:
                    st.session_state.opal_form["morning_routine"] = st.text_area("Morning Routine", st.session_state.opal_form["morning_routine"])
                elif i == 2:
                    st.session_state.opal_form["evening_routine"] = st.text_area("Evening Routine", st.session_state.opal_form["evening_routine"])
                elif i == 3:
                    st.session_state.opal_form["interests"] = st.text_area("Personal Interests", st.session_state.opal_form["interests"])
                elif i == 4:
                    st.session_state.opal_form["hobbies"] = st.text_area("Hobbies & Passions", st.session_state.opal_form["hobbies"])
                elif i == 5:
                    st.session_state.opal_form["life_events"] = st.text_area("Important Life Events", st.session_state.opal_form["life_events"])
                elif i == 6:
                    st.session_state.opal_form["family_history"] = st.text_area("Family Background", st.session_state.opal_form["family_history"])
                    st.session_state.opal_form["community_roles"] = st.text_area("Community Roles or Contributions", st.session_state.opal_form["community_roles"])

    st.markdown("---")
    if st.button("✅ Save & Continue to Download"):
        st.success("Form captured. Ready for PDF generation.")
        st.json(st.session_state.opal_form)
