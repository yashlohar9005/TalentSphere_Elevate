"""
Personal Information module for High School Students.
Handles fetching and updating the StudentProfile.
"""

import streamlit as st
from database import db_session, StudentProfile

def render_personal_information(user_id: int):
    st.header("📄 Personal Information")
    st.write("Keep your profile updated to receive better AI recommendations and accurate reports.")
    
    # Fetch existing profile if available
    with db_session() as session:
        profile = session.query(StudentProfile).filter_by(user_id=user_id).first()
        
        # We need a disconnected dict to easily pre-fill Streamlit fields without keeping the session open unnecessarily
        if profile:
            profile_data = {
                "full_name": profile.full_name or "",
                "dob": profile.dob or "",
                "gender": profile.gender or "Select",
                "blood_group": profile.blood_group or "Select",
                "mobile": profile.mobile or "",
                "email": profile.email or "",
                "school_name": profile.school_name or "",
                "student_class": profile.student_class or "Select",
                "board": profile.board or "Select",
                "percentage": profile.percentage or "",
                "favorite_subject": profile.favorite_subject or "",
                "least_favorite_subject": profile.least_favorite_subject or "",
                "dream_career": profile.dream_career or "",
                "interest": profile.interest or "",
                "hobbies": profile.hobbies or "",
                "strengths": profile.strengths or "",
                "weaknesses": profile.weaknesses or "",
                "city": profile.city or "",
                "state": profile.state or "",
                "country": profile.country or ""
            }
        else:
            profile_data = {
                "full_name": "", "dob": "", "gender": "Select", "blood_group": "Select",
                "mobile": "", "email": "", "school_name": "", "student_class": "Select",
                "board": "Select", "percentage": "", "favorite_subject": "", 
                "least_favorite_subject": "", "dream_career": "", "interest": "",
                "hobbies": "", "strengths": "", "weaknesses": "", "city": "", 
                "state": "", "country": ""
            }

    with st.form("personal_information_form"):
        # Basic Details
        with st.expander("👤 Basic Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name", value=profile_data["full_name"])
                gender_options = ["Select", "Male", "Female", "Other", "Prefer not to say"]
                gender_idx = gender_options.index(profile_data["gender"]) if profile_data["gender"] in gender_options else 0
                gender = st.selectbox("Gender", gender_options, index=gender_idx)
                mobile = st.text_input("Mobile Number", value=profile_data["mobile"])
            with col2:
                dob = st.text_input("Date of Birth (DD/MM/YYYY)", value=profile_data["dob"])
                bg_options = ["Select", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
                bg_idx = bg_options.index(profile_data["blood_group"]) if profile_data["blood_group"] in bg_options else 0
                blood_group = st.selectbox("Blood Group", bg_options, index=bg_idx)
                email = st.text_input("Email Address", value=profile_data["email"])

        # Academic Details
        with st.expander("🎓 Academic Details", expanded=True):
            col3, col4 = st.columns(2)
            with col3:
                school_name = st.text_input("School Name", value=profile_data["school_name"])
                class_options = ["Select", "8th", "9th", "10th", "11th", "12th"]
                class_idx = class_options.index(profile_data["student_class"]) if profile_data["student_class"] in class_options else 0
                student_class = st.selectbox("Class", class_options, index=class_idx)
                favorite_subject = st.text_input("Favourite Subject", value=profile_data["favorite_subject"])
            with col4:
                board_options = ["Select", "State", "CBSE", "ICSE", "Others"]
                board_idx = board_options.index(profile_data["board"]) if profile_data["board"] in board_options else 0
                board = st.selectbox("Board", board_options, index=board_idx)
                percentage = st.text_input("Current Percentage/Grade", value=profile_data["percentage"])
                least_favorite_subject = st.text_input("Least Favourite Subject", value=profile_data["least_favorite_subject"])

        # Career Information
        with st.expander("🎯 Career Information", expanded=True):
            col5, col6 = st.columns(2)
            with col5:
                dream_career = st.text_input("Dream Career", value=profile_data["dream_career"])
                hobbies = st.text_area("Hobbies", value=profile_data["hobbies"])
                weaknesses = st.text_area("Weaknesses", value=profile_data["weaknesses"])
            with col6:
                interest = st.text_input("Area of Interest", value=profile_data["interest"])
                strengths = st.text_area("Strengths", value=profile_data["strengths"])
                

        # Address
        with st.expander("📍 Address", expanded=True):
            col7, col8 = st.columns(2)
            with col7:
                city = st.text_input("City", value=profile_data["city"])
                country = st.text_input("Country", value=profile_data["country"])
            with col8:
                state = st.text_input("State", value=profile_data["state"])

        st.markdown("---")
        submit_btn = st.form_submit_button(label="Save / Update Profile")

    if submit_btn:
        # Save updates to SQLite
        try:
            with db_session() as session:
                db_profile = session.query(StudentProfile).filter_by(user_id=user_id).first()
                if not db_profile:
                    db_profile = StudentProfile(user_id=user_id)
                    session.add(db_profile)
                
                db_profile.full_name = full_name
                db_profile.dob = dob
                db_profile.gender = gender if gender != "Select" else None
                db_profile.blood_group = blood_group if blood_group != "Select" else None
                db_profile.mobile = mobile
                db_profile.email = email
                db_profile.school_name = school_name
                db_profile.student_class = student_class if student_class != "Select" else None
                db_profile.board = board if board != "Select" else None
                db_profile.percentage = percentage
                db_profile.favorite_subject = favorite_subject
                db_profile.least_favorite_subject = least_favorite_subject
                db_profile.dream_career = dream_career
                db_profile.interest = interest
                db_profile.hobbies = hobbies
                db_profile.strengths = strengths
                db_profile.weaknesses = weaknesses
                db_profile.city = city
                db_profile.state = state
                db_profile.country = country
                
                # Update user table's full_name and dob to keep them in sync
                from database import User
                user = session.query(User).filter_by(id=user_id).first()
                if user:
                    if full_name:
                        user.full_name = full_name
                    if dob:
                        user.dob = dob
            
            st.success("✅ Personal Information successfully saved and updated!")
            st.balloons()
            st.rerun() # Refresh page to show updated data
            
        except Exception as e:
            st.error(f"Failed to update profile: {str(e)}")
