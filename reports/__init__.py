"""
Reports and Certificate Engine for TalentSphere Elevate.
"""
import streamlit as st
from reports.student_info_card import render_student_info_card
from reports.report_engine import ReportEngine

def render_reports_manager(user_id: int, ai_engine):
    st.header("Reports & Certificates")

    # Student Information Card — displayed before all report tabs
    render_student_info_card(user_id)
    tabs = st.tabs([
        "Weekly Report", 
        "Monthly Report",
        "Skill Report", 
        "Career Report", 
        "Progress Report",
        "Placement Report",
        "Interview Report",
        "Resume Report",
        "Coding Report",
        "Certificates"
    ])
    
    engine = ReportEngine(user_id, ai_engine)
    
    with tabs[0]:
        engine.generate_weekly_report()
        
    with tabs[1]:
        engine.generate_monthly_report()
        
    with tabs[2]:
        engine.generate_skill_report()
        
    with tabs[3]:
        engine.generate_career_report()
        
    with tabs[4]:
        engine.generate_progress_report()
        
    with tabs[5]:
        engine.generate_placement_report()
        
    with tabs[6]:
        engine.generate_interview_report()
        
    with tabs[7]:
        engine.generate_resume_report()
        
    with tabs[8]:
        engine.generate_coding_report()
        
    with tabs[9]:
        engine.generate_certificate_report()
