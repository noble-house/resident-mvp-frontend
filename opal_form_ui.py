import streamlit as st
import fitz  # PyMuPDF
import os

TEMPLATE_PATH = os.path.join("templates", "OPAL Life Story Brochure.pdf")

# Field positions for inserting into the PDF
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
    "community_roles": (100, 280)
}


def render_opal_form():
    """Render editable form with values stored in session_state['opal_form.*'] keys"""

    # Initialize default empty values if not already set
    for field in FIELD_COORDINATES.keys():
        key = f"opal_form.{field}"
        if key not in st.session_state:
            st.session_state[key] = ""

    st.text_input("Full Name", key="opal_form.name")
    st.text_input("Age", key="opal_form.age")
    st.text_area("Previous Home Location", key="opal_form.previous_location")
    st.text_area("Morning Routine", key="opal_form.morning_routine")
    st.text_area("Evening Routine", key="opal_form.evening_routine")
    st.text_area("Interests", key="opal_form.interests")
    st.text_area("Hobbies & Passions", key="opal_form.hobbies")
    st.text_area("Important Life Events", key="opal_form.life_events")
    st.text_area("Family History", key="opal_form.family_history")
    st.text_area("Community Roles / Contributions", key="opal_form.community_roles")


def generate_opal_pdf_from_form() -> bytes:
    """Generate a filled OPAL Life Story PDF using session state values"""
    if not os.path.exists(TEMPLATE_PATH):
        st.error("❌ OPAL PDF template not found in /templates directory.")
        return None

    doc = fitz.open(TEMPLATE_PATH)
    page = doc[0]

    for field, coords in FIELD_COORDINATES.items():
        value = st.session_state.get(f"opal_form.{field}", "")
        if value:
            page.insert_text(coords, str(value), fontsize=11, fontname="helv", fill=(0, 0, 0))

    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes
