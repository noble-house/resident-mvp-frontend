import streamlit as st
import fitz  # PyMuPDF
import os

TEMPLATE_PATH = os.path.join("templates", "OPAL Life Story Brochure.pdf")

# Field positions (x, y coordinates) in the PDF template
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


def render_opal_form():
    """Render editable OPAL Life Story Form UI using session_state"""
    if "opal_form" not in st.session_state:
        st.session_state.opal_form = {}

    form = st.session_state.opal_form

    form["name"] = st.text_input("Full Name", value=form.get("name", ""))
    form["age"] = st.text_input("Age", value=form.get("age", ""))
    form["previous_location"] = st.text_area("Previous Home Location", value=form.get("previous_location", ""), height=100)
    form["morning_routine"] = st.text_area("Morning Routine", value=form.get("morning_routine", ""), height=100)
    form["evening_routine"] = st.text_area("Evening Routine", value=form.get("evening_routine", ""), height=100)
    form["interests"] = st.text_area("Interests", value=form.get("interests", ""), height=100)
    form["hobbies"] = st.text_area("Hobbies & Passions", value=form.get("hobbies", ""), height=100)
    form["life_events"] = st.text_area("Important Life Events", value=form.get("life_events", ""), height=100)
    form["family_history"] = st.text_area("Family History", value=form.get("family_history", ""), height=100)
    form["community_roles"] = st.text_area("Community Roles / Contributions", value=form.get("community_roles", ""), height=100)

    # Save updated form back to session state
    st.session_state.opal_form = form


def generate_opal_pdf_from_form() -> bytes:
    """Generate a filled OPAL Life Story PDF using current form values"""
    if not os.path.exists(TEMPLATE_PATH):
        st.error("❌ OPAL PDF template not found in /templates directory.")
        return None

    doc = fitz.open(TEMPLATE_PATH)
    page = doc[0]

    form = st.session_state.get("opal_form", {})
    for field, coords in FIELD_COORDINATES.items():
        value = form.get(field, "")
        if value:
            page.insert_text(coords, str(value), fontsize=11, fontname="helv", fill=(0, 0, 0))

    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes
