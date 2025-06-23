import streamlit as st
import io
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

def render_opal_form(opal_data: dict):
    updated_data = {}
    with st.expander("📝 OPAL Life Story Form"):
        for key, value in opal_data.items():
            new_value = st.text_area(key.replace("_", " ").capitalize(), value)
            updated_data[key] = new_value
    return updated_data

def generate_opal_pdf_from_form():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    width, height = LETTER
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "OPAL Life Story")
    c.setFont("Helvetica", 12)
    y -= 30

    for key, value in st.session_state.opal_form.items():
        label = key.replace("_", " ").capitalize()
        text = f"{label}: {value}"
        for line in split_text(text, 80):
            c.drawString(50, y, line)
            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50

    c.save()
    buffer.seek(0)
    return buffer

def split_text(text, max_chars):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
