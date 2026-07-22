"""
Career Explorer Module for TalentSphere Elevate.

Renders the Career Explorer page with search, filter, career cards,
detail views, and the "Add to Goal" workflow. Reuses existing AI
recommendation and roadmap services — no logic duplication.
"""

import streamlit as st
from database import db_session, CareerGoal
from modules.career_data import CAREER_CATALOG, CAREER_CATEGORIES
from notifications.notification_service import send_notification


def _filter_careers(search_query: str, category_filter: str) -> list[dict]:
    """Filters the career catalog by search query and category."""
    results = CAREER_CATALOG

    if category_filter and category_filter != "All":
        results = [c for c in results if c["category"] == category_filter]

    if search_query:
        query_lower = search_query.lower()
        results = [
            c for c in results
            if query_lower in c["name"].lower()
            or query_lower in c["description"].lower()
            or any(query_lower in skill.lower() for skill in c["required_skills"])
        ]

    return results


def _get_user_goals(user_id: int, session) -> set[str]:
    """Returns the set of career names the user has already added as goals."""
    goals = session.query(CareerGoal).filter_by(user_id=user_id).all()
    return {g.career_name for g in goals}


def _render_career_card(career: dict, user_id: int, ai_engine, existing_goals: set, portal) -> None:
    """Renders a single career card with View Details and Add to Goal actions."""
    with st.container(border=True):
        st.markdown(f"### {career['icon']} {career['name']}")
        st.caption(f"📂 {career['category']}")
        st.write(career["description"][:150] + "..." if len(career["description"]) > 150 else career["description"])

        # Skill tags
        skills_display = " · ".join(career["required_skills"][:3])
        st.markdown(f"**Key Skills:** {skills_display}")

        # Career outlook snippet
        st.markdown(f"📈 *{career['career_outlook'][:80]}...*")

        col_detail, col_goal = st.columns(2)

        # --- View Details ---
        with col_detail:
            detail_key = f"detail_{career['name'].replace(' ', '_')}_{user_id}"
            if st.button("🔍 View Details", key=detail_key, use_container_width=True):
                st.session_state["selected_career_for_details"] = career["name"]
                st.rerun()

        # --- Add to Goal ---
        with col_goal:
            goal_key = f"goal_{career['name'].replace(' ', '_')}_{user_id}"
            already_added = career["name"] in existing_goals

            if already_added:
                st.button("✅ Goal Added", key=goal_key, disabled=True, use_container_width=True)
            else:
                if st.button("🎯 Add to Goal", key=goal_key, use_container_width=True):
                    _add_career_goal(career, user_id, ai_engine, portal)


def _render_career_details_page(career: dict, user_id: int, ai_engine, portal) -> None:
    """Renders the comprehensive full-page career details view."""
    
    # Back button at top
    if st.button("⬅ Back to Career Explorer", key="back_top"):
        st.session_state["selected_career_for_details"] = None
        st.rerun()
        
    st.markdown("---")
    
    # ----------------------------------------------------
    # Header
    # ----------------------------------------------------
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"<h1 style='text-align: center; font-size: 4rem;'>{career['icon']}</h1>", unsafe_allow_html=True)
    with col2:
        st.title(career['name'])
        st.subheader(career['category'])
        st.markdown(f"*{career['career_outlook'][:80]}...*")

    st.markdown("---")
    
    # ----------------------------------------------------
    # About Career
    # ----------------------------------------------------
    st.header("About Career")
    st.write(career["description"])
    
    col_what, col_where = st.columns(2)
    with col_what:
        st.markdown("**What this career does:**")
        st.write(f"Professionals in this role typically design, implement, and maintain solutions relevant to {career['category']}. They collaborate with cross-functional teams to solve complex real-world problems.")
    with col_where:
        st.markdown("**Where professionals work:**")
        st.write(f"Commonly employed in Tech companies, Startups, Financial Institutions, and specialized {career['category']} firms.")

    st.markdown("---")
    
    # ----------------------------------------------------
    # Skills Required
    # ----------------------------------------------------
    st.header("Skills Required")
    col_tech, col_soft, col_tools = st.columns(3)
    
    with col_tech:
        st.markdown("**Technical Skills**")
        for skill in career["required_skills"][:3]:
            st.markdown(f"- {skill}")
            
    with col_soft:
        st.markdown("**Soft Skills**")
        st.markdown("- Problem Solving\n- Communication\n- Teamwork\n- Critical Thinking")
        
    with col_tools:
        st.markdown("**Tools & Frameworks**")
        st.markdown("- Git / GitHub\n- Agile / Jira\n- VS Code / IDEs\n- Cloud Platforms (AWS/GCP)")
        
    st.markdown("---")
    
    # ----------------------------------------------------
    # Education Roadmap
    # ----------------------------------------------------
    st.header("Education Roadmap")
    st.info(career["education_path"])
    with st.expander("Detailed Education Steps"):
        st.markdown("""
        - **After 10th:** Focus on Mathematics and Science streams.
        - **After 12th:** Pursue a relevant degree or diploma.
        - **Diploma:** Specialized vocational training (optional).
        - **Bachelor Degree:** B.Sc / B.Tech / B.E. in a related field.
        - **Master Degree:** Optional, for specialization or research.
        - **Certifications:** Continuous learning to stay updated.
        """)

    st.markdown("---")
    
    # ----------------------------------------------------
    # Learning Roadmap
    # ----------------------------------------------------
    st.header("Learning Roadmap")
    lr_col1, lr_col2, lr_col3 = st.columns(3)
    with lr_col1:
        st.markdown("**Beginner**")
        for proj in career["beginner_projects"]:
            st.markdown(f"- {proj}")
    with lr_col2:
        st.markdown("**Intermediate**")
        st.markdown("- Advanced algorithms\n- Database integration\n- API Development\n- Cloud basics")
    with lr_col3:
        st.markdown("**Advanced**")
        st.markdown("- System architecture\n- Performance optimization\n- Security best practices\n- Mentorship")
        
    st.markdown("---")
    
    # ----------------------------------------------------
    # Future Scope
    # ----------------------------------------------------
    st.header("Future Scope")
    fs_col1, fs_col2, fs_col3 = st.columns(3)
    with fs_col1:
        st.metric("Industry Growth", "15-25%", "High Demand")
    with fs_col2:
        # Simple extraction of salary if available
        salary_text = "$100,000+"
        if "Median salary" in career["career_outlook"]:
            try:
                salary_text = career["career_outlook"].split("Median salary")[1].split(".")[0].strip()
            except Exception:
                pass
        st.metric("Salary Trend", salary_text)
    with fs_col3:
        st.metric("Career Opportunities", "Global", "Remote Available")
        
    st.markdown("---")
    
    # ----------------------------------------------------
    # Recommended Courses & Certifications
    # ----------------------------------------------------
    st.header("Recommendations")
    rec_col1, rec_col2 = st.columns(2)
    with rec_col1:
        st.subheader("📚 Recommended Courses")
        for course in career["suggested_courses"]:
            with st.container(border=True):
                st.markdown(f"**{course}**")
                
    with rec_col2:
        st.subheader("📜 Recommended Certifications")
        certs = ["Google Professional Certificate", "Microsoft Fundamentals", "Coursera Specialization"]
        for cert in certs:
            with st.container(border=True):
                st.markdown(f"**{cert}**")

    # Add AI Recommendations if available
    if ai_engine:
        st.markdown("**🤖 AI-Powered Insights**")
        recs = ai_engine.recommendation_engine.get_career_recommendations(career["name"])
        if recs.get("courses"):
            st.write("**Additional Courses:** " + ", ".join(recs["courses"]))
        if recs.get("projects"):
            st.write("**Additional Projects:** " + ", ".join(recs["projects"]))
        if recs.get("certifications"):
            st.write("**More Certifications:** " + ", ".join(recs["certifications"]))

    st.markdown("---")
    
    # ----------------------------------------------------
    # Related Careers
    # ----------------------------------------------------
    st.header("Related Careers")
    related = [c for c in CAREER_CATALOG if c["category"] == career["category"] and c["name"] != career["name"]]
    if related:
        rel_cols = st.columns(min(len(related), 3))
        for i, rel_c in enumerate(related[:3]):
            with rel_cols[i]:
                with st.container(border=True):
                    st.markdown(f"**{rel_c['icon']} {rel_c['name']}**")
                    if st.button("View Details", key=f"rel_{rel_c['name']}"):
                        st.session_state["selected_career_for_details"] = rel_c["name"]
                        st.rerun()
    else:
        st.info("No highly related careers found in the current catalog.")

    st.markdown("---")
    
    # ----------------------------------------------------
    # Resources (Videos, Books)
    # ----------------------------------------------------
    st.header("Resources")
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.markdown("**📺 Recommended Videos**")
        st.markdown(f"- [Day in the life of a {career['name']}](https://youtube.com/)")
        st.markdown(f"- [How to become a {career['name']} in 2024](https://youtube.com/)")
        st.markdown(f"- [Top Skills for {career['name']}](https://youtube.com/)")
    with res_col2:
        st.markdown("**📖 Recommended Books**")
        st.markdown("- *The Pragmatic Programmer*")
        st.markdown("- *Clean Code*")
        st.markdown("- *Cracking the Coding Interview*")
        
    st.markdown("---")
    
    # ----------------------------------------------------
    # Career Tips
    # ----------------------------------------------------
    st.header("Career Tips")
    with st.container(border=True):
        st.markdown("**💡 Interview Tips:** Focus on demonstrating problem-solving ability rather than just memorizing syntax.")
        st.markdown("**🎯 Preparation Tips:** Build a strong portfolio of projects that solve real-world problems.")
        st.markdown("**⚠️ Common Mistakes:** Neglecting soft skills like communication and teamwork.")

    st.markdown("---")
    
    # ----------------------------------------------------
    # Bottom Actions
    # ----------------------------------------------------
    st.subheader("Take Action")
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("⬅ Back to Career Explorer", key="back_bottom", use_container_width=True):
            st.session_state["selected_career_for_details"] = None
            st.rerun()
            
    with db_session() as session:
        existing_goals = _get_user_goals(user_id, session)
        
    already_added = career["name"] in existing_goals
    
    with action_col2:
        if already_added:
            st.button("✅ Goal Added", key="add_goal_bottom", disabled=True, use_container_width=True)
        else:
            if st.button("🎯 Add Career Goal", key="add_goal_bottom", use_container_width=True):
                _add_career_goal(career, user_id, ai_engine, portal)
                
    with action_col3:
        if already_added:
            st.button("✅ Roadmap Generated", key="gen_roadmap_bottom", disabled=True, use_container_width=True)
        else:
            if st.button("📚 Generate Learning Roadmap", key="gen_roadmap_bottom", use_container_width=True):
                _add_career_goal(career, user_id, ai_engine, portal)


def _add_career_goal(career: dict, user_id: int, ai_engine, portal) -> None:
    """
    Handles the full 'Add to Goal' workflow:
    1. Save CareerGoal to database.
    2. Generate a career-specific roadmap via the existing roadmap generator.
    3. Send a success notification to the user's inbox.
    4. Display a success message.
    """
    try:
        with db_session() as session:
            # Check for duplicates (defensive — button should already be disabled)
            existing = session.query(CareerGoal).filter_by(
                user_id=user_id, career_name=career["name"]
            ).first()
            if existing:
                st.info(f"'{career['name']}' is already in your career goals!")
                return

            # Step 1: Save career goal
            new_goal = CareerGoal(
                user_id=user_id,
                career_name=career["name"],
                category=career["category"],
            )
            session.add(new_goal)

        # Step 2: Generate roadmap using the existing roadmap generator service
        if ai_engine:
            roadmap_data = ai_engine.roadmap_generator.generate_career_roadmap(career["name"])
        else:
            # Fallback if AI engine is unavailable
            roadmap_data = {
                "title": f"{career['name']} Career Pathway",
                "flat_steps": [
                    "[30-Day Plan] Research the field and key skills",
                    "[30-Day Plan] Start an introductory course",
                    "[60-Day Plan] Complete a beginner project",
                    "[90-Day Plan] Build a portfolio-worthy project",
                ],
            }

        # Step 3: Save roadmap via BasePortal's generate_roadmap (reuse, no duplication)
        portal.generate_roadmap(
            title=roadmap_data["title"],
            steps=roadmap_data["flat_steps"],
            description=f"Career pathway roadmap for {career['name']}.",
        )

        # Step 4: Send notification via existing notification service
        send_notification(
            user_id=user_id,
            notif_type="Achievement",
            message=f"🎯 You added '{career['name']}' as a career goal! "
                    f"A personalized roadmap has been generated for you.",
        )

        st.success(
            f"🎉 '{career['name']}' has been added to your career goals! "
            f"A personalized roadmap has been generated — check the "
            f"'Roadmap & Progress' tab to start your journey."
        )
        st.rerun()

    except Exception as e:
        st.error(f"Failed to add career goal: {e}")


def _render_my_goals(user_id: int) -> None:
    """Renders the user's saved career goals section."""
    st.markdown("---")
    st.subheader("🎯 My Career Goals")

    with db_session() as session:
        goals = session.query(CareerGoal).filter_by(user_id=user_id).order_by(
            CareerGoal.added_at.desc()
        ).all()

        if not goals:
            st.info("You haven't added any career goals yet. Explore the careers above and click 'Add to Goal' to get started!")
            return

        cols = st.columns(min(len(goals), 4))
        for i, goal in enumerate(goals):
            with cols[i % 4]:
                with st.container(border=True):
                    # Find the icon from the catalog
                    career_entry = next(
                        (c for c in CAREER_CATALOG if c["name"] == goal.career_name),
                        None,
                    )
                    icon = career_entry["icon"] if career_entry else "🎯"
                    st.markdown(f"### {icon} {goal.career_name}")
                    st.caption(f"📂 {goal.category}")
                    st.caption(f"📅 Added: {goal.added_at.strftime('%b %d, %Y')}")


def render_career_explorer(user_id: int, ai_engine, portal) -> None:
    """
    Main entry point for the Career Explorer page.
    Called by BasePortal.run() when the user navigates to 'Career Explorer'.
    """
    
    # Check if a career is selected for detailed view
    selected_career_name = st.session_state.get("selected_career_for_details")
    if selected_career_name:
        # Find the career object
        career_obj = next((c for c in CAREER_CATALOG if c["name"] == selected_career_name), None)
        if career_obj:
            _render_career_details_page(career_obj, user_id, ai_engine, portal)
            return
        else:
            # Clear invalid state
            st.session_state["selected_career_for_details"] = None

    st.header("🧭 Career Explorer")
    st.write("Discover exciting career paths, explore what each role involves, and set career goals with personalized learning roadmaps.")

    # --- Search & Filter Bar ---
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search_query = st.text_input(
            "🔍 Search careers",
            placeholder="Search by career name, description, or skill...",
            key="career_search",
        )
    with col_filter:
        category_filter = st.selectbox(
            "📂 Filter by Category",
            options=CAREER_CATEGORIES,
            key="career_category_filter",
        )

    # --- Filter Careers ---
    filtered_careers = _filter_careers(search_query, category_filter)

    if not filtered_careers:
        st.warning("No careers found matching your search. Try a different keyword or category.")
        return

    st.caption(f"Showing {len(filtered_careers)} career(s)")

    # --- Fetch existing goals once for all cards ---
    with db_session() as session:
        existing_goals = _get_user_goals(user_id, session)

    # --- Career Cards Grid (3 columns) ---
    cols = st.columns(3)
    for i, career in enumerate(filtered_careers):
        with cols[i % 3]:
            _render_career_card(career, user_id, ai_engine, existing_goals, portal)

    # --- My Career Goals Section ---
    _render_my_goals(user_id)
