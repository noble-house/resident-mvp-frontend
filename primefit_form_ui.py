import streamlit as st
import io
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

def render_primefit_form(primefit_data, notes):
    with st.expander("📝 PrimeFit Wellness Form"):
        for key, value in primefit_data.items():
            if isinstance(value, list):
                new_value = st.text_area(key.replace("_", " ").capitalize(), ", ".join(value))
                primefit_data[key] = [v.strip() for v in new_value.split(",")]
            else:
                primefit_data[key] = st.text_area(key.replace("_", " ").capitalize(), value)
        primefit_data["notes"] = st.text_area("Notes", notes)

def generate_primefit_pdf_from_form():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    width, height = LETTER
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "PrimeFit Wellness Profile")
    c.setFont("Helvetica", 12)
    y -= 30

    for key, value in st.session_state.primefit_form.items():
        label = key.replace("_", " ").capitalize()
        if isinstance(value, list):
            text = f"{label}: {', '.join(value)}"
        else:
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
