import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def render_opal_form():
    form_data = st.session_state.get("opal_form", {})
    with st.form("opal_form"):
        col1, col2 = st.columns(2)
        with col1:
            form_data["name"] = st.text_input("Name", form_data.get("name", ""))
            form_data["age"] = st.text_input("Age / DOB", form_data.get("age", ""))
            form_data["birthplace"] = st.text_input("Birthplace", form_data.get("birthplace", ""))
            form_data["previous_residence"] = st.text_input("Previous Residence", form_data.get("previous_residence", ""))
            form_data["career"] = st.text_input("Career", form_data.get("career", ""))
            form_data["military_service"] = st.checkbox("Military Service", form_data.get("military_service", False))
            form_data["military_branch"] = st.text_input("Military Branch", form_data.get("military_branch", ""))
            form_data["military_duration"] = st.text_input("Military Duration", form_data.get("military_duration", ""))
            form_data["hobbies_interests"] = st.text_area("Hobbies & Interests", form_data.get("hobbies_interests", ""))
            form_data["achievements"] = st.text_area("Achievements", form_data.get("achievements", ""))
        with col2:
            form_data["favorites_music"] = st.text_input("Favorite Music", form_data.get("favorites_music", ""))
            form_data["favorites_movies"] = st.text_input("Favorite Movies", form_data.get("favorites_movies", ""))
            form_data["favorites_books"] = st.text_input("Favorite Books", form_data.get("favorites_books", ""))
            form_data["daily_routine"] = st.text_area("Daily Routine", form_data.get("daily_routine", ""))
            form_data["religion_beliefs"] = st.text_input("Religion / Beliefs", form_data.get("religion_beliefs", ""))
            form_data["important_people"] = st.text_area("Important People", form_data.get("important_people", ""))
            form_data["health_conditions"] = st.text_input("Health Conditions", form_data.get("health_conditions", ""))
            form_data["mobility_needs"] = st.text_input("Mobility Needs", form_data.get("mobility_needs", ""))
            form_data["communication"] = st.text_input("Communication Style", form_data.get("communication", ""))
            form_data["likes_dislikes"] = st.text_area("Likes & Dislikes", form_data.get("likes_dislikes", ""))
        form_data["notes"] = st.text_area("📝 Life Story Summary (Auto)", form_data.get("notes", ""), height=200)

        st.session_state.opal_form = form_data
        st.form_submit_button("💾 Save Changes")

def generate_opal_pdf_from_form():
    data = st.session_state.get("opal_form", {})
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "OPAL Life Story Summary")
    c.setFont("Helvetica", 11)
    y -= 30

    for key, value in data.items():
        if y < 60:
            c.showPage()
            y = height - 40
        c.drawString(40, y, f"{key.replace('_', ' ').capitalize()}: {value}")
        y -= 20

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
