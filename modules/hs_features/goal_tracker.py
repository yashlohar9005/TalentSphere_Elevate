"""
Goal Tracker Module for TalentSphere Elevate — High School.

Allows students to Create, Edit, Delete, and Track goals with
progress bars, deadlines, completion percentages, and notifications.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from database import db_session, Goal
from notifications.notification_service import send_notification


def render_goal_tracker(user_id: int) -> None:
    """Renders the Goal Tracker page."""
    st.header("🎯 Goal Tracker")
    st.write("Set personal goals, track your progress, and stay accountable.")

    tab_goals, tab_create, tab_analytics = st.tabs(["📋 My Goals", "➕ Create Goal", "📊 Analytics"])

    # ── My Goals ──
    with tab_goals:
        _render_goals_list(user_id)

    # ── Create Goal ──
    with tab_create:
        _render_create_goal(user_id)

    # ── Analytics ──
    with tab_analytics:
        _render_goal_analytics(user_id)


def _render_goals_list(user_id: int) -> None:
    """Renders the list of user goals with edit/delete/progress controls."""
    with db_session() as session:
        goals = (
            session.query(Goal)
            .filter_by(user_id=user_id)
            .order_by(Goal.created_at.desc())
            .all()
        )

        if not goals:
            st.info("You haven't set any goals yet. Go to the 'Create Goal' tab to get started!")
            return

        # Summary metrics
        active = [g for g in goals if g.status == "Active"]
        completed = [g for g in goals if g.status == "Completed"]
        avg_progress = int(sum(g.progress for g in active) / len(active)) if active else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Goals", len(active))
        with col2:
            st.metric("Completed", len(completed))
        with col3:
            st.metric("Avg Progress", f"{avg_progress}%")

        st.markdown("---")

        # Goal cards
        for goal in goals:
            _render_goal_card(goal, user_id, session)


def _render_goal_card(goal, user_id: int, session) -> None:
    """Renders a single goal card with edit, delete, and progress controls."""
    status_icons = {"Active": "🟢", "Completed": "✅", "Cancelled": "⛔"}
    icon = status_icons.get(goal.status, "🔵")

    with st.container(border=True):
        col_title, col_status = st.columns([4, 1])
        with col_title:
            st.markdown(f"### {icon} {goal.title}")
        with col_status:
            st.caption(goal.status)

        if goal.description:
            st.write(goal.description)

        # Progress bar
        st.progress(goal.progress / 100, text=f"Progress: {goal.progress}%")

        # Deadline
        if goal.deadline:
            deadline = datetime.strptime(goal.deadline, "%Y-%m-%d")
            days_left = (deadline - datetime.utcnow()).days
            if days_left < 0:
                st.error(f"⚠️ Overdue by {abs(days_left)} day(s)")
            elif days_left <= 3:
                st.warning(f"⏰ {days_left} day(s) left")
            else:
                st.caption(f"📅 Deadline: {goal.deadline} ({days_left} days left)")

        # Action buttons
        if goal.status == "Active":
            col_progress, col_complete, col_edit, col_delete = st.columns(4)

            with col_progress:
                new_progress = st.slider(
                    "Update Progress", 0, 100, goal.progress,
                    key=f"prog_{goal.id}", label_visibility="collapsed",
                )
                if new_progress != goal.progress:
                    goal.progress = new_progress
                    goal.updated_at = datetime.utcnow()
                    if new_progress == 100:
                        goal.status = "Completed"
                        send_notification(
                            user_id, "Achievement",
                            f"🎉 Congratulations! You completed your goal: '{goal.title}'!",
                            session,
                        )
                    session.commit()
                    st.rerun()

            with col_complete:
                if st.button("✅ Complete", key=f"complete_{goal.id}"):
                    goal.status = "Completed"
                    goal.progress = 100
                    goal.updated_at = datetime.utcnow()
                    send_notification(
                        user_id, "Achievement",
                        f"🎉 Goal completed: '{goal.title}'!",
                        session,
                    )
                    session.commit()
                    st.rerun()

            with col_edit:
                if st.button("✏️ Edit", key=f"edit_{goal.id}"):
                    st.session_state[f"editing_goal_{goal.id}"] = True
                    st.rerun()

            with col_delete:
                if st.button("🗑️ Delete", key=f"delete_{goal.id}"):
                    session.delete(goal)
                    session.commit()
                    st.success(f"Goal '{goal.title}' deleted.")
                    st.rerun()

            # Edit form (shown when edit button is clicked)
            if st.session_state.get(f"editing_goal_{goal.id}", False):
                _render_edit_form(goal, session)
        else:
            # Non-active goals: only allow delete
            if st.button("🗑️ Delete", key=f"del_{goal.id}"):
                session.delete(goal)
                session.commit()
                st.rerun()


def _render_edit_form(goal, session) -> None:
    """Renders the inline edit form for a goal."""
    with st.form(f"edit_form_{goal.id}"):
        new_title = st.text_input("Title", value=goal.title)
        new_desc = st.text_area("Description", value=goal.description or "")
        new_deadline = st.text_input("Deadline (YYYY-MM-DD)", value=goal.deadline or "")

        col_save, col_cancel = st.columns(2)
        with col_save:
            if st.form_submit_button("💾 Save"):
                goal.title = new_title
                goal.description = new_desc if new_desc else None
                goal.deadline = new_deadline if new_deadline else None
                goal.updated_at = datetime.utcnow()
                session.commit()
                st.session_state[f"editing_goal_{goal.id}"] = False
                st.rerun()
        with col_cancel:
            if st.form_submit_button("❌ Cancel"):
                st.session_state[f"editing_goal_{goal.id}"] = False
                st.rerun()


def _render_create_goal(user_id: int) -> None:
    """Renders the create goal form."""
    st.subheader("➕ Create a New Goal")

    with st.form("create_goal_form"):
        title = st.text_input("Goal Title", placeholder="e.g., Learn Python in 30 days")
        description = st.text_area("Description (optional)", placeholder="Describe your goal...")
        deadline = st.date_input("Deadline (optional)")

        if st.form_submit_button("🚀 Create Goal", use_container_width=True):
            if not title.strip():
                st.error("Please enter a goal title.")
            else:
                try:
                    with db_session() as session:
                        new_goal = Goal(
                            user_id=user_id,
                            title=title.strip(),
                            description=description.strip() if description else None,
                            deadline=deadline.strftime("%Y-%m-%d") if deadline else None,
                        )
                        session.add(new_goal)

                    send_notification(
                        user_id, "Information",
                        f"🎯 New goal created: '{title.strip()}'. Stay focused and track your progress!",
                    )
                    st.success(f"Goal '{title.strip()}' created successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to create goal: {e}")


def _render_goal_analytics(user_id: int) -> None:
    """Renders goal analytics with Plotly charts."""
    with db_session() as session:
        goals = session.query(Goal).filter_by(user_id=user_id).all()

        if not goals:
            st.info("No goals to analyze yet.")
            return

        # Status distribution
        status_counts = {}
        for g in goals:
            status_counts[g.status] = status_counts.get(g.status, 0) + 1

        df_status = pd.DataFrame([
            {"Status": s, "Count": c} for s, c in status_counts.items()
        ])
        fig_status = px.pie(df_status, names="Status", values="Count",
                            title="Goal Status Distribution",
                            color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_status, width='stretch')

        # Active goals progress
        active = [g for g in goals if g.status == "Active"]
        if active:
            df_active = pd.DataFrame([
                {"Goal": g.title[:25], "Progress %": g.progress}
                for g in active
            ])
            fig_active = px.bar(df_active, x="Goal", y="Progress %",
                                title="Active Goals Progress",
                                range_y=[0, 100], color="Progress %",
                                color_continuous_scale="Viridis")
            st.plotly_chart(fig_active, width='stretch')
