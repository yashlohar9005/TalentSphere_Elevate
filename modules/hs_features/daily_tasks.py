"""
Daily Learning Tasks Module for TalentSphere Elevate — High School.

Auto-generates daily tasks based on active goals and assessments.
Task categories: coding, aptitude, career, reading, communication.
Displays Today's Tasks, Weekly Tasks, Completed %, Pending %.
"""

import streamlit as st
import json
import random
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from database import (
    db_session, DailyTask, CareerGoal, CareerQuizResult, Assessment,
)


# ──────────────────────────────────────────────────────────────────────────────
# Task Templates — keyed by category
# ──────────────────────────────────────────────────────────────────────────────

TASK_TEMPLATES: dict[str, list[str]] = {
    "coding": [
        "Learn Python Variables — complete 3 exercises",
        "Practice Python Loops — write 2 loop programs",
        "Learn Python Functions — create a reusable function",
        "Study Python Lists — solve 3 list manipulation problems",
        "Practice Python Strings — write a string reversal program",
        "Learn Python Dictionaries — build a contact book",
        "Study Python Conditions — solve 3 if-else problems",
        "Practice Python File I/O — read and write a text file",
        "Build a mini Python project — number guessing game",
        "Review Python Operators — complete operator exercises",
    ],
    "aptitude": [
        "Solve 5 Quantitative Aptitude questions",
        "Complete 5 Logical Reasoning puzzles",
        "Practice 5 Verbal Ability questions",
        "Solve 3 Pattern Recognition problems",
        "Complete 5 Analytical Thinking exercises",
        "Practice percentage and ratio problems",
        "Solve time and work aptitude questions",
        "Complete a series completion exercise",
        "Practice data interpretation questions",
        "Solve 5 probability problems",
    ],
    "career": [
        "Watch a career guidance video (15 min)",
        "Read about a trending career in AI/ML",
        "Research the education path for your career goal",
        "Read an article about future technology trends",
        "Watch a TED talk on personal development",
        "Explore a new career on the Career Explorer page",
        "Read about the day-in-the-life of a Software Engineer",
        "Research scholarship opportunities in your field",
        "Read about entrepreneurship success stories",
        "Watch a documentary about innovation",
    ],
    "reading": [
        "Read a chapter of a self-improvement book",
        "Read about AI and its impact on society",
        "Read a news article about technology",
        "Read about famous scientists and their discoveries",
        "Read a blog post about study techniques",
        "Read about the history of computing",
        "Read a Wikipedia article about a topic you're curious about",
        "Read about mental health and well-being",
        "Read about environmental sustainability",
        "Read a short story or poem",
    ],
    "communication": [
        "Complete a public speaking exercise (2-min speech)",
        "Practice email writing — draft a formal email",
        "Write a 200-word essay on any topic",
        "Practice active listening — summarize a podcast episode",
        "Complete a vocabulary building exercise (10 new words)",
        "Practice body language — record yourself presenting",
        "Write a thank-you note to a teacher or mentor",
        "Practice grammar — complete 10 grammar exercises",
        "Prepare a 3-slide presentation on any topic",
        "Have a structured conversation about a career topic",
    ],
}

CATEGORIES = list(TASK_TEMPLATES.keys())


def _generate_daily_tasks(user_id: int, date_str: str) -> list[dict]:
    """Generates 5 daily tasks (one per category) for a given date."""
    random.seed(f"{user_id}_{date_str}")  # Deterministic per user+date
    tasks: list[dict] = []
    for cat in CATEGORIES:
        task_text = random.choice(TASK_TEMPLATES[cat])
        tasks.append({"task_text": task_text, "category": cat})
    return tasks


def _ensure_tasks_exist(user_id: int, date_str: str, session) -> list:
    """Ensures daily tasks exist in DB for the given date; creates if missing."""
    existing = (
        session.query(DailyTask)
        .filter_by(user_id=user_id, task_date=date_str)
        .all()
    )
    if existing:
        return existing

    # Generate and save
    generated = _generate_daily_tasks(user_id, date_str)
    new_tasks = []
    for t in generated:
        dt = DailyTask(
            user_id=user_id,
            task_date=date_str,
            task_text=t["task_text"],
            category=t["category"],
        )
        session.add(dt)
        new_tasks.append(dt)
    session.flush()
    return new_tasks


def render_daily_tasks(user_id: int) -> None:
    """Renders the Daily Learning Tasks page."""
    st.header("📋 Daily Learning Tasks")
    st.write("Stay on track with personalized daily tasks across 5 learning categories.")

    today = datetime.utcnow().strftime("%Y-%m-%d")

    tab_today, tab_week, tab_stats = st.tabs(["📅 Today's Tasks", "📆 This Week", "📊 Progress Stats"])

    # ── Today's Tasks ──
    with tab_today:
        st.subheader(f"Tasks for {today}")
        with db_session() as session:
            tasks = _ensure_tasks_exist(user_id, today, session)
            completed_count = sum(1 for t in tasks if t.is_completed)
            total_count = len(tasks)

            if total_count > 0:
                st.progress(completed_count / total_count, text=f"{completed_count}/{total_count} completed")

            for task in tasks:
                col1, col2 = st.columns([5, 1])
                with col1:
                    icon = {"coding": "💻", "aptitude": "🧮", "career": "🎯", "reading": "📖", "communication": "🗣️"}
                    cat_icon = icon.get(task.category, "📋")
                    checked = st.checkbox(
                        f"{cat_icon} [{task.category.title()}] {task.task_text}",
                        value=bool(task.is_completed),
                        key=f"dt_{task.id}",
                    )
                    if checked != bool(task.is_completed):
                        task.is_completed = 1 if checked else 0
                        task.completed_at = datetime.utcnow() if checked else None
                        session.commit()
                        st.rerun()

    # ── Weekly View ──
    with tab_week:
        st.subheader("This Week's Tasks")
        with db_session() as session:
            week_data: list[dict] = []
            for i in range(7):
                day = (datetime.utcnow() - timedelta(days=datetime.utcnow().weekday()) + timedelta(days=i))
                day_str = day.strftime("%Y-%m-%d")
                day_label = day.strftime("%a %b %d")
                tasks = _ensure_tasks_exist(user_id, day_str, session)
                completed = sum(1 for t in tasks if t.is_completed)
                total = len(tasks)
                week_data.append({
                    "Day": day_label, "Completed": completed,
                    "Pending": total - completed, "Total": total,
                })

            df = pd.DataFrame(week_data)
            fig = px.bar(
                df, x="Day", y=["Completed", "Pending"],
                title="Weekly Task Completion",
                barmode="stack",
                color_discrete_map={"Completed": "#00CC96", "Pending": "#EF553B"},
            )
            st.plotly_chart(fig, width='stretch')

            # Expandable daily details
            for i, row in enumerate(week_data):
                day_date = (datetime.utcnow() - timedelta(days=datetime.utcnow().weekday()) + timedelta(days=i))
                day_str = day_date.strftime("%Y-%m-%d")
                tasks = session.query(DailyTask).filter_by(user_id=user_id, task_date=day_str).all()
                with st.expander(f"{row['Day']} — {row['Completed']}/{row['Total']} completed"):
                    for t in tasks:
                        status = "✅" if t.is_completed else "⬜"
                        st.write(f"{status} [{t.category.title()}] {t.task_text}")

    # ── Progress Stats ──
    with tab_stats:
        st.subheader("📊 Overall Progress")
        with db_session() as session:
            all_tasks = session.query(DailyTask).filter_by(user_id=user_id).all()
            if not all_tasks:
                st.info("No task history yet. Complete today's tasks to see your progress!")
                return

            total = len(all_tasks)
            completed = sum(1 for t in all_tasks if t.is_completed)
            pending = total - completed

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Tasks", total)
            with col2:
                st.metric("Completed ✅", f"{completed} ({int(completed / total * 100)}%)")
            with col3:
                st.metric("Pending ⏳", f"{pending} ({int(pending / total * 100)}%)")

            # Category breakdown
            cat_data: dict[str, dict] = {}
            for t in all_tasks:
                if t.category not in cat_data:
                    cat_data[t.category] = {"completed": 0, "total": 0}
                cat_data[t.category]["total"] += 1
                if t.is_completed:
                    cat_data[t.category]["completed"] += 1

            df_cat = pd.DataFrame([
                {"Category": cat.title(), "Completed": d["completed"], "Total": d["total"],
                 "Completion %": int(d["completed"] / d["total"] * 100) if d["total"] > 0 else 0}
                for cat, d in cat_data.items()
            ])
            fig = px.bar(df_cat, x="Category", y="Completion %", title="Completion by Category",
                         range_y=[0, 100], color="Category")
            st.plotly_chart(fig, width='stretch')
