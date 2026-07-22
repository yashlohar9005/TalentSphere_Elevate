import streamlit as st
from database import db_session, User, Progress, StudentProfile
from reports.pdf_report import generate_certificate_pdf

def render_certificate_generator(user_id: int):
    st.subheader("Official Certificates")
    
    with db_session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        username = user.username if user else "User"
        
        profile = session.query(StudentProfile).filter_by(user_id=user_id).first()
        school_name = profile.school_name if profile and profile.school_name else ""
        student_class = profile.student_class if profile and profile.student_class else ""
        
        progress_items = session.query(Progress).filter(Progress.roadmap.has(user_id=user_id)).all()
        completed = sum(1 for p in progress_items if p.is_completed == 1)
        
    # Basic logic to unlock certificates
    certs_available = ["Participation Certificate"]
    
    if completed > 5:
        certs_available.append("Course Completion")
    if completed > 10:
        certs_available.append("Excellence Achievement")
        
    st.write("Unlock official certificates by completing your roadmap milestones.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### Available Certificates")
        for c in certs_available:
            st.success(f"🔓 {c}")
            
    with col2:
        cert_choice = st.selectbox("Select Certificate to Download", certs_available)
        
        if st.button("Generate Certificate"):
            try:
                pdf_bytes = generate_certificate_pdf(username, cert_choice, school_name, student_class)
                
                st.download_button(
                    label="⬇️ Download PDF Certificate",
                    data=pdf_bytes,
                    file_name=f"{cert_choice.replace(' ', '_')}_{username}.pdf",
                    mime="application/pdf"
                )
            except ImportError as e:
                st.error(str(e))
