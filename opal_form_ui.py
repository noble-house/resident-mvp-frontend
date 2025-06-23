import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def render_opal_form():
    opal = st.session_state.opal_form

    with st.form("opal_form"):
        opal["name"] = st.text_input("Full Name", opal.get("name", ""))
        opal["age"] = st.text_input("Age or Date of Birth", opal.get("age", ""))
        opal["birthplace"] = st.text_input("Birthplace", opal.get("birthplace", ""))
        opal["previous_residence"] = st.text_input("Previous Residence", opal.get("previous_residence", ""))
        opal["career"] = st.text_input("Career", opal.get("career", ""))
        opal["military_service"] = st.checkbox("Military Service?", opal.get("military_service", False))
        opal["military_branch"] = st.text_input("Branch of Service", opal.get("military_branch", ""))
        opal["military_duration"] = st.text_input("Service Duration", opal.get("military_duration", ""))
        opal["hobbies_interests"] = st.text_area("Hobbies & Interests", opal.get("hobbies_interests", ""))
        opal["favorites_music"] = st.text_input("Favorite Music", opal.get("favorites_music", ""))
        opal["favorites_movies"] = st.text_input("Favorite Movies", opal.get("favorites_movies", ""))
        opal["favorites_books"] = st.text_input("Favorite Books", opal.get("favorites_books", ""))
        opal["achievements"] = st.text_area("Achievements", opal.get("achievements", ""))
        opal["daily_routine"] = st.text_area("Typical Daily Routine", opal.get("daily_routine", ""))
        opal["religion_beliefs"] = st.text_input("Religion / Spiritual Beliefs", opal.get("religion_beliefs", ""))
        opal["important_people"] = st.text_area("Important People", opal.get("important_people", ""))
        opal["health_conditions"] = st.text_input("Health Conditions", opal.get("health_conditions", ""))
        opal["mobility_needs"] = st.text_input("Mobility Needs", opal.get("mobility_needs", ""))
        opal["communication"] = st.text_input("Communication Needs", opal.get("communication", ""))
        opal["likes_dislikes"] = st.text_area("Likes & Dislikes", opal.get("likes_dislikes", ""))
        opal["notes"] = st.text_area("AI-generated Life Story Summary (100+ words)", opal.get("notes", ""))

        st.form_submit_button("💾 Save")

def generate_opal_pdf_from_form():
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    opal = st.session_state.opal_form
    y = 750

    for label, key in [
        ("Name", "name"),
        ("Age", "age"),
        ("Birthplace", "birthplace"),
        ("Previous Residence", "previous_residence"),
        ("Career", "career"),
        ("Military Service", "military_service"),
        ("Branch", "military_branch"),
        ("Duration", "military_duration"),
        ("Hobbies", "hobbies_interests"),
        ("Fav Music", "favorites_music"),
        ("Fav Movies", "favorites_movies"),
        ("Fav Books", "favorites_books"),
        ("Achievements", "achievements"),
        ("Routine", "daily_routine"),
        ("Religion", "religion_beliefs"),
        ("Important People", "important_people"),
        ("Health", "health_conditions"),
        ("Mobility", "mobility_needs"),
        ("Communication", "communication"),
        ("Likes/Dislikes", "likes_dislikes"),
        ("Life Story Summary", "notes")
    ]:
        value = str(opal.get(key, ""))
        if y < 60:
            p.showPage()
            y = 750
        p.drawString(40, y, f"{label}: {value[:100]}")
        y -= 20

    p.save()
    buffer.seek(0)
    return buffer.getvalue()
