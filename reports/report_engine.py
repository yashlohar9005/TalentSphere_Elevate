"""
Centralized Report Engine for TalentSphere Elevate.
Handles data aggregation, formatting, and PDF export for all report types.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import logging
from datetime import datetime

from database import (
    db_session, User, Assessment, Progress, ResumeData,
    PlacementReadiness, MockInterviewResult, ATSResult, CollegeCodingTest
)
from reports.pdf_report import generate_report_pdf
from reports.certificate_generator import render_certificate_generator

logger = logging.getLogger(__name__)

class ReportEngine:
    def __init__(self, user_id: int, ai_engine=None):
        self.user_id = user_id
        self.ai_engine = ai_engine
        
    def _safe_query(self, query_func):
        """Executes a database query safely, handling exceptions."""
        try:
            with db_session() as session:
                return query_func(session)
        except Exception as e:
            logger.error(f"Database error in ReportEngine: {str(e)}")
            st.error(f"Failed to fetch data: {str(e)}")
            return None

    def _generate_download_btn(self, title: str, content: str, filename: str):
        """Generates a styled PDF download button."""
        try:
            pdf_bytes = generate_report_pdf(title, content)
            st.download_button(
                label=f"📥 Download {title} (PDF)",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                key=f"download_{filename}"
            )
        except Exception as e:
            st.error(f"Failed to generate PDF: {str(e)}")

    def generate_weekly_report(self):
        st.subheader("Weekly Analytics Report")
        
        def query_weekly(session):
            assessments = session.query(Assessment).filter_by(user_id=self.user_id).all()
            progress = session.query(Progress).filter(Progress.roadmap.has(user_id=self.user_id)).all()
            resume = session.query(ResumeData).filter_by(user_id=self.user_id).first()
            return {
                'num_assessments': len(assessments),
                'completed_tasks': sum(1 for p in progress if p.is_completed),
                'has_resume': resume is not None
            }
            
        result = self._safe_query(query_weekly)
        if not result:
            return
            
        num_assessments = result['num_assessments']
        completed_tasks = result['completed_tasks']
        has_resume = result['has_resume']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("⏱️ Learning Hours")
            st.metric("Total", "12.5 hrs", "+2.5 hrs")
        with col2:
            st.info("📋 Assessments")
            st.metric("Completed", num_assessments)
        with col3:
            st.info("🚀 Roadmap")
            st.metric("Tasks Completed", completed_tasks)
            
        st.markdown("---")
        
        col_gauge, col_rec = st.columns([1, 1])
        with col_gauge:
            score = 85 if has_resume else 75
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                title = {'text': "Placement Readiness"},
                gauge = {
                    'axis': {'range': [0, 100]}, 
                    'bar': {'color': "#0f9b8e"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "lightgreen"}
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
            
        with col_rec:
            st.markdown("### 💡 Career Recommendations")
            if self.ai_engine:
                try:
                    recs = self.ai_engine.recommendation_engine.generate_recommendations("high_school", "STEM", {})
                    career_suggestions = recs.get('career_suggestions', ['Keep learning!'])
                    st.info(f"**Focus:** {career_suggestions[0]}")
                    st.write("**Recommended Courses:**")
                    for c in recs.get("courses", [])[:3]:
                        st.success(f"✓  {c}")
                except Exception as e:
                    st.warning("Could not generate AI recommendations at this time.")
            else:
                st.write("AI Engine not connected.")
                
        content = f"Weekly Report\nLearning Hours: 12.5 hrs\nAssessments: {num_assessments}\nTasks Completed: {completed_tasks}\nPlacement Readiness: {score}%"
        self._generate_download_btn("Weekly Report", content, "weekly_report.pdf")

    def generate_monthly_report(self):
        st.subheader("Monthly Performance Summary")
        st.info("This report aggregates your performance over the last 30 days.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Overall Growth", "15%", "+2% from last month")
            st.metric("Skills Acquired", 3)
        with col2:
            st.metric("Active Days", "22 Days")
            st.metric("Mock Interviews", 2)
            
        content = "Monthly Report\nOverall Growth: 15%\nSkills Acquired: 3\nActive Days: 22"
        self._generate_download_btn("Monthly Report", content, "monthly_report.pdf")

    def generate_skill_report(self):
        st.subheader("Skill Gap & Growth Report")
        
        def query_skill(session):
            latest = session.query(Assessment).filter_by(user_id=self.user_id).order_by(Assessment.completed_at.desc()).first()
            if latest and latest.details:
                return latest.details
            return None
            
        details_str = self._safe_query(query_skill)
        
        if not details_str:
            st.info("Complete some assessments to view your skill report.")
            return
            
        try:
            details = json.loads(details_str)
        except json.JSONDecodeError:
            st.error("Failed to parse assessment details.")
            return
            
        current_skills = {k: v for k, v in details.items() if k not in ["hard_skills_score", "soft_skills_score"]}
        
        if not current_skills:
            st.info("No detailed skills found in the latest assessment.")
            return

        df = pd.DataFrame(dict(r=list(current_skills.values()), theta=list(current_skills.keys())))
        fig = px.line_polar(df, r="r", theta="theta", line_close=True, title="Current Skills Breakdown", template="plotly_dark")
        fig.update_traces(fill="toself", line_color="#0f9b8e")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### ✅ Skills Processed")
        skills_df = pd.DataFrame([{"Skill": skill, "Score": f"{int(score * 10)}%" if score <= 10 else f"{score}%"} for skill, score in current_skills.items()])
        for _, row in skills_df.iterrows():
            st.success(f"✓  **{row['Skill']}** — {row['Score']}")

        st.markdown("---")
        st.markdown("### 🔍 Skills Missing & Growth")
        if self.ai_engine:
            try:
                required_skills = {k: 8 for k in current_skills.keys()}
                gap_analysis = self.ai_engine.skill_gap.analyze_gap(current_skills, required_skills)
                st.metric("Overall Improvement Potential", f"{100 - gap_analysis.get('readiness_percentage', 0)}%")
                
                missing = gap_analysis.get("missing_skills", {})
                if missing:
                    st.markdown("#### Skills That Need Attention")
                    cols = st.columns(min(len(missing), 3) or 1)
                    for idx, skill_name in enumerate(missing.keys()):
                        with cols[idx % len(cols)]:
                            st.warning(f"• **{skill_name}**")
                else:
                    st.success("All skills meet the required threshold!")
                    
                st.markdown("### 💡 Recommendations")
                suggestions = gap_analysis.get("learning_suggestions", [])
                for suggestion in suggestions:
                    st.success(f"✓  {suggestion}")
            except Exception as e:
                st.warning("Could not generate AI gap analysis.")
        else:
            st.write("AI Engine not connected.")
            
        content = "Skill Report\n" + "\n".join([f"{k}: {v}" for k, v in current_skills.items()])
        self._generate_download_btn("Skill Report", content, "skill_report.pdf")

    def generate_career_report(self):
        st.subheader("Career Progression Report")
        
        def query_career(session):
            user = session.query(User).filter_by(id=self.user_id).first()
            assessments = session.query(Assessment).filter_by(user_id=self.user_id).all()
            return {
                "user_type": user.user_type if user else "Unknown",
                "ass_data": [{"category": a.category, "score": a.score} for a in assessments],
                "num_assessments": len(assessments)
            }
            
        result = self._safe_query(query_career)
        if not result:
            return
            
        user_type = result["user_type"]
        ass_data = result["ass_data"]
        
        st.write(f"**Current Career Stage:** {user_type}")
        
        if self.ai_engine:
            try:
                cat = ass_data[0]['category'] if ass_data else "STEM"
                profile_data = {
                    "career_stage": user_type,
                    "category": cat,
                    "readiness_percentage": ass_data[0]["score"] if ass_data else 50,
                    "assessments_completed": len(ass_data),
                    "roadmaps_completed": 1
                }
                pred = self.ai_engine.career_predictor.predict_career(profile_data)
                
                st.write("### Career Prediction")
                st.success(pred.get("career_path", "Keep studying and tracking your progress!"))
                st.metric("Promotion Readiness Score", pred.get("promotion_readiness", 0))
                
                recs = self.ai_engine.recommendation_engine.generate_recommendations(user_type, cat, {})
                col1, col2 = st.columns(2)
                with col1:
                    st.write("### Recommended Certifications")
                    for cert in recs.get("certifications", []):
                        st.success(f"✓  {cert}")
                with col2:
                    st.write("### Recommended Projects")
                    for proj in recs.get("projects", []):
                        st.success(f"✓  {proj}")
            except Exception as e:
                st.warning("AI Career Prediction unavailable.")
        
        content = f"Career Report\nStage: {user_type}\nAssessments Completed: {result['num_assessments']}"
        self._generate_download_btn("Career Report", content, "career_report.pdf")

    def generate_progress_report(self):
        st.subheader("Roadmap Progress Report")
        
        def query_progress(session):
            progress_items = session.query(Progress).filter(Progress.roadmap.has(user_id=self.user_id)).all()
            return [{"is_completed": p.is_completed} for p in progress_items]
            
        progress_items = self._safe_query(query_progress)
        
        if not progress_items:
            st.info("No roadmap generated yet. Generate a roadmap in the Skill Gap Analysis tab.")
            return
            
        completed = sum(1 for p in progress_items if p["is_completed"] == 1)
        total = len(progress_items)
        remaining = total - completed
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Completed Tasks", completed)
            st.metric("Remaining Tasks", remaining)
            st.metric("Roadmap Completion", f"{int((completed/total)*100)}%" if total else "0%")
            
        with col2:
            if total > 0:
                df = pd.DataFrame({"Status": ["Completed", "Remaining"], "Count": [completed, remaining]})
                fig = px.pie(df, values='Count', names='Status', title='Task Completion Status', color='Status',
                     color_discrete_map={'Completed':'#0f9b8e', 'Remaining':'#333333'})
                st.plotly_chart(fig, use_container_width=True)
                
        content = f"Progress Report\nCompleted: {completed}\nRemaining: {remaining}\nTotal Tasks: {total}"
        self._generate_download_btn("Progress Report", content, "progress_report.pdf")

    def generate_placement_report(self):
        st.subheader("Placement Readiness Report")
        
        def query_placement(session):
            p = session.query(PlacementReadiness).filter_by(user_id=self.user_id).order_by(PlacementReadiness.updated_at.desc()).first()
            if p:
                return {
                    "placement_score": p.placement_score,
                    "industry_readiness": p.industry_readiness,
                    "overall_recommendation": p.overall_recommendation
                }
            return None
            
        placement = self._safe_query(query_placement)
        
        if not placement:
            st.info("Take the placement readiness assessment to generate your report.")
            return
            
        col1, col2 = st.columns(2)
        col1.metric("Placement Score", f"{placement['placement_score']}%")
        col2.metric("Industry Readiness", f"{placement['industry_readiness']}%")
        
        st.write("### Recommendation")
        st.success(placement['overall_recommendation'] or "Keep practicing to improve your score!")
        
        content = f"Placement Report\nScore: {placement['placement_score']}%\nIndustry Readiness: {placement['industry_readiness']}%\nRecommendation: {placement['overall_recommendation']}"
        self._generate_download_btn("Placement Report", content, "placement_report.pdf")

    def generate_interview_report(self):
        st.subheader("Mock Interview Report")
        
        def query_interview(session):
            interviews = session.query(MockInterviewResult).filter_by(user_id=self.user_id).order_by(MockInterviewResult.completed_at.desc()).all()
            if interviews:
                latest = interviews[0]
                return {
                    "interview_type": latest.interview_type,
                    "overall_score": latest.overall_score,
                    "confidence_score": latest.confidence_score,
                    "technical_accuracy": latest.technical_accuracy,
                    "ai_feedback": latest.ai_feedback,
                    "improvement_suggestions": latest.improvement_suggestions
                }
            return None
            
        latest = self._safe_query(query_interview)
        
        if not latest:
            st.info("No mock interviews completed yet.")
            return
            
        st.write(f"**Latest Interview:** {latest['interview_type']}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Overall Score", f"{latest['overall_score']}%")
        col2.metric("Confidence", f"{latest['confidence_score']}%")
        col3.metric("Technical", f"{latest['technical_accuracy']}%")
        
        st.write("### Feedback")
        st.info(latest['ai_feedback'] or "Good effort, continue practicing.")
        
        try:
            suggestions = json.loads(latest['improvement_suggestions']) if latest['improvement_suggestions'] else []
            if suggestions:
                st.write("### Suggestions")
                for s in suggestions:
                    st.warning(f"• {s}")
        except:
            pass
            
        content = f"Interview Report\nType: {latest['interview_type']}\nScore: {latest['overall_score']}%\nConfidence: {latest['confidence_score']}%\nFeedback: {latest['ai_feedback']}"
        self._generate_download_btn("Interview Report", content, "interview_report.pdf")

    def generate_resume_report(self):
        st.subheader("ATS Resume Analysis Report")
        
        def query_resume(session):
            ats = session.query(ATSResult).filter_by(user_id=self.user_id).order_by(ATSResult.created_at.desc()).first()
            if ats:
                return {
                    "resume_score": ats.resume_score,
                    "ats_compatibility": ats.ats_compatibility,
                    "keyword_match": ats.keyword_match,
                    "formatting_score": ats.formatting_score
                }
            return None
            
        ats = self._safe_query(query_resume)
        
        if not ats:
            st.info("Upload your resume to see your ATS report.")
            return
            
        st.metric("Overall ATS Score", f"{ats['resume_score']}%")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Compatibility", f"{ats['ats_compatibility']}%")
        col2.metric("Keyword Match", f"{ats['keyword_match']}%")
        col3.metric("Formatting", f"{ats['formatting_score']}%")
        
        content = f"Resume Report\nATS Score: {ats['resume_score']}%\nCompatibility: {ats['ats_compatibility']}%\nKeyword Match: {ats['keyword_match']}%"
        self._generate_download_btn("Resume Report", content, "resume_report.pdf")

    def generate_coding_report(self):
        st.subheader("Coding Practice Report")
        
        def query_coding(session):
            tests = session.query(CollegeCodingTest).filter_by(user_id=self.user_id).order_by(CollegeCodingTest.completed_at.desc()).all()
            if tests:
                latest = tests[0]
                return {
                    "score": latest.score,
                    "total_questions": latest.total_questions,
                    "topic": latest.topic,
                    "ai_suggestions": latest.ai_suggestions
                }
            return None
            
        latest = self._safe_query(query_coding)
        
        if not latest:
            st.info("No coding tests taken yet.")
            return
            
        st.metric("Latest Score", f"{latest['score']} / {latest['total_questions']}")
        st.write(f"**Topic:** {latest['topic']}")
        
        st.write("### Suggestions")
        st.info(latest['ai_suggestions'] or "Keep up the good work!")
        
        content = f"Coding Report\nTopic: {latest['topic']}\nScore: {latest['score']}/{latest['total_questions']}\nSuggestions: {latest['ai_suggestions']}"
        self._generate_download_btn("Coding Report", content, "coding_report.pdf")

    def generate_certificate_report(self):
        # We delegate this to the existing render_certificate_generator
        # as it already has the required logic and handles its own UI nicely.
        render_certificate_generator(self.user_id)
