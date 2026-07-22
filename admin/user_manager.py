import streamlit as st
import json
import bcrypt
from database import db_session, User, Assessment, ResumeData, Progress

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def render_user_manager(ai_engine):
    st.subheader("User Management")
    
    with db_session() as session:
        users = session.query(User).all()
        
        if not users:
            st.info("No users found.")
            return
            
        # Filter and Search
        search_query = st.text_input("Search by Username")
        filter_type = st.selectbox("Filter by Type", ["All", "High School Student", "College Student", "Working Professional", "Admin"])
        
        filtered_users = users
        if filter_type != "All":
            filtered_users = [u for u in filtered_users if u.user_type == filter_type]
        if search_query:
            filtered_users = [u for u in filtered_users if search_query.lower() in u.username.lower()]
            
        st.write(f"Showing {len(filtered_users)} users")
        
        user_options = {f"{u.username} (ID: {u.id})": u.id for u in filtered_users}
        selected_user_label = st.selectbox("Select a User to Manage", ["-- Select User --"] + list(user_options.keys()))
        
        if selected_user_label != "-- Select User --":
            user_id = user_options[selected_user_label]
            user = session.query(User).filter_by(id=user_id).first()
            
            st.markdown(f"### Manage: {user.username}")
            st.write(f"**Type:** {user.user_type} | **Status:** {'Active' if user.is_active else 'Deactivated'}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Toggle Active Status"):
                    user.is_active = 0 if user.is_active == 1 else 1
                    session.commit()
                    st.success("Status updated!")
                    st.rerun()
            with col2:
                new_pw = st.text_input("New Password", type="password")
                if st.button("Reset Password") and new_pw:
                    user.password_hash = hash_password(new_pw)
                    session.commit()
                    st.success("Password reset!")
            with col3:
                if st.button("Delete User"):
                    session.delete(user)
                    session.commit()
                    st.success("User deleted!")
                    st.rerun()
                    
            st.subheader("User Insights")
            tab1, tab2, tab3 = st.tabs(["Assessments", "Resume & ATS", "Progress"])
            
            with tab1:
                assessments = session.query(Assessment).filter_by(user_id=user.id).all()
                for a in assessments:
                    st.write(f"- **{a.category}**: Score {a.score}")
            with tab2:
                resume = session.query(ResumeData).filter_by(user_id=user.id).first()
                if resume:
                    st.json(json.loads(resume.content))
                    if st.button("View ATS Score"):
                        # Just an integration hook
                        st.info("Pass resume text to ai_engine to score.")
                else:
                    st.write("No resume built yet.")
            with tab3:
                # Progress
                st.write("Progress milestones will appear here.")
