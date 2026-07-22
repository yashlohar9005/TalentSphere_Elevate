import streamlit as st
from admin import analytics, user_manager, course_manager, quiz_manager, notification_manager

def show_dashboard(ai_engine=None):
    st.title("Admin Management System")
    st.write("Welcome to the TalentSphere Elevate Admin control panel.")
    
    # Verify Admin Role
    if st.session_state.get("user_type") != "Admin":
        st.error("Unauthorized access. Admin privileges required.")
        return
        
    tabs = st.tabs([
        "Analytics", 
        "User Management", 
        "Course & Career Paths", 
        "Quiz Management", 
        "Notification Center"
    ])
    
    with tabs[0]:
        analytics.render_analytics(ai_engine)
        
    with tabs[1]:
        user_manager.render_user_manager(ai_engine)
        
    with tabs[2]:
        course_manager.render_course_manager()
        
    with tabs[3]:
        quiz_manager.render_quiz_manager()
        
    with tabs[4]:
        notification_manager.render_notification_manager()
