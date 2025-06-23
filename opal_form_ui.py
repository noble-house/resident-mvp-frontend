import streamlit as st
import fitz  # PyMuPDF
import os

# Path to OPAL PDF template inside templates/
TEMPLATE_PATH = os.path.join("templates", "OPAL Life Story Brochure.pdf")

# Coordinates mapping: (x, y) positions on PDF for each field
FIELD_COORDINATES = {
    "name": (100, 100),
    "age": (100, 120),
    "previous_location": (100, 140),
    "morning_routine": (100, 160),
    "evening_routine": (100, 180),
    "interests": (100, 200),
    "hobbies": (100, 220),
    "life_events": (100, 240),
    "family_history": (100, 260),
    "community_roles": (100, 280),
}

# Default empty form structure
DEFAULT_FORM = {
    "name": "",
    "age": "",
    "previous_location": "",
    "morning_routine": "",
    "evening_routine": "",
    "interests": "",
    "hobbies": "",
    "life_events": "",
    "family_history": "",
    "community_roles": "",
}

# Renders editable form on Streamlit UI
def render_opal_form(profile_data: dict = None):
    if "opal_form" not in st.session_state:
        st.session_state.opal_form = DEFAULT_FORM.copy()

    if profile_data:
        # If new profile is provided (from transcript), update the form
        for key in DEFAULT_FORM:
            st.session_state.opal_form[key] = profile_data.get(key, "")

    st.subheader("📝 OPAL Life Story Editable Form")

    # Actual editable UI
    st.session_state.opal_form["name"] = st.text_input("Full Name", st.session_state.opal_form["name"])
    st.session_state.opal_form["age"] = st.text_input("Age", st.session_state.opal_form["age"])
    st.session_state.opal_form["previous_location"] = st.text_area("Previous Home Location", st.session_state.opal_form["previous_location"])
    st.session_state.opal_form["morning_routine"] = st.text_area("Morning Routine", st.session_state.opal_form["morning_routine"])
    st.session_state.opal_form["evening_routine"] = st.text_area("Evening Routine", st.session_state.opal_form["evening_routine"])
    st.session_state.opal_form["interests"] = st.text_area("Interests", st.session_state.opal_form["interests"])
    st.session_state.opal_form["hobbies"] = st.text_area("Hobbies & Passions", st.session_state.opal_form["hobbies"])
    st.session_state.opal_form["life_events"] = st.text_area("Important Life Events", st.session_state.opal_form["life_events"])
    st.session_state.opal_form["family_history"] = st.text_area("Family History", st.session_state.opal_form["family_history"])
    st.session_state.opal_form["community_roles"] = st.text_area("Community Roles / Contributions", st.session_state.opal_form["community_roles"])

# Generates filled OPAL PDF and returns as bytes for download
def generate_opal_pdf_from_form(form_data: dict) -> bytes:
    if not os.path.exists(TEMPLATE_PATH):
        st.error("❌ Template not found: OPAL Life Story Brochure.pdf")
        return None

    doc = fitz.open(TEMPLATE_PATH)
    page = doc[0]

    for field, coords in FIELD_COORDINATES.items():
        value = form_data.get(field, "")
        if value:
            page.insert_text(
                coords,
                str(value),
                fontsize=11,
                fontname="helv",
                fill=(0, 0, 0)
            )

    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes
