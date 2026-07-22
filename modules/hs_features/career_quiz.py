"""
AI Career Quiz Module for TalentSphere Elevate — High School.

Provides a 28-question guided quiz covering 8 dimensions:
Interests, Personality, Logical Thinking, Creativity, Mathematics,
Communication, Technology, and Leadership.

Results: Career Match Score, Personality Type, Recommended Careers,
Confidence Level. Stored in the CareerQuizResult table.
"""

import streamlit as st
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from database import db_session, CareerQuizResult


# ──────────────────────────────────────────────────────────────────────────────
# Quiz Question Bank — 28 questions across 8 categories
# ──────────────────────────────────────────────────────────────────────────────

QUIZ_QUESTIONS: list[dict] = [
    # Interests (4)
    {"category": "Interests", "question": "Which activity excites you the most?",
     "options": ["Building a website or app", "Designing a poster or painting", "Organizing a community event", "Solving a science puzzle"],
     "weights": {"Technology": 3, "Arts": 0, "Leadership": 0, "STEM": 0}},
    {"category": "Interests", "question": "What would you spend a free Saturday doing?",
     "options": ["Learning a new programming language", "Reading about history or philosophy", "Volunteering at a local NGO", "Conducting a kitchen science experiment"],
     "weights": {"Technology": 3, "Arts": 0, "Leadership": 0, "STEM": 0}},
    {"category": "Interests", "question": "Which YouTube channel would you subscribe to first?",
     "options": ["Tech tutorials", "Art & design", "Motivational speakers", "Science experiments"],
     "weights": {"Technology": 3, "Arts": 0, "Leadership": 0, "STEM": 0}},
    {"category": "Interests", "question": "Which club would you join in school?",
     "options": ["Robotics Club", "Drama Club", "Student Council", "Science Olympiad"],
     "weights": {"Technology": 3, "Arts": 0, "Leadership": 0, "STEM": 0}},

    # Personality (3)
    {"category": "Personality", "question": "How do you prefer to work?",
     "options": ["Alone, focused on details", "In a creative team", "Leading a group", "Researching and experimenting"],
     "weights": {"Technology": 3, "Arts": 0, "Leadership": 0, "STEM": 0}},
    {"category": "Personality", "question": "When facing a tough problem, you:",
     "options": ["Break it into logical steps", "Think of creative alternatives", "Ask for team input", "Gather data and analyze"],
     "weights": {"Logical Thinking": 3, "Creativity": 0, "Communication": 0, "Mathematics": 0}},
    {"category": "Personality", "question": "What describes you best?",
     "options": ["Analytical and precise", "Imaginative and artistic", "Outgoing and persuasive", "Curious and experimental"],
     "weights": {"Logical Thinking": 3, "Creativity": 0, "Communication": 0, "STEM": 0}},

    # Logical Thinking (4)
    {"category": "Logical Thinking", "question": "If all roses are flowers and some flowers fade quickly, which is true?",
     "options": ["All roses fade quickly", "Some roses may fade quickly", "No roses fade", "Roses are not flowers"],
     "weights": {"correct": 1}},
    {"category": "Logical Thinking", "question": "What comes next: 2, 6, 12, 20, ?",
     "options": ["30", "28", "25", "32"],
     "weights": {"correct": 0}},
    {"category": "Logical Thinking", "question": "A bat and a ball cost $1.10. The bat costs $1 more than the ball. How much does the ball cost?",
     "options": ["$0.05", "$0.10", "$0.15", "$0.50"],
     "weights": {"correct": 0}},
    {"category": "Logical Thinking", "question": "Which shape completes the pattern: ◯ △ ◯ △ ◯ ?",
     "options": ["△", "◯", "◻", "◇"],
     "weights": {"correct": 0}},

    # Creativity (3)
    {"category": "Creativity", "question": "How many uses can you think of for a paperclip?",
     "options": ["1–3", "4–6", "7–10", "More than 10"],
     "weights": {"scale": True}},
    {"category": "Creativity", "question": "When given a blank canvas, you feel:",
     "options": ["Overwhelmed", "Slightly curious", "Excited to create", "Bursting with ideas"],
     "weights": {"scale": True}},
    {"category": "Creativity", "question": "You prefer projects that are:",
     "options": ["Strictly defined", "Somewhat flexible", "Open-ended", "Completely free-form"],
     "weights": {"scale": True}},

    # Mathematics (4)
    {"category": "Mathematics", "question": "How comfortable are you with algebra?",
     "options": ["Not at all", "Somewhat", "Comfortable", "Very comfortable"],
     "weights": {"scale": True}},
    {"category": "Mathematics", "question": "Which best describes your relationship with numbers?",
     "options": ["I avoid them", "I tolerate them", "I enjoy working with them", "I love solving math puzzles"],
     "weights": {"scale": True}},
    {"category": "Mathematics", "question": "What is 15% of 200?",
     "options": ["25", "30", "35", "40"],
     "weights": {"correct": 1}},
    {"category": "Mathematics", "question": "If x + 5 = 12, what is x?",
     "options": ["5", "6", "7", "8"],
     "weights": {"correct": 2}},

    # Communication (4)
    {"category": "Communication", "question": "How confident are you speaking in front of a class?",
     "options": ["Very nervous", "Slightly nervous", "Fairly confident", "Very confident"],
     "weights": {"scale": True}},
    {"category": "Communication", "question": "When writing an essay, you:",
     "options": ["Struggle to start", "Get the basics done", "Write clearly and concisely", "Enjoy crafting compelling arguments"],
     "weights": {"scale": True}},
    {"category": "Communication", "question": "In group discussions, you typically:",
     "options": ["Stay quiet", "Contribute occasionally", "Participate actively", "Often lead the discussion"],
     "weights": {"scale": True}},
    {"category": "Communication", "question": "How would you rate your listening skills?",
     "options": ["I often zone out", "Average", "Good — I remember key points", "Excellent — I capture nuances"],
     "weights": {"scale": True}},

    # Technology (3)
    {"category": "Technology", "question": "Have you ever written code or built something with technology?",
     "options": ["Never", "Tried once or twice", "Built a few small projects", "I code regularly"],
     "weights": {"scale": True}},
    {"category": "Technology", "question": "How interested are you in AI and Machine Learning?",
     "options": ["Not interested", "Slightly curious", "Interested", "Fascinated"],
     "weights": {"scale": True}},
    {"category": "Technology", "question": "Which tech topic excites you most?",
     "options": ["Web Development", "Artificial Intelligence", "Cybersecurity", "Game Development"],
     "weights": {"Technology": 3, "AI": 0, "Security": 0, "Gaming": 0}},

    # Leadership (3)
    {"category": "Leadership", "question": "Have you ever led a team or project?",
     "options": ["Never", "Once in school", "A few times", "Regularly"],
     "weights": {"scale": True}},
    {"category": "Leadership", "question": "How do you handle conflict in a group?",
     "options": ["I avoid it", "I compromise", "I mediate actively", "I find win-win solutions"],
     "weights": {"scale": True}},
    {"category": "Leadership", "question": "You prefer to:",
     "options": ["Follow clear instructions", "Collaborate equally", "Take initiative", "Define the vision and delegate"],
     "weights": {"scale": True}},
]

# Maps personality types to their descriptions and career matches
PERSONALITY_MAP: dict[str, dict] = {
    "The Analyst": {
        "traits": "Logical, detail-oriented, systematic",
        "careers": ["Data Scientist", "Software Engineer", "Cyber Security Analyst"],
    },
    "The Innovator": {
        "traits": "Creative, visionary, experimental",
        "careers": ["AI Engineer", "Game Developer", "UX Designer"],
    },
    "The Communicator": {
        "traits": "Expressive, empathetic, persuasive",
        "careers": ["Content Creator", "Marketing Manager", "Public Relations Specialist"],
    },
    "The Builder": {
        "traits": "Practical, hands-on, persistent",
        "careers": ["Web Developer", "Full-Stack Engineer", "DevOps Engineer"],
    },
    "The Leader": {
        "traits": "Decisive, strategic, inspiring",
        "careers": ["Product Manager", "Entrepreneur", "Management Consultant"],
    },
}


def _calculate_results(answers: list[int]) -> dict:
    """Calculates quiz results from the answer indices."""
    category_scores: dict[str, list[int]] = {
        "Interests": [], "Personality": [], "Logical Thinking": [],
        "Creativity": [], "Mathematics": [], "Communication": [],
        "Technology": [], "Leadership": [],
    }

    for i, answer_idx in enumerate(answers):
        q = QUIZ_QUESTIONS[i]
        cat = q["category"]
        weights = q["weights"]

        if "correct" in weights:
            # Objective question — binary score
            score = 100 if answer_idx == weights["correct"] else 0
        elif weights.get("scale"):
            # Likert-style scale — map 0-3 to 25-100
            score = (answer_idx + 1) * 25
        else:
            # First option scores highest for primary category
            score = (answer_idx + 1) * 25

        category_scores[cat].append(score)

    # Average each category
    avg_scores: dict[str, int] = {}
    for cat, scores in category_scores.items():
        avg_scores[cat] = int(sum(scores) / len(scores)) if scores else 0

    # Determine personality type
    top_cats = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)
    top_cat = top_cats[0][0]

    if top_cat in ("Logical Thinking", "Mathematics"):
        ptype = "The Analyst"
    elif top_cat in ("Creativity",):
        ptype = "The Innovator"
    elif top_cat in ("Communication",):
        ptype = "The Communicator"
    elif top_cat in ("Technology",):
        ptype = "The Builder"
    elif top_cat in ("Leadership",):
        ptype = "The Leader"
    else:
        # Interests or Personality — decide by second-highest
        if len(top_cats) > 1 and top_cats[1][0] in ("Technology", "Mathematics", "Logical Thinking"):
            ptype = "The Analyst"
        elif len(top_cats) > 1 and top_cats[1][0] in ("Creativity",):
            ptype = "The Innovator"
        else:
            ptype = "The Builder"

    personality_info = PERSONALITY_MAP[ptype]
    recommended_careers = personality_info["careers"]

    # Confidence level: how dominant the top category is
    all_vals = list(avg_scores.values())
    max_val = max(all_vals) if all_vals else 0
    mean_val = sum(all_vals) / len(all_vals) if all_vals else 0
    confidence = min(int(max_val * 0.6 + (max_val - mean_val) * 0.4), 100) if max_val > 0 else 50

    return {
        "scores": avg_scores,
        "personality_type": ptype,
        "personality_traits": personality_info["traits"],
        "recommended_careers": recommended_careers,
        "confidence_level": confidence,
    }


def render_career_quiz(user_id: int, ai_engine=None) -> None:
    """Renders the AI Career Quiz page."""
    st.header("🧠 Career Quiz")
    st.write("Answer 28 questions to discover your ideal career path, personality type, and personalized recommendations.")

    # ── Show Previous Results ──
    with db_session() as session:
        previous = (
            session.query(CareerQuizResult)
            .filter_by(user_id=user_id)
            .order_by(CareerQuizResult.completed_at.desc())
            .first()
        )
        if previous:
            _render_results(
                json.loads(previous.scores),
                previous.personality_type,
                json.loads(previous.recommended_careers),
                previous.confidence_level,
                ai_engine,
            )
            st.markdown("---")
            if not st.checkbox("🔄 Retake the quiz", key="retake_quiz"):
                return

    # ── Quiz Form ──
    st.subheader("📝 Career Discovery Quiz")
    st.info("Select the option that best describes you for each question.")

    answers: list[int] = []
    with st.form("career_quiz_form"):
        for i, q in enumerate(QUIZ_QUESTIONS):
            st.markdown(f"**Q{i + 1}. [{q['category']}]** {q['question']}")
            ans = st.radio(
                "Select one:", q["options"],
                key=f"quiz_q_{i}", index=0, horizontal=True, label_visibility="collapsed",
            )
            answers.append(q["options"].index(ans))
            if i < len(QUIZ_QUESTIONS) - 1:
                st.markdown("---")

        submitted = st.form_submit_button("🚀 Submit Quiz", use_container_width=True)

    if submitted:
        results = _calculate_results(answers)
        try:
            with db_session() as session:
                new_result = CareerQuizResult(
                    user_id=user_id,
                    scores=json.dumps(results["scores"]),
                    personality_type=results["personality_type"],
                    recommended_careers=json.dumps(results["recommended_careers"]),
                    confidence_level=results["confidence_level"],
                )
                session.add(new_result)
            st.success("Quiz completed! Your results are ready.")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to save quiz results: {e}")


def _render_results(
    scores: dict, personality_type: str,
    recommended_careers: list[str], confidence: int,
    ai_engine=None,
) -> None:
    """Renders quiz results with Pie Chart, Radar Chart, and Recommendation Cards."""
    st.subheader("📊 Your Career Quiz Results")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🧬 Personality Type", personality_type)
    with col2:
        st.metric("🎯 Confidence Level", f"{confidence}%")
    with col3:
        traits = PERSONALITY_MAP.get(personality_type, {}).get("traits", "")
        st.metric("✨ Traits", traits[:30])

    st.markdown("---")

    # ── Radar Chart ──
    col_radar, col_pie = st.columns(2)
    with col_radar:
        categories = list(scores.keys())
        values = list(scores.values())
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself', name='Your Profile',
            line=dict(color='#636EFA'),
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title="Skill Profile Radar",
            showlegend=False,
        )
        st.plotly_chart(fig_radar, width='stretch')

    # ── Pie Chart ──
    with col_pie:
        df_pie = pd.DataFrame({"Category": list(scores.keys()), "Score": list(scores.values())})
        fig_pie = px.pie(df_pie, names="Category", values="Score", title="Career Interest Distribution")
        st.plotly_chart(fig_pie, width='stretch')

    # ── Recommendation Cards ──
    st.subheader("🎯 Recommended Careers")
    cols = st.columns(min(len(recommended_careers), 3))
    for i, career in enumerate(recommended_careers):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### 🚀 {career}")
                if ai_engine:
                    recs = ai_engine.recommendation_engine.get_career_recommendations(career)
                    if recs.get("courses"):
                        st.markdown("**📚 Courses:** " + ", ".join(recs["courses"][:2]))
                    if recs.get("certifications"):
                        st.markdown("**📜 Certs:** " + ", ".join(recs["certifications"][:1]))
                else:
                    st.write("Complete your profile to get AI-powered recommendations.")
