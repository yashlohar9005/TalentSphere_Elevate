import streamlit as st
import json
from database import db_session, Course, CareerPath

def render_course_manager():
    st.subheader("Course & Career Path Management")
    
    tab1, tab2 = st.tabs(["Courses", "Career Paths"])
    
    with tab1:
        st.write("### Add New Course")
        with st.form("add_course_form"):
            title = st.text_input("Course Title")
            category = st.text_input("Category (e.g., Programming, Leadership)")
            description = st.text_area("Description")
            if st.form_submit_button("Add Course"):
                with db_session() as session:
                    new_course = Course(title=title, category=category, description=description)
                    session.add(new_course)
                st.success(f"Added course: {title}")
                st.rerun()
                
        st.write("### Existing Courses")
        with db_session() as session:
            courses = session.query(Course).all()
            for c in courses:
                col1, col2 = st.columns([4, 1])
                col1.write(f"**{c.title}** ({c.category}) - {c.description}")
                if col2.button("Delete", key=f"del_c_{c.id}"):
                    session.delete(c)
                    session.commit()
                    st.rerun()
                    
    with tab2:
        st.write("### Add Career Path")
        with st.form("add_cp_form"):
            cp_title = st.text_input("Career Path Title")
            skills = st.text_input("Required Skills (comma separated)")
            certs = st.text_input("Recommended Certifications (comma separated)")
            if st.form_submit_button("Add Career Path"):
                s_list = [s.strip() for s in skills.split(",")] if skills else []
                c_list = [c.strip() for c in certs.split(",")] if certs else []
                with db_session() as session:
                    new_cp = CareerPath(title=cp_title, skills=json.dumps(s_list), certifications=json.dumps(c_list))
                    session.add(new_cp)
                st.success(f"Added Career Path: {cp_title}")
                st.rerun()
                
        st.write("### Existing Career Paths")
        with db_session() as session:
            paths = session.query(CareerPath).all()
            for p in paths:
                with st.expander(p.title):
                    st.write(f"**Skills:** {', '.join(json.loads(p.skills)) if p.skills else 'None'}")
                    st.write(f"**Certs:** {', '.join(json.loads(p.certifications)) if p.certifications else 'None'}")
                    if st.button("Delete", key=f"del_p_{p.id}"):
                        session.delete(p)
                        session.commit()
                        st.rerun()
