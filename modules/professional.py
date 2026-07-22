"""
Professional Module for TalentSphere Elevate.

This module provides functionalities tailored for Working Professionals.
It inherits from BasePortal and implements advanced assessments, 
skill gap analysis, recommendation engines, and 30/60/90 day roadmaps.
"""

import streamlit as st
import json
from database import db_session, Assessment
from modules.base_portal import BasePortal

class ProfessionalPortal(BasePortal):
    """
    Professional portal inheriting from BasePortal.
    """
    
    def __init__(self, user_id: int, username: str, ai_engine=None):
        super().__init__(user_id, username, portal_prefix="pro", ai_engine=ai_engine)
        self.pages = ["Dashboard", "Assessment", "Skill Gap Analysis", "Roadmap & Progress", "Resume Builder", "Reports & Certificates", "Notifications"]

    def _calculate_promotion_readiness(self, latest_assessment: Assessment) -> int:
        """Calculates a simulated promotion readiness score (0-100)."""
        if not latest_assessment:
            return 0
        details = json.loads(latest_assessment.details)
        # Weighted average of leadership, comms, and hard skills
        soft = details.get("soft_skills_score", 0)
        hard = details.get("hard_skills_score", 0)
        return int((soft * 0.6) + (hard * 0.4))

    def render_dashboard(self) -> None:
        st.header("Professional Dashboard")
        st.write(f"Welcome back, {self.username}! Here is an overview of your career trajectory.")
        
        with db_session() as session:
            assessments = self.fetch_assessments(session)
            roadmaps = self.fetch_roadmaps(session)
            latest = assessments[-1] if assessments else None
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Assessments Completed", len(assessments))
            with col2:
                st.metric("Active Roadmaps", len(roadmaps))
            with col3:
                st.metric("Certifications", len(roadmaps)) # Proxy for certs completed
            with col4:
                readiness = self._calculate_promotion_readiness(latest)
                st.metric("Promotion Readiness", f"{readiness}%")
                
            if assessments:
                st.subheader("Career Growth Analytics")
                
                tab1, tab2 = st.tabs(["Learning Trend", "Skill Progression"])
                with tab1:
                    self.plot_assessment_history(assessments)
                with tab2:
                    if latest:
                        details = json.loads(latest.details)
                        self.plot_radar_chart(details, exclude_keys=["hard_skills_score", "soft_skills_score"])
            else:
                st.info("Complete your first assessment to unlock career growth analytics.")

    def render_assessment(self) -> None:
        st.header("Professional Readiness Assessment")
        st.write("Evaluate your technical and soft skills to identify career growth opportunities.")
        
        with st.form("pro_assessment_form"):
            st.subheader("Technical Skills")
            col1, col2 = st.columns(2)
            with col1:
                q_py = st.slider("Python Proficiency", 1, 10, 5)
                q_sql = st.slider("SQL & Data Modeling", 1, 10, 5)
                q_sys = st.slider("System Design", 1, 10, 5)
            with col2:
                q_docker = st.slider("Docker / Containerization", 1, 10, 5)
                q_k8s = st.slider("Kubernetes", 1, 10, 5)
                q_aws = st.slider("AWS / Cloud Architecture", 1, 10, 5)
                
            st.subheader("Soft Skills & Leadership")
            col3, col4 = st.columns(2)
            with col3:
                q_comm = st.slider("Communication", 1, 10, 5)
                q_lead = st.slider("Leadership & Mentoring", 1, 10, 5)
            with col4:
                q_prob = st.slider("Problem Solving", 1, 10, 5)
                q_time = st.slider("Time Management", 1, 10, 5)
            
            submitted = st.form_submit_button("Submit Assessment")
            
            if submitted:
                hard_skills = (q_py + q_sql + q_sys + q_docker + q_k8s + q_aws) / 6 * 10
                soft_skills = (q_comm + q_lead + q_prob + q_time) / 4 * 10
                
                category = "Engineering Leader" if soft_skills > 75 and hard_skills > 75 else ("Technical Specialist" if hard_skills > soft_skills else "Product / Management Focused")
                final_score = max(hard_skills, soft_skills)
                
                details = {
                    "Python": q_py, "SQL": q_sql, "System Design": q_sys, 
                    "Docker": q_docker, "Kubernetes": q_k8s, "AWS": q_aws,
                    "Communication": q_comm, "Leadership": q_lead, 
                    "Problem Solving": q_prob, "Time Management": q_time,
                    "hard_skills_score": hard_skills, "soft_skills_score": soft_skills
                }
                
                with db_session() as session:
                    new_assessment = Assessment(
                        user_id=self.user_id,
                        category=category,
                        score=int(final_score),
                        details=json.dumps(details)
                    )
                    session.add(new_assessment)
                
                st.success(f"Assessment completed! Your professional archetype is: {category}")
                st.rerun()

    def _generate_recommendations(self, category: str) -> tuple:
        """
        Rule-based recommendation engine. 
        Designed to be easily replaceable with an LLM call in the future.
        Returns (courses, certs, projects, roadmap_title, roadmap_plan).
        """
        if category == "Engineering Leader":
            courses = ["Advanced System Design", "Engineering Management 101"]
            certs = ["AWS Certified Solutions Architect - Professional"]
            projects = ["Architect a scalable microservices backend"]
            roadmap_title = "Path to Staff Engineer / Manager"
            plan = [
                ("30-Day Plan", ["Read 'Designing Data-Intensive Applications'", "Lead a technical design review"]),
                ("60-Day Plan", ["Complete AWS Solutions Architect course", "Mentor a junior developer"]),
                ("90-Day Plan", ["Pass AWS Cert exam", "Propose a major architectural improvement to leadership"])
            ]
        elif category == "Technical Specialist":
            courses = ["Kubernetes in Action", "Advanced Python Concurrency"]
            certs = ["Certified Kubernetes Administrator (CKA)"]
            projects = ["Build a CI/CD pipeline from scratch"]
            roadmap_title = "Cloud Native Expert"
            plan = [
                ("30-Day Plan", ["Master Docker fundamentals", "Deploy a simple app to AWS ECS"]),
                ("60-Day Plan", ["Take CKA preparation course", "Implement monitoring with Prometheus/Grafana"]),
                ("90-Day Plan", ["Pass CKA exam", "Migrate a monolithic service to Kubernetes"])
            ]
        else:
            courses = ["Agile Product Management", "Data-Driven Decision Making"]
            certs = ["Certified Scrum Master (CSM)"]
            projects = ["Lead a cross-functional sprint delivery"]
            roadmap_title = "Product / Management Track"
            plan = [
                ("30-Day Plan", ["Complete Agile basics course", "Run a successful sprint retrospective"]),
                ("60-Day Plan", ["Prepare for CSM exam", "Improve team velocity by 10%"]),
                ("90-Day Plan", ["Pass CSM exam", "Present quarterly roadmap to stakeholders"])
            ]
            
        return courses, certs, projects, roadmap_title, plan

    def render_skill_gap(self) -> None:
        st.header("Skill Gap Analysis & Recommendation Engine")
        
        with db_session() as session:
            latest = session.query(Assessment).filter_by(user_id=self.user_id).order_by(Assessment.completed_at.desc()).first()
            
            if not latest:
                st.warning("Please complete an Assessment first.")
                return
                
            details = json.loads(latest.details)
            category = latest.category
            
            # --- 1. Skill Gap Analysis ---
            st.subheader("1. Skill Gap Analysis")
            st.write(f"**Current Archetype:** {category}")
            self.plot_radar_chart(details, exclude_keys=["hard_skills_score", "soft_skills_score"])
            
            # --- 2. Recommendation Engine ---
            st.subheader("2. AI-Ready Recommendation Engine")
            st.write("Based on your assessment, here are targeted recommendations to close your skill gaps.")
            
            if self.ai_engine:
                recs = self.ai_engine.recommendation_engine.generate_recommendations("professional", category, details)
                courses = recs.get("courses", [])
                certs = recs.get("certifications", [])
                projects = recs.get("projects", [])
                
                roadmap = self.ai_engine.roadmap_generator.generate_roadmap("professional", category)
                roadmap_title = roadmap["title"]
                flat_steps = roadmap["flat_steps"]
            else:
                courses, certs, projects, roadmap_title, plan = self._generate_recommendations(category)
                flat_steps = []
                for phase, tasks in plan:
                    for task in tasks:
                        flat_steps.append(f"[{phase}] {task}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("**Recommended Courses**\n\n" + "\n".join(f"- {c}" for c in courses))
            with col2:
                st.success("**Target Certifications**\n\n" + "\n".join(f"- {c}" for c in certs))
            with col3:
                st.warning("**Portfolio Projects**\n\n" + "\n".join(f"- {p}" for p in projects))

            # --- 3. Roadmap Generator ---
            st.subheader("3. 30/60/90 Day Roadmap Generator")
            st.write(f"Generate your personalized **{roadmap_title}** roadmap.")
            
            if st.button("Generate 30/60/90 Day Roadmap"):
                self.generate_roadmap(roadmap_title, flat_steps, f"Structured 30/60/90 day plan for {roadmap_title}.")

def show_dashboard(ai_engine=None) -> None:
    user_id = st.session_state.get('user_id')
    username = st.session_state.get('username')
    
    if not user_id:
        st.error("Authentication error. Please log in again.")
        return
        
    portal = ProfessionalPortal(user_id, username, ai_engine=ai_engine)
    portal.run(portal.pages)
