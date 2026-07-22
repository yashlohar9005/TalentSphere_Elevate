"""
Interest Assessment Module for TalentSphere Elevate — High School.

Assesses student interests across 7 career streams: STEM, Arts, Commerce,
Healthcare, Design, Government, Entrepreneurship. Generates an Interest
Profile, Recommended Career Streams, and Skill Suggestions.

Integrates with the AI Engine's RecommendationEngine for tailored guidance.
"""

import streamlit as st
import json
import plotly.graph_objects as go
import pandas as pd
from database import db_session, InterestProfile


# ──────────────────────────────────────────────────────────────────────────────
# Assessment Questions — 3 per stream = 21 questions
# ──────────────────────────────────────────────────────────────────────────────

STREAMS: list[str] = [
    "STEM", "Arts", "Commerce", "Healthcare",
    "Design", "Government", "Entrepreneurship",
]

STREAM_QUESTIONS: dict[str, list[str]] = {
    "STEM": [
        "I enjoy conducting science experiments and analyzing data.",
        "I find mathematics and physics problems intellectually stimulating.",
        "I am curious about how machines, software, or natural systems work.",
    ],
    "Arts": [
        "I love expressing myself through music, writing, or visual art.",
        "I enjoy reading literature, watching films, or attending cultural events.",
        "I am drawn to creative storytelling and performance.",
    ],
    "Commerce": [
        "I am interested in how businesses operate and make money.",
        "I enjoy working with numbers, budgets, and financial planning.",
        "I like understanding market trends and consumer behavior.",
    ],
    "Healthcare": [
        "I care deeply about people's physical and mental well-being.",
        "I am interested in biology, anatomy, or medical sciences.",
        "I would enjoy a career helping patients or researching cures.",
    ],
    "Design": [
        "I have a strong eye for aesthetics, colors, and layout.",
        "I enjoy creating user interfaces, graphics, or physical products.",
        "I appreciate good architecture, fashion, or industrial design.",
    ],
    "Government": [
        "I am interested in public policy, law, or civil services.",
        "I want to contribute to societal change through governance.",
        "I enjoy debating current affairs and understanding regulations.",
    ],
    "Entrepreneurship": [
        "I enjoy coming up with new ideas for products or services.",
        "I am comfortable taking calculated risks.",
        "I aspire to build my own company or startup someday.",
    ],
}

# Career stream → suggested skills and career paths
STREAM_RECOMMENDATIONS: dict[str, dict] = {
    "STEM": {
        "careers": ["Software Engineer", "Data Scientist", "Mechanical Engineer", "Research Scientist"],
        "skills": ["Programming", "Critical Thinking", "Data Analysis", "Scientific Research"],
    },
    "Arts": {
        "careers": ["Content Creator", "Journalist", "Film Director", "Music Producer"],
        "skills": ["Creative Writing", "Visual Communication", "Storytelling", "Performing Arts"],
    },
    "Commerce": {
        "careers": ["Chartered Accountant", "Financial Analyst", "Marketing Manager", "Investment Banker"],
        "skills": ["Financial Literacy", "Analytical Skills", "Business Strategy", "Communication"],
    },
    "Healthcare": {
        "careers": ["Doctor", "Pharmacist", "Biomedical Researcher", "Public Health Specialist"],
        "skills": ["Biology", "Patient Communication", "Research Methodology", "Empathy"],
    },
    "Design": {
        "careers": ["UX Designer", "Graphic Designer", "Architect", "Fashion Designer"],
        "skills": ["Visual Design", "Prototyping", "User Research", "Adobe Creative Suite"],
    },
    "Government": {
        "careers": ["Civil Servant (IAS/IPS)", "Policy Analyst", "Lawyer", "Diplomat"],
        "skills": ["Current Affairs", "Legal Knowledge", "Essay Writing", "Public Speaking"],
    },
    "Entrepreneurship": {
        "careers": ["Startup Founder", "Product Manager", "Business Consultant", "Venture Capitalist"],
        "skills": ["Business Planning", "Leadership", "Marketing", "Financial Management"],
    },
}


def render_interest_assessment(user_id: int, ai_engine=None) -> None:
    """Renders the Interest Assessment page."""
    st.header("🎯 Interest Assessment")
    st.write("Discover which career streams align with your natural interests and passions.")

    # ── Show Previous Results ──
    with db_session() as session:
        previous = (
            session.query(InterestProfile)
            .filter_by(user_id=user_id)
            .order_by(InterestProfile.completed_at.desc())
            .first()
        )
        if previous:
            _render_profile(
                json.loads(previous.scores),
                json.loads(previous.recommended_streams),
                json.loads(previous.skill_suggestions),
                ai_engine,
            )
            st.markdown("---")
            if not st.checkbox("🔄 Retake the assessment", key="retake_interest"):
                return

    # ── Assessment Form ──
    st.subheader("📝 Rate Each Statement")
    st.info("Rate how much you agree with each statement on a scale of 1 (Strongly Disagree) to 10 (Strongly Agree).")

    responses: dict[str, list[int]] = {stream: [] for stream in STREAMS}

    with st.form("interest_assessment_form"):
        for stream in STREAMS:
            st.markdown(f"#### 📂 {stream}")
            for j, question in enumerate(STREAM_QUESTIONS[stream]):
                val = st.slider(question, 1, 10, 5, key=f"interest_{stream}_{j}")
                responses[stream].append(val)
            st.markdown("---")

        submitted = st.form_submit_button("🚀 Submit Assessment", use_container_width=True)

    if submitted:
        # Calculate average score per stream (out of 100)
        scores: dict[str, int] = {}
        for stream, vals in responses.items():
            scores[stream] = int(sum(vals) / len(vals) * 10)

        # Top 3 streams
        sorted_streams = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        recommended = [s[0] for s in sorted_streams[:3]]

        # Skill suggestions from top streams
        skill_suggestions: list[str] = []
        for stream in recommended:
            skill_suggestions.extend(STREAM_RECOMMENDATIONS[stream]["skills"][:2])

        try:
            with db_session() as session:
                profile = InterestProfile(
                    user_id=user_id,
                    scores=json.dumps(scores),
                    recommended_streams=json.dumps(recommended),
                    skill_suggestions=json.dumps(skill_suggestions),
                )
                session.add(profile)
            st.success("Interest Assessment completed!")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to save assessment: {e}")


def _render_profile(
    scores: dict, recommended_streams: list[str],
    skill_suggestions: list[str], ai_engine=None,
) -> None:
    """Renders the interest profile with radar chart and recommendations."""
    st.subheader("📊 Your Interest Profile")

    # ── Radar Chart ──
    categories = list(scores.keys())
    values = list(scores.values())
    fig = go.Figure(data=go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself', name='Interest Profile',
        line=dict(color='#00CC96'),
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title="Interest Profile Across Career Streams",
        showlegend=False,
    )
    st.plotly_chart(fig, width='stretch')

    # ── Top Streams ──
    st.subheader("🏆 Top Recommended Streams")
    cols = st.columns(min(len(recommended_streams), 3))
    for i, stream in enumerate(recommended_streams):
        with cols[i]:
            rec = STREAM_RECOMMENDATIONS.get(stream, {})
            with st.container(border=True):
                st.markdown(f"### 🎯 {stream}")
                st.metric("Score", f"{scores.get(stream, 0)}%")
                st.markdown("**Careers:** " + ", ".join(rec.get("careers", [])[:3]))
                st.markdown("**Skills:** " + ", ".join(rec.get("skills", [])[:3]))

    # ── Skill Suggestions ──
    st.subheader("💡 Suggested Skills to Develop")
    unique_skills = list(dict.fromkeys(skill_suggestions))  # deduplicate preserving order
    for skill in unique_skills:
        st.markdown(f"- ✅ {skill}")

    # ── AI Recommendations ──
    if ai_engine and recommended_streams:
        st.subheader("🤖 AI-Powered Insights")
        top_stream = recommended_streams[0]
        recs = ai_engine.recommendation_engine.generate_recommendations(
            "high_school",
            top_stream if top_stream == "STEM" else "Arts & Humanities",
            scores,
        )
        if recs.get("courses"):
            st.write("**Recommended Courses:** " + ", ".join(recs["courses"]))
        if recs.get("career_suggestions"):
            st.write("**Career Suggestions:** " + ", ".join(recs["career_suggestions"]))
