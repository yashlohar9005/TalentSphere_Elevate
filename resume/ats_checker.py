import streamlit as st
import plotly.graph_objects as go
import json
from database import db_session, ATSResult

def render_ats_analysis(resume_data: dict, ai_engine) -> None:
    """Renders the ATS Analysis tab using the AIEngine."""
    st.subheader("ATS Resume Analysis")
    
    # Flatten resume data for analysis
    resume_text_parts = []
    
    personal = resume_data.get("personal", {})
    resume_text_parts.append(personal.get("name", ""))
    resume_text_parts.append(personal.get("email", ""))
    resume_text_parts.append(personal.get("phone", ""))
    
    resume_text_parts.append("Education")
    resume_text_parts.append(resume_data.get("education", ""))
    
    resume_text_parts.append("Experience")
    resume_text_parts.append(resume_data.get("experience", ""))
    
    resume_text_parts.append("Projects")
    resume_text_parts.append(resume_data.get("projects", ""))
    
    resume_text_parts.append("Skills")
    resume_text_parts.append(resume_data.get("skills", ""))
    
    resume_text_parts.append("Certifications")
    resume_text_parts.append(resume_data.get("certifications", ""))
    
    resume_text_parts.append("Achievements")
    resume_text_parts.append(resume_data.get("achievements", ""))
    
    resume_text_parts.append("Languages")
    resume_text_parts.append(resume_data.get("languages", ""))
    
    if resume_data.get("github"):
        resume_text_parts.append("GitHub: " + resume_data.get("github", ""))
        
    if resume_data.get("linkedin"):
        resume_text_parts.append("LinkedIn: " + resume_data.get("linkedin", ""))
        
    full_text = "\n".join(resume_text_parts)
    
    target_role = st.text_input("Target Role (optional, for keyword matching)", "Software Engineer")
    
    if st.button("Analyze Resume"):
        if not ai_engine:
            st.error("AI Engine is not connected. Cannot perform analysis.")
            return
            
        with st.spinner("Analyzing resume against ATS rules..."):
            result = ai_engine.resume_analyzer.analyze_resume(full_text, target_role)
            
            # Save to Database if user is logged in
            user_id = st.session_state.get("user_id")
            if user_id:
                with db_session() as session:
                    ats_record = ATSResult(
                        user_id=user_id,
                        resume_score=result["resume_score"],
                        ats_compatibility=result["ats_compatibility"],
                        keyword_match=result["keyword_match"],
                        formatting_score=result["formatting_score"],
                        education_score=result["education_score"],
                        project_score=result["project_score"],
                        experience_score=result["experience_score"],
                        technical_skills_score=result["technical_skills_score"],
                        soft_skills_score=result["soft_skills_score"],
                        feedback_json=json.dumps({
                            "strengths": result["strengths"],
                            "weaknesses": result["weaknesses"],
                            "suggestions": result["suggestions"]
                        })
                    )
                    session.add(ats_record)
            
            st.subheader("Analysis Results")
            
            col_gauge1, col_gauge2, col_gauge3 = st.columns(3)
            with col_gauge1:
                fig1 = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = result["resume_score"],
                    title = {'text': "Overall Resume Score"},
                    gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
                ))
                st.plotly_chart(fig1, use_container_width=True)
            with col_gauge2:
                fig2 = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = result["ats_compatibility"],
                    title = {'text': "ATS Compatibility"},
                    gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "green"}}
                ))
                st.plotly_chart(fig2, use_container_width=True)
            with col_gauge3:
                fig3 = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = result["keyword_match"],
                    title = {'text': "Keyword Match"},
                    gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "purple"}}
                ))
                st.plotly_chart(fig3, use_container_width=True)
                
            # Breakdown metrics
            st.markdown("### Score Breakdown")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Formatting", f"{result['formatting_score']}%")
            c2.metric("Education", f"{result['education_score']}%")
            c3.metric("Experience", f"{result['experience_score']}%")
            c4.metric("Projects", f"{result['project_score']}%")
            
            c5, c6, c7, c8 = st.columns(4)
            c5.metric("Tech Skills", f"{result.get('technical_skills_score', 0)}%")
            c6.metric("Soft Skills", f"{result.get('soft_skills_score', 0)}%")
            c7.metric("Job Fit", result.get("job_compatibility", "N/A"))
            c8.metric("Industry Rec.", result.get("industry_recommendation", "N/A"))
            
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.success("### Strengths")
                for s in result["strengths"]:
                    st.write(f"✅ {s}")
            with col2:
                st.error("### Weaknesses")
                for w in result["weaknesses"]:
                    st.write(f"❌ {w}")
                    
            if result["suggestions"]:
                st.warning("### ATS Optimization Tips")
                for sug in result["suggestions"]:
                    st.write(f"💡 {sug}")
