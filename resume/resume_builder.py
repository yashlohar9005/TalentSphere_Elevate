"""
Resume Builder UI for TalentSphere Elevate.
"""
import streamlit as st
import json
from database import db_session, ResumeData
from resume.ats_checker import render_ats_analysis
from resume.pdf_export import generate_pdf

def get_resume_data(session, user_id: int) -> dict:
    record = session.query(ResumeData).filter_by(user_id=user_id).first()
    if record:
        return json.loads(record.content)
    return {}

def save_resume_data(session, user_id: int, data: dict):
    record = session.query(ResumeData).filter_by(user_id=user_id).first()
    if record:
        record.content = json.dumps(data)
    else:
        new_record = ResumeData(user_id=user_id, content=json.dumps(data))
        session.add(new_record)

def render_resume_manager(user_id: int, ai_engine) -> None:
    st.header("Resume Builder")
    
    tabs = st.tabs(["Builder", "Preview", "ATS Analysis", "PDF Download"])
    
    with db_session() as session:
        data = get_resume_data(session, user_id)
        
    with tabs[0]:
        with st.form("resume_builder_form"):
            st.subheader("Personal Details")
            personal = data.get("personal", {})
            name = st.text_input("Full Name", value=personal.get("name", ""))
            email = st.text_input("Email", value=personal.get("email", ""))
            phone = st.text_input("Phone", value=personal.get("phone", ""))
            
            st.subheader("Professional Links")
            github = st.text_input("GitHub Profile", value=data.get("github", ""))
            linkedin = st.text_input("LinkedIn Profile", value=data.get("linkedin", ""))
            
            st.subheader("Core Sections")
            education = st.text_area("Education", value=data.get("education", ""), height=100)
            experience = st.text_area("Experience", value=data.get("experience", ""), height=150)
            projects = st.text_area("Projects", value=data.get("projects", ""), height=150)
            skills = st.text_area("Skills", value=data.get("skills", ""), height=100)
            
            st.subheader("Additional Information")
            certifications = st.text_area("Certifications", value=data.get("certifications", ""))
            achievements = st.text_area("Achievements", value=data.get("achievements", ""))
            languages = st.text_area("Languages", value=data.get("languages", ""))
            
            if st.form_submit_button("Save Resume"):
                new_data = {
                    "personal": {"name": name, "email": email, "phone": phone},
                    "github": github,
                    "linkedin": linkedin,
                    "education": education,
                    "experience": experience,
                    "projects": projects,
                    "skills": skills,
                    "certifications": certifications,
                    "achievements": achievements,
                    "languages": languages
                }
                with db_session() as session:
                    save_resume_data(session, user_id, new_data)
                st.success("Resume saved successfully!")
                st.rerun()

    with tabs[1]:
        st.subheader("Resume Preview")
        if not data:
            st.info("Fill out the Builder tab and save your resume to see the preview.")
        else:
            personal = data.get("personal", {})
            st.markdown(f"## {personal.get('name', '')}")
            st.markdown(f"**Email:** {personal.get('email', '')} | **Phone:** {personal.get('phone', '')}")
            st.markdown(f"**GitHub:** {data.get('github', '')} | **LinkedIn:** {data.get('linkedin', '')}")
            
            for section in ["Education", "Experience", "Projects", "Skills", "Certifications", "Achievements", "Languages"]:
                content = data.get(section.lower(), "")
                if content:
                    st.markdown(f"### {section}")
                    st.markdown(content)

    with tabs[2]:
        if not data:
            st.info("Save your resume first to run the ATS Analysis.")
        else:
            render_ats_analysis(data, ai_engine)

    with tabs[3]:
        st.subheader("Export to PDF")
        if not data:
            st.info("Save your resume first to download it as a PDF.")
        else:
            template = st.selectbox("Select Template", ["Modern", "Professional", "Minimal"])
            
            try:
                pdf_bytes = generate_pdf(data, template)
                st.download_button(
                    label="Download Resume PDF",
                    data=pdf_bytes,
                    file_name="resume.pdf",
                    mime="application/pdf"
                )
            except ImportError as e:
                st.error(str(e))
                st.info("Please install reportlab: pip install reportlab")
