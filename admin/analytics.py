import streamlit as st
import pandas as pd
import plotly.express as px
from database import db_session, User, Assessment, ResumeData

def render_analytics(ai_engine):
    st.subheader("Platform Analytics")
    
    with db_session() as session:
        users = session.query(User).all()
        assessments = session.query(Assessment).all()
        resumes = session.query(ResumeData).all()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Users", len(users))
        col2.metric("Active Users", sum(1 for u in users if u.is_active == 1))
        col3.metric("Assessments Completed", len(assessments))
        col4.metric("Resumes Built", len(resumes))
        
        st.markdown("---")
        
        # User Distribution Pie Chart
        user_types = [u.user_type for u in users]
        if user_types:
            df_users = pd.DataFrame(user_types, columns=["User Type"])
            type_counts = df_users["User Type"].value_counts().reset_index()
            type_counts.columns = ["User Type", "Count"]
            
            fig_pie = px.pie(type_counts, names="User Type", values="Count", title="User Demographics")
            st.plotly_chart(fig_pie, width='stretch')
            
        # Assessments Bar Chart
        if assessments:
            categories = [a.category for a in assessments]
            df_ass = pd.DataFrame(categories, columns=["Category"])
            cat_counts = df_ass["Category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]
            
            fig_bar = px.bar(cat_counts, x="Category", y="Count", title="Assessment Categories", color="Category")
            st.plotly_chart(fig_bar, width='stretch')
            
        # Placement/Promotion Readiness Placeholder
        st.subheader("Readiness Heatmap")
        heatmap_data = pd.DataFrame({
            'Python': [80, 60, 40],
            'Leadership': [50, 70, 90],
            'Communication': [60, 80, 85]
        }, index=['High School', 'College', 'Professional'])
        fig_heat = px.imshow(heatmap_data, text_auto=True, title="Average Skill Ratings by User Type")
        st.plotly_chart(fig_heat, width='stretch')
