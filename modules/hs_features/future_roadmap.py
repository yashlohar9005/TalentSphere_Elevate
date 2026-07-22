"""
Future Skills Roadmap Module for TalentSphere Elevate — High School.

Generates personalized 30/60/90-day roadmaps based on assessment results,
career goals, and AI recommendations. Each roadmap includes Weekly Tasks,
Learning Resources, Mini Projects, Certifications, and Milestones.

Reuses RoadmapGenerator and BasePortal.generate_roadmap().
"""

import streamlit as st
import json
import plotly.express as px
import pandas as pd
from database import (
    db_session, Assessment, CareerGoal, CareerQuizResult,
    InterestProfile, Roadmap, Progress,
)


# ──────────────────────────────────────────────────────────────────────────────
# Roadmap templates for each career stream
# ──────────────────────────────────────────────────────────────────────────────

ROADMAP_TEMPLATES: dict[str, dict] = {
    "STEM": {
        "title": "STEM Skills Roadmap",
        "30_day": {
            "tasks": ["Learn Python basics (variables, loops, functions)", "Solve 10 math puzzles on Khan Academy",
                      "Watch 3 science documentaries", "Set up a GitHub account"],
            "resources": ["Khan Academy — Algebra", "Codecademy — Python", "MIT OpenCourseWare"],
            "project": "Build a simple calculator in Python",
            "certification": "Google IT Support Certificate (start)",
        },
        "60_day": {
            "tasks": ["Complete a data analysis mini-project", "Learn HTML & CSS basics",
                      "Read 'A Brief History of Time'", "Join an online coding community"],
            "resources": ["freeCodeCamp", "Coursera — Data Science Basics", "HackerRank"],
            "project": "Create a personal portfolio website",
            "certification": "HackerRank Python Certification",
        },
        "90_day": {
            "tasks": ["Build an AI-powered chatbot", "Participate in a hackathon",
                      "Complete AP CS preparation module", "Contribute to open source"],
            "resources": ["Fast.ai", "LeetCode", "The Odin Project"],
            "project": "Develop a weather app using APIs",
            "certification": "AP Computer Science A (register)",
        },
    },
    "Arts": {
        "title": "Creative Arts Roadmap",
        "30_day": {
            "tasks": ["Start a daily journaling habit", "Read 2 classic novels",
                      "Watch TED talks on creativity", "Learn basic graphic design"],
            "resources": ["Canva Design School", "MasterClass Writing", "Project Gutenberg"],
            "project": "Write a 1000-word short story",
            "certification": "Canva Design Certificate",
        },
        "60_day": {
            "tasks": ["Join a school drama or debate club", "Create a blog or vlog",
                      "Study film-making basics", "Practice public speaking weekly"],
            "resources": ["WordPress.com", "YouTube Creator Academy", "Toastmasters Youth"],
            "project": "Produce a 3-minute short film or podcast episode",
            "certification": "Google Digital Garage — Fundamentals",
        },
        "90_day": {
            "tasks": ["Submit writing to a publication", "Organize a cultural event",
                      "Build a creative portfolio", "Enter an art competition"],
            "resources": ["Behance", "Medium", "Skillshare"],
            "project": "Curate an online art / writing portfolio",
            "certification": "Adobe Creative Cloud Certificate (start)",
        },
    },
    "Technology": {
        "title": "Technology Explorer Roadmap",
        "30_day": {
            "tasks": ["Learn Python variables and data types", "Set up VS Code",
                      "Complete 5 coding challenges", "Understand how the internet works"],
            "resources": ["Codecademy", "CS50 (Harvard)", "freeCodeCamp YouTube"],
            "project": "Build a CLI to-do list app",
            "certification": "Codecademy Python Certificate",
        },
        "60_day": {
            "tasks": ["Learn web development (HTML/CSS/JS)", "Build a responsive website",
                      "Study version control with Git", "Join a Discord coding community"],
            "resources": ["The Odin Project", "MDN Web Docs", "GitHub Learning Lab"],
            "project": "Create a weather dashboard web app",
            "certification": "freeCodeCamp Responsive Web Design",
        },
        "90_day": {
            "tasks": ["Learn React.js or Flask basics", "Build a full-stack project",
                      "Study databases and SQL", "Prepare for coding competitions"],
            "resources": ["Scrimba React", "SQLBolt", "LeetCode"],
            "project": "Deploy a full-stack app to the cloud",
            "certification": "AWS Cloud Practitioner (start studying)",
        },
    },
    "General": {
        "title": "Career Discovery Roadmap",
        "30_day": {
            "tasks": ["Take a personality assessment", "Research 5 careers of interest",
                      "Read about growth mindset", "Watch motivational career talks"],
            "resources": ["16Personalities.com", "O*NET OnLine", "TED Career Talks"],
            "project": "Create a career vision board",
            "certification": "LinkedIn Learning — Career Skills Certificate",
        },
        "60_day": {
            "tasks": ["Interview a professional in your field of interest", "Learn basic Excel/Sheets",
                      "Start a passion project", "Join a relevant club or community"],
            "resources": ["Google Sheets Tutorial", "Coursera Soft Skills", "Meetup.com"],
            "project": "Write a 'My Future Career' essay",
            "certification": "Google Digital Marketing Fundamentals",
        },
        "90_day": {
            "tasks": ["Build a beginner portfolio or resume", "Complete an online course",
                      "Volunteer in your field of interest", "Set 3-month goals with milestones"],
            "resources": ["Canva Resume Builder", "Coursera", "VolunteerMatch"],
            "project": "Present your career plan to a mentor or teacher",
            "certification": "Coursera Career Certificate (any introductory)",
        },
    },
}


def _determine_stream(user_id: int, session) -> str:
    """Determines the best stream for roadmap generation from user data."""
    # Check career quiz results
    quiz = (
        session.query(CareerQuizResult)
        .filter_by(user_id=user_id)
        .order_by(CareerQuizResult.completed_at.desc())
        .first()
    )
    if quiz:
        scores = json.loads(quiz.scores)
        top_cat = max(scores, key=scores.get) if scores else "General"
        if top_cat in ("Technology", "Logical Thinking", "Mathematics"):
            return "Technology"
        if top_cat in ("Creativity",):
            return "Arts"
        if top_cat in ("Interests", "STEM"):
            return "STEM"

    # Check interest profile
    interest = (
        session.query(InterestProfile)
        .filter_by(user_id=user_id)
        .order_by(InterestProfile.completed_at.desc())
        .first()
    )
    if interest:
        streams = json.loads(interest.recommended_streams)
        if streams:
            top = streams[0]
            if top in ROADMAP_TEMPLATES:
                return top

    # Check assessment
    assessment = (
        session.query(Assessment)
        .filter_by(user_id=user_id)
        .order_by(Assessment.completed_at.desc())
        .first()
    )
    if assessment:
        return "STEM" if assessment.category == "STEM" else "Arts"

    return "General"


def render_future_roadmap(user_id: int, ai_engine=None, portal=None) -> None:
    """Renders the Future Skills Roadmap page."""
    st.header("🗺️ Future Skills Roadmap")
    st.write("Your personalized 30/60/90-day learning journey based on your assessments and career goals.")

    with db_session() as session:
        stream = _determine_stream(user_id, session)

        # Check existing roadmaps
        existing_roadmaps = session.query(Roadmap).filter_by(user_id=user_id).all()

        # ── Show existing roadmap progress ──
        if existing_roadmaps:
            st.subheader("📈 Your Active Roadmaps")
            for rm in existing_roadmaps:
                items = session.query(Progress).filter_by(roadmap_id=rm.id).all()
                completed = sum(1 for i in items if i.is_completed)
                total = len(items)
                pct = int(completed / total * 100) if total > 0 else 0

                with st.expander(f"📋 {rm.title} — {pct}% Complete", expanded=False):
                    st.progress(pct / 100, text=f"{completed}/{total} milestones completed")
                    for item in items:
                        st.checkbox(
                            item.milestone_name,
                            value=bool(item.is_completed),
                            disabled=True,
                            key=f"fr_{item.id}",
                        )

            # Overall progress chart
            data = {"Roadmap": [], "Completion %": []}
            for rm in existing_roadmaps:
                items = session.query(Progress).filter_by(roadmap_id=rm.id).all()
                completed = sum(1 for i in items if i.is_completed)
                total = len(items)
                data["Roadmap"].append(rm.title[:30])
                data["Completion %"].append(int(completed / total * 100) if total > 0 else 0)

            if data["Roadmap"]:
                df = pd.DataFrame(data)
                fig = px.bar(df, x="Roadmap", y="Completion %", title="Roadmap Progress Overview",
                             range_y=[0, 100], color="Completion %",
                             color_continuous_scale="Viridis")
                st.plotly_chart(fig, width='stretch')

    # ── Generate New Roadmap ──
    st.markdown("---")
    st.subheader("🚀 Generate a New Roadmap")
    st.info(f"Based on your profile, we recommend the **{stream}** track.")

    template = ROADMAP_TEMPLATES.get(stream, ROADMAP_TEMPLATES["General"])

    # Preview the roadmap
    tab30, tab60, tab90 = st.tabs(["📅 30-Day Plan", "📅 60-Day Plan", "📅 90-Day Plan"])

    for tab, period in [(tab30, "30_day"), (tab60, "60_day"), (tab90, "90_day")]:
        with tab:
            plan = template[period]
            st.markdown("**Weekly Tasks:**")
            for t in plan["tasks"]:
                st.markdown(f"- ☐ {t}")
            st.markdown("**Learning Resources:**")
            for r in plan["resources"]:
                st.markdown(f"- 📚 {r}")
            st.markdown(f"**Mini Project:** 🛠️ {plan['project']}")
            st.markdown(f"**Certification:** 📜 {plan['certification']}")

    # Generate button
    if portal and st.button("✅ Generate This Roadmap", use_container_width=True):
        roadmap_title = template["title"]
        steps: list[str] = []
        for period_label, period_key in [("30-Day", "30_day"), ("60-Day", "60_day"), ("90-Day", "90_day")]:
            plan = template[period_key]
            for task in plan["tasks"]:
                steps.append(f"[{period_label}] {task}")
            steps.append(f"[{period_label}] 🛠️ Project: {plan['project']}")
            steps.append(f"[{period_label}] 📜 Certification: {plan['certification']}")

        portal.generate_roadmap(roadmap_title, steps, f"Personalized {stream} roadmap.")
