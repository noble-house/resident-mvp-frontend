import streamlit as st
import fitz  # PyMuPDF
import os
import openai

TEMPLATE_PATH = os.path.join("templates", "OPAL Life Story Brochure.pdf")

# Field positions (coordinates in PDF)
FIELD_COORDINATES = {
    "name": (100, 100),
    "age": (100, 120),
    "birthplace": (100, 140),
    "career": (100, 160),
    "military_branch": (100, 180),
    "hobbies_interests": (100, 200),
    "favorites_music": (100, 220),
    "achievements": (100, 240),
    "daily_routine": (100, 260),
    "important_people": (100, 280),
    "health_conditions": (100, 300),
    "mobility_needs": (100, 320),
    "communication": (100, 340),
    "likes_dislikes": (100, 360),
    "notes": (100, 380)
}


def render_opal_form():
    """Render OPAL form with all available fields"""
    if "opal_form" not in st.session_state:
        st.session_state.opal_form = {}

    form = st.session_state.opal_form

    form["name"] = st.text_input("Full Name", value=form.get("name", ""))
    form["age"] = st.text_input("Age / DOB", value=form.get("age", ""))
    form["birthplace"] = st.text_input("Birthplace", value=form.get("birthplace", ""))
    form["career"] = st.text_input("Career", value=form.get("career", ""))
    form["military_branch"] = st.text_input("Military Service (Branch)", value=form.get("military_branch", ""))
    form["hobbies_interests"] = st.text_area("Hobbies & Interests", value=form.get("hobbies_interests", ""), height=80)
    form["favorites_music"] = st.text_input("Favorite Music", value=form.get("favorites_music", ""))
    form["achievements"] = st.text_area("Major Achievements", value=form.get("achievements", ""), height=80)
    form["daily_routine"] = st.text_area("Daily Routine", value=form.get("daily_routine", ""), height=80)
    form["important_people"] = st.text_area("Important People / Family", value=form.get("important_people", ""), height=80)
    form["health_conditions"] = st.text_area("Health Conditions / Dietary Notes", value=form.get("health_conditions", ""), height=80)
    form["mobility_needs"] = st.text_input("Mobility Needs", value=form.get("mobility_needs", ""))
    form["communication"] = st.text_input("Communication Style / Notes", value=form.get("communication", ""))
    form["likes_dislikes"] = st.text_area("Likes / Dislikes", value=form.get("likes_dislikes", ""), height=80)

    # Generate or allow editing notes
    if not form.get("notes"):
        full_summary_prompt = "Summarize the resident’s life story based on the following information:\n\n"
        for k, v in form.items():
            if k != "notes" and v:
                full_summary_prompt += f"{k.replace('_', ' ').title()}: {v}\n"
        with st.spinner("Generating life story summary..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": full_summary_prompt}]
                )
                summary = response.choices[0].message["content"]
                form["notes"] = summary.strip()
            except Exception as e:
                st.warning(f"Could not generate summary: {e}")
                form["notes"] = ""

    form["notes"] = st.text_area("Life Story Summary (AI-generated, editable)", value=form.get("notes", ""), height=120)

    st.session_state.opal_form = form


def generate_opal_pdf_from_form() -> bytes:
    """Generate OPAL PDF from form"""
    if not os.path.exists(TEMPLATE_PATH):
        st.error("❌ Template not found")
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
