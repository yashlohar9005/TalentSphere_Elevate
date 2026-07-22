"""
Student Information Card for TalentSphere Elevate Reports.

Renders a professional information card at the top of every report page,
displaying the student's name, DOB, user type, latest assessment date,
and overall assessment score.
"""

import streamlit as st
from database import db_session, User, Assessment, StudentProfile, CollegeStudentProfile
from sqlalchemy import func
from sqlalchemy.orm import selectinload

def _fetch_student_data(user_id: int) -> dict:
    """
    Fetches all data required for the student information card dynamically.
    Converts ORM objects to dictionaries within the session to prevent DetachedInstanceError.
    """
    with db_session() as session:
        # Eager load the related profiles
        user = session.query(User).options(
            selectinload(User.student_profile),
            selectinload(User.college_student_profile)
        ).filter_by(id=user_id).first()
        
        if not user:
            return {
                "full_name": "Not Provided",
                "dob": "Not Provided",
                "user_type": "Not Provided",
                "assessment_date": "Not Provided",
                "overall_score": None,
                "is_college": False
            }

        display_name = user.full_name if user.full_name else user.username
        dob_display = user.dob if user.dob else "Not Provided"
        user_type = user.user_type if user.user_type else "Not Provided"
        student_id = f"STU-{user.id:04d}"

        # Fetch latest assessment
        latest_assessment = (
            session.query(Assessment)
            .filter_by(user_id=user_id)
            .order_by(Assessment.completed_at.desc())
            .first()
        )
        if latest_assessment and latest_assessment.completed_at:
            assessment_date = latest_assessment.completed_at.strftime("%d/%m/%Y %I:%M %p")
        else:
            assessment_date = "Not Provided"

        # Overall score
        avg_result = session.query(func.avg(Assessment.score)).filter_by(user_id=user_id).scalar()
        overall_score = round(avg_result) if avg_result is not None else None

        # Helper to handle missing values
        def val(x):
            return str(x).strip() if x and str(x).strip() else "Not Provided"

        data = {
            "full_name": val(display_name),
            "dob": val(dob_display),
            "user_type": val(user_type),
            "student_id": val(student_id),
            "assessment_date": val(assessment_date),
            "overall_score": overall_score,
            "email": "Not Provided",
            "mobile": "Not Provided",
            "gender": "Not Provided",
            "percentage": "Not Provided",
            "dream_career": "Not Provided",
            "area_of_interest": "Not Provided",
            "is_college": (user_type == "College Student")
        }

        # Populate profile data based on User Type
        if data["is_college"]:
            profile = user.college_student_profile
            if profile:
                data["email"] = val(profile.email)
                data["mobile"] = val(profile.mobile)
                data["gender"] = val(profile.gender)
                
                # Check for cgpa first, then percentage
                if profile.cgpa and str(profile.cgpa).strip():
                    data["percentage"] = val(profile.cgpa)
                else:
                    data["percentage"] = val(profile.percentage)
                    
                data["dream_career"] = val(profile.dream_role)
                data["area_of_interest"] = val(profile.preferred_industry)
                
                data["college_name"] = val(profile.college_name)
                data["university"] = val(profile.university_name)
                data["branch"] = val(profile.department)
                data["course"] = val(profile.degree)
                
                sem = profile.semester if profile.semester else ""
                yr = profile.year_of_study if profile.year_of_study else ""
                data["semester"] = val(f"{sem} {yr}".strip())
                data["skills"] = val(profile.programming_languages)
                data["preferred_role"] = val(profile.interested_job_roles)
            else:
                data["college_name"] = "Not Provided"
                data["university"] = "Not Provided"
                data["branch"] = "Not Provided"
                data["course"] = "Not Provided"
                data["semester"] = "Not Provided"
                data["skills"] = "Not Provided"
                data["preferred_role"] = "Not Provided"
        else:
            profile = user.student_profile
            if profile:
                data["email"] = val(profile.email)
                data["mobile"] = val(profile.mobile)
                data["gender"] = val(profile.gender)
                data["percentage"] = val(profile.percentage)
                data["dream_career"] = val(profile.dream_career)
                data["area_of_interest"] = val(profile.interest)
                data["school_name"] = val(profile.school_name)
                data["student_class"] = val(profile.student_class)
                data["board"] = val(profile.board)
                data["skills"] = val(profile.strengths)
            else:
                data["school_name"] = "Not Provided"
                data["student_class"] = "Not Provided"
                data["board"] = "Not Provided"
                data["skills"] = "Not Provided"

        return data


def render_student_info_card(user_id: int) -> None:
    """
    Renders a professional Student Information Card using Streamlit
    containers, columns, and metric widgets.
    """
    data = _fetch_student_data(user_id)

    with st.container():
        st.markdown(
            """
            <style>
            .student-card {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border-radius: 12px;
                padding: 24px 32px;
                margin-bottom: 24px;
                border-left: 5px solid #0f9b8e;
            }
            .student-card h3 {
                color: #0f9b8e;
                margin-bottom: 4px;
            }
            .student-card p {
                color: #e0e0e0;
                margin: 0;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### 📋 Student Information")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("**Student Name**")
            st.info(f"🎓  {data['full_name']}")
        with c2:
            st.markdown("**Student ID**")
            st.info(f"🆔  {data['student_id']}")
        with c3:
            st.markdown("**User Type**")
            st.info(f"👤  {data['user_type']}")
        with c4:
            st.markdown("**Date of Birth**")
            st.info(f"📅  {data['dob']}")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("**Email**")
            st.info(f"📧  {data['email']}")
        with c2:
            st.markdown("**Mobile Number**")
            st.info(f"📱  {data['mobile']}")
        with c3:
            st.markdown("**Gender**")
            st.info(f"🧑  {data['gender']}")
        with c4:
            st.markdown("**Current Percentage/CGPA**")
            st.info(f"📈  {data['percentage']}")

        st.markdown("---")
        
        c1, c2, c3, c4 = st.columns(4)
        if data["is_college"]:
            with c1:
                st.markdown("**College Name**")
                st.info(f"🏫  {data['college_name']}")
            with c2:
                st.markdown("**University**")
                st.info(f"🎓  {data['university']}")
            with c3:
                st.markdown("**Branch / Department**")
                st.info(f"🏛️  {data['branch']}")
            with c4:
                st.markdown("**Semester / Year**")
                st.info(f"📅  {data['semester']}")
        else:
            with c1:
                st.markdown("**School Name**")
                st.info(f"🏫  {data['school_name']}")
            with c2:
                st.markdown("**Class**")
                st.info(f"📚  {data['student_class']}")
            with c3:
                st.markdown("**Board**")
                st.info(f"📜  {data['board']}")
            with c4:
                st.markdown("**Skills**")
                st.info(f"⚡  {data['skills']}")
                
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("**Dream Career**")
            st.info(f"🎯  {data['dream_career']}")
        with c2:
            st.markdown("**Area of Interest**")
            st.info(f"💡  {data['area_of_interest']}")
        with c3:
            st.markdown("**Assessment Date**")
            st.info(f"🕐  {data['assessment_date']}")
        with c4:
            st.markdown("**Overall Assessment Score**")
            if data["overall_score"] is not None:
                st.metric(label="Score", value=f"{data['overall_score']} / 100")
            else:
                st.warning("Not Provided")

        st.markdown("---")
