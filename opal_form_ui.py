import streamlit as st
from PIL import Image
import os
import fitz  # PyMuPDF
import io

# Load all 7 page background images
pages = []
for i in range(1, 8):
    img_path = f"opal_page_{i}.png"
    if os.path.exists(img_path):
        pages.append(Image.open(img_path))

def render_opal_form():
    if "opal_form" not in st.session_state:
        st.session_state.opal_form = {}

    for i, page_img in enumerate(pages):
        st.markdown(f"### Page {i+1}")
        col1, col2 = st.columns([2, 3])
        with col1:
            st.image(page_img, use_column_width=True)
        with col2:
            if i == 0:
                st.session_state.opal_form["name"] = st.text_input("Resident Full Name", st.session_state.opal_form.get("name", ""))
                st.session_state.opal_form["age"] = st.text_input("Age", st.session_state.opal_form.get("age", ""))
                st.session_state.opal_form["previous_location"] = st.text_area("Previous Home Location", st.session_state.opal_form.get("previous_location", ""))
            elif i == 1:
                st.session_state.opal_form["morning_routine"] = st.text_area("Morning Routine", st.session_state.opal_form.get("morning_routine", ""))
            elif i == 2:
                st.session_state.opal_form["evening_routine"] = st.text_area("Evening Routine", st.session_state.opal_form.get("evening_routine", ""))
            elif i == 3:
                st.session_state.opal_form["interests"] = st.text_area("Personal Interests", st.session_state.opal_form.get("interests", ""))
            elif i == 4:
                st.session_state.opal_form["hobbies"] = st.text_area("Hobbies & Passions", st.session_state.opal_form.get("hobbies", ""))
            elif i == 5:
                st.session_state.opal_form["life_events"] = st.text_area("Important Life Events", st.session_state.opal_form.get("life_events", ""))
            elif i == 6:
                st.session_state.opal_form["family_history"] = st.text_area("Family Background", st.session_state.opal_form.get("family_history", ""))
                st.session_state.opal_form["community_roles"] = st.text_area("Community Roles or Contributions", st.session_state.opal_form.get("community_roles", ""))

def generate_opal_pdf_from_form(profile: dict) -> bytes:
    template_path = "templates/OPAL Life Story Brochure.pdf"
    doc = fitz.open(template_path)
    page = doc[0]

    def insert(page, label, x, y):
        value = profile.get(label, "")
        page.insert_text((x, y), value, fontsize=11, fontname="helv")

    # These positions must be precisely aligned by trial on the template
    insert(page, "name", 100, 100)
    insert(page, "age", 100, 120)
    insert(page, "previous_location", 100, 140)
    insert(page, "morning_routine", 100, 160)
    insert(page, "evening_routine", 100, 180)
    insert(page, "interests", 100, 200)
    insert(page, "hobbies", 100, 220)
    insert(page, "life_events", 100, 240)
    insert(page, "family_history", 100, 260)
    insert(page, "community_roles", 100, 280)

    pdf_bytes = io.BytesIO()
    doc.save(pdf_bytes)
    doc.close()
    pdf_bytes.seek(0)
    return pdf_bytes
