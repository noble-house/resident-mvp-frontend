import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


def render_opal_form():
    """Render OPAL Life Story Form UI"""
    if "opal_form" not in st.session_state:
        st.session_state.opal_form = {}

    form = st.session_state.opal_form

    st.subheader("👤 Resident Information")
    form["name"] = st.text_input("Full Name", value=form.get("name", ""))
    form["age"] = st.text_input("Age or DOB", value=form.get("age", ""))
    form["birthplace"] = st.text_input("Birthplace", value=form.get("birthplace", ""))
    form["previous_residence"] = st.text_input("Previous Residence", value=form.get("previous_residence", ""))
    form["career"] = st.text_input("Career", value=form.get("career", ""))

    st.subheader("🎖️ Military Service")
    form["military_service"] = st.checkbox("Has Served in Military", value=form.get("military_service", False))
    if form["military_service"]:
        form["military_branch"] = st.text_input("Branch", value=form.get("military_branch", ""))
        form["military_duration"] = st.text_input("Service Duration", value=form.get("military_duration", ""))
    else:
        form["military_branch"] = ""
        form["military_duration"] = ""

    st.subheader("🎨 Interests & Preferences")
    form["hobbies_interests"] = st.text_area("Hobbies & Interests", value=form.get("hobbies_interests", ""))
    form["favorites_music"] = st.text_input("Favorite Music", value=form.get("favorites_music", ""))
    form["favorites_movies"] = st.text_input("Favorite Movies", value=form.get("favorites_movies", ""))
    form["favorites_books"] = st.text_input("Favorite Books", value=form.get("favorites_books", ""))

    st.subheader("🏆 Achievements & Daily Life")
    form["achievements"] = st.text_area("Achievements", value=form.get("achievements", ""))
    form["daily_routine"] = st.text_area("Daily Routine", value=form.get("daily_routine", ""))

    st.subheader("🙏 Beliefs & Relationships")
    form["religion_beliefs"] = st.text_area("Religion or Beliefs", value=form.get("religion_beliefs", ""))
    form["important_people"] = st.text_area("Important People in Life", value=form.get("important_people", ""))

    st.subheader("🩺 Health & Accessibility")
    form["health_conditions"] = st.text_area("Health Conditions / Allergies", value=form.get("health_conditions", ""))
    form["mobility_needs"] = st.text_input("Mobility Needs", value=form.get("mobility_needs", ""))
    form["communication"] = st.text_input("Communication Style / Notes", value=form.get("communication", ""))

    st.subheader("💬 Personality")
    form["likes_dislikes"] = st.text_area("Likes / Dislikes", value=form.get("likes_dislikes", ""))

    st.subheader("📝 AI-Generated Notes / Life Summary")
    form["notes"] = st.text_area("Summary / Notes", value=form.get("notes", ""), height=120)

    st.session_state.opal_form = form


def generate_opal_pdf_from_form() -> bytes:
    """Generate a clean formatted OPAL Life Story PDF using reportlab"""
    form = st.session_state.get("opal_form", {})
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 50
    y = height - margin

    def draw_section_title(title):
        nonlocal y
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y, title)
        y -= 18

    def draw_field(label, value):
        nonlocal y
        value = str(value or "")  # Safely cast None to empty string
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin, y, f"{label}:")
        y -= 14
        c.setFont("Helvetica", 11)
        text_obj = c.beginText(margin + 10, y)
        for line in value.split("\n"):
            text_obj.textLine(line.strip())
            y -= 13
        c.drawText(text_obj)
        y -= 8

        if y < 100:
            c.showPage()
            y = height - margin

    draw_section_title("👤 Resident Information")
    draw_field("Full Name", form.get("name"))
    draw_field("Age or DOB", form.get("age"))
    draw_field("Birthplace", form.get("birthplace"))
    draw_field("Previous Residence", form.get("previous_residence"))
    draw_field("Career", form.get("career"))

    draw_section_title("🎖️ Military Service")
    if form.get("military_service"):
        draw_field("Branch", form.get("military_branch"))
        draw_field("Service Duration", form.get("military_duration"))
    else:
        draw_field("Military Service", "No")

    draw_section_title("🎨 Interests & Preferences")
    draw_field("Hobbies & Interests", form.get("hobbies_interests"))
    draw_field("Favorite Music", form.get("favorites_music"))
    draw_field("Favorite Movies", form.get("favorites_movies"))
    draw_field("Favorite Books", form.get("favorites_books"))

    draw_section_title("🏆 Achievements & Daily Life")
    draw_field("Achievements", form.get("achievements"))
    draw_field("Daily Routine", form.get("daily_routine"))

    draw_section_title("🙏 Beliefs & Relationships")
    draw_field("Religion or Beliefs", form.get("religion_beliefs"))
    draw_field("Important People in Life", form.get("important_people"))

    draw_section_title("🩺 Health & Accessibility")
    draw_field("Health Conditions / Allergies", form.get("health_conditions"))
    draw_field("Mobility Needs", form.get("mobility_needs"))
    draw_field("Communication Style", form.get("communication"))

    draw_section_title("💬 Personality")
    draw_field("Likes / Dislikes", form.get("likes_dislikes"))

    draw_section_title("📝 AI-Generated Life Summary")
    draw_field("Summary / Notes", form.get("notes"))

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
