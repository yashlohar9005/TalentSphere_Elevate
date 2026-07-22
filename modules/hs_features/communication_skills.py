"""
Communication Skills Module for TalentSphere Elevate — High School.

Topics: Public Speaking, Interview Communication, Email Writing,
Presentation Skills, Listening Skills, Body Language, Vocabulary Builder,
Grammar Practice, Mini Exercises. Progress tracked per topic.
"""

import streamlit as st
import json
from datetime import datetime
from database import db_session, CommunicationProgress


# ──────────────────────────────────────────────────────────────────────────────
# Communication Topics with lessons and exercises
# ──────────────────────────────────────────────────────────────────────────────

COMM_TOPICS: list[dict] = [
    {
        "name": "Public Speaking",
        "icon": "🎤",
        "lesson": (
            "Public speaking is the art of effectively communicating ideas to an audience.\n\n"
            "**Key Principles:**\n"
            "1. **Know your audience** — Tailor your message to who is listening\n"
            "2. **Structure your speech** — Introduction, body, conclusion\n"
            "3. **Practice, practice, practice** — Rehearse out loud multiple times\n"
            "4. **Use eye contact** — Connect with different sections of the audience\n"
            "5. **Control your pace** — Speak slowly and clearly, use pauses for emphasis\n\n"
            "**Tips for Overcoming Stage Fright:**\n"
            "- Deep breathing before you start\n"
            "- Visualize success\n"
            "- Focus on the message, not yourself\n"
            "- Start with a familiar topic\n"
        ),
        "exercise": {
            "type": "reflection",
            "prompt": "Prepare a 2-minute speech on 'Why learning new skills is important'. Write your key points below:",
            "tips": ["Start with a hook", "Use 3 main points", "End with a call to action"],
        },
    },
    {
        "name": "Interview Communication",
        "icon": "💼",
        "lesson": (
            "Interview communication is about presenting yourself confidently and clearly.\n\n"
            "**STAR Method for answering behavioral questions:**\n"
            "- **S**ituation — Set the context\n"
            "- **T**ask — Describe your responsibility\n"
            "- **A**ction — Explain what you did\n"
            "- **R**esult — Share the outcome\n\n"
            "**Common Mistakes:**\n"
            "- Speaking too fast or too slowly\n"
            "- Not listening to the question fully\n"
            "- Using filler words (um, uh, like)\n"
            "- Negative body language\n"
        ),
        "exercise": {
            "type": "reflection",
            "prompt": "Using the STAR method, answer: 'Tell me about a time you worked in a team.'",
            "tips": ["Be specific", "Quantify results if possible", "Keep it under 2 minutes"],
        },
    },
    {
        "name": "Email Writing",
        "icon": "📧",
        "lesson": (
            "Professional email writing is essential for academic and career success.\n\n"
            "**Email Structure:**\n"
            "1. **Subject Line** — Clear and specific\n"
            "2. **Greeting** — Formal: 'Dear Mr./Ms.' or 'Hello [Name]'\n"
            "3. **Body** — Concise, one topic per email, clear action items\n"
            "4. **Closing** — 'Best regards', 'Thank you', 'Sincerely'\n"
            "5. **Signature** — Name, title/role, contact info\n\n"
            "**Do's and Don'ts:**\n"
            "- ✅ Proofread before sending\n"
            "- ✅ Use proper grammar and punctuation\n"
            "- ❌ Don't use slang or emojis in formal emails\n"
            "- ❌ Don't write walls of text — use paragraphs\n"
        ),
        "exercise": {
            "type": "reflection",
            "prompt": "Write a formal email to a teacher requesting a recommendation letter for a scholarship application:",
            "tips": ["Include a clear subject line", "State your purpose early", "Thank them for their time"],
        },
    },
    {
        "name": "Presentation Skills",
        "icon": "📊",
        "lesson": (
            "Great presentations combine clear content with engaging delivery.\n\n"
            "**The 10-20-30 Rule (Guy Kawasaki):**\n"
            "- **10** slides maximum\n"
            "- **20** minutes duration\n"
            "- **30** point minimum font size\n\n"
            "**Slide Design Tips:**\n"
            "- One key idea per slide\n"
            "- Use visuals (charts, images) over text\n"
            "- Maintain consistent formatting\n"
            "- Use contrast for readability\n\n"
            "**Delivery Tips:**\n"
            "- Don't read from slides — know your content\n"
            "- Engage with questions or polls\n"
            "- Use hand gestures naturally\n"
        ),
        "exercise": {
            "type": "reflection",
            "prompt": "Plan a 5-slide presentation on 'The Future of AI'. Write the title and key point for each slide:",
            "tips": ["Slide 1: Hook/Title", "Slides 2-4: Main points", "Slide 5: Conclusion/CTA"],
        },
    },
    {
        "name": "Listening Skills",
        "icon": "👂",
        "lesson": (
            "Active listening is one of the most important communication skills.\n\n"
            "**Active Listening Techniques:**\n"
            "1. **Pay full attention** — Put away distractions\n"
            "2. **Show you're listening** — Nod, make eye contact\n"
            "3. **Provide feedback** — Paraphrase: 'So what you're saying is...'\n"
            "4. **Defer judgment** — Don't interrupt or jump to conclusions\n"
            "5. **Respond appropriately** — Be honest and respectful\n\n"
            "**Barriers to Listening:**\n"
            "- Multitasking\n"
            "- Preconceived notions\n"
            "- Emotional reactions\n"
            "- Environmental noise\n"
        ),
        "exercise": {
            "type": "reflection",
            "prompt": "Listen to a 5-minute podcast or TED talk and summarize the 3 main points below:",
            "tips": ["Focus on key themes, not details", "Note the speaker's conclusion", "Write in your own words"],
        },
    },
    {
        "name": "Body Language",
        "icon": "🧍",
        "lesson": (
            "Over 55% of communication is non-verbal. Your body speaks before you do.\n\n"
            "**Positive Body Language:**\n"
            "- ✅ Open posture (uncrossed arms)\n"
            "- ✅ Appropriate eye contact (60-70% of time)\n"
            "- ✅ Genuine smile\n"
            "- ✅ Firm handshake\n"
            "- ✅ Leaning slightly forward (shows interest)\n\n"
            "**Negative Body Language:**\n"
            "- ❌ Crossed arms (defensive)\n"
            "- ❌ Avoiding eye contact (lack of confidence)\n"
            "- ❌ Fidgeting (nervousness)\n"
            "- ❌ Slouching (disinterest)\n"
        ),
        "exercise": {
            "type": "quiz",
            "questions": [
                {"q": "Crossing arms during a conversation signals:", "options": ["Confidence", "Defensiveness", "Agreement", "Excitement"], "answer": 1},
                {"q": "How much eye contact is ideal in a conversation?", "options": ["100%", "0%", "60-70%", "10%"], "answer": 2},
                {"q": "Leaning slightly forward shows:", "options": ["Boredom", "Interest", "Aggression", "Fear"], "answer": 1},
            ],
        },
    },
    {
        "name": "Vocabulary Builder",
        "icon": "📚",
        "lesson": (
            "A strong vocabulary helps you express ideas precisely and persuasively.\n\n"
            "**Word of the Week Strategy:**\n"
            "Learn one new word daily and use it in 3 sentences.\n\n"
            "**Power Words for Communication:**\n"
            "| Word | Meaning | Usage |\n"
            "|------|---------|-------|\n"
            "| Articulate | Express clearly | 'She articulated her vision well.' |\n"
            "| Collaborate | Work together | 'Let's collaborate on this project.' |\n"
            "| Innovative | New and creative | 'The solution was innovative.' |\n"
            "| Resilient | Recover quickly | 'She remained resilient under pressure.' |\n"
            "| Empathetic | Understanding others | 'An empathetic leader listens first.' |\n"
        ),
        "exercise": {
            "type": "quiz",
            "questions": [
                {"q": "'Articulate' means to:", "options": ["Confuse", "Express clearly", "Mumble", "Debate"], "answer": 1},
                {"q": "A 'resilient' person:", "options": ["Gives up easily", "Recovers from setbacks", "Avoids challenges", "Is always happy"], "answer": 1},
                {"q": "'Collaborate' means to:", "options": ["Compete", "Work alone", "Work together", "Criticize"], "answer": 2},
            ],
        },
    },
    {
        "name": "Grammar Practice",
        "icon": "✏️",
        "lesson": (
            "Good grammar is the foundation of clear communication.\n\n"
            "**Common Grammar Rules:**\n"
            "1. **Subject-Verb Agreement** — Singular subjects take singular verbs\n"
            "2. **Tense Consistency** — Don't switch tenses mid-paragraph\n"
            "3. **Pronoun Reference** — Make sure pronouns clearly refer to a noun\n"
            "4. **Active vs Passive Voice** — Prefer active voice for clarity\n"
            "5. **Comma Usage** — Before conjunctions in compound sentences, after introductory clauses\n\n"
            "**Examples:**\n"
            "- ❌ 'The team are working hard.' → ✅ 'The team is working hard.'\n"
            "- ❌ 'Me and him went.' → ✅ 'He and I went.'\n"
        ),
        "exercise": {
            "type": "quiz",
            "questions": [
                {"q": "Which is correct?", "options": ["The team are ready", "The team is ready", "The team be ready", "The team were ready"], "answer": 1},
                {"q": "Choose the active voice:", "options": ["The cake was eaten by me", "I ate the cake", "The cake is being eaten", "The eating was done"], "answer": 1},
                {"q": "'Each student ___ their homework.'", "options": ["do", "does", "done", "doing"], "answer": 1},
            ],
        },
    },
    {
        "name": "Mini Exercises",
        "icon": "🏋️",
        "lesson": (
            "Practice makes perfect! Here are quick daily exercises to boost your communication.\n\n"
            "**Daily Exercises:**\n"
            "1. 🗣️ **Mirror Speech** — Practice speaking in front of a mirror for 2 minutes\n"
            "2. ✍️ **Journal Entry** — Write 200 words about your day\n"
            "3. 📖 **Read Aloud** — Read a paragraph from a book out loud\n"
            "4. 🎧 **Podcast Summary** — Listen to a podcast and summarize in 3 sentences\n"
            "5. 💬 **Conversation Starter** — Start a meaningful conversation with someone new\n\n"
            "**Weekly Challenge:**\n"
            "Pick one exercise and do it every day for a week. Track your progress!\n"
        ),
        "exercise": {
            "type": "reflection",
            "prompt": "Choose one exercise above and write about your experience doing it today:",
            "tips": ["Be specific about what you did", "Note what was easy/hard", "Set a goal for tomorrow"],
        },
    },
]


def render_communication_skills(user_id: int) -> None:
    """Renders the Communication Skills page."""
    st.header("🗣️ Communication Skills")
    st.write("Master essential communication skills for career success.")

    # ── Load progress ──
    with db_session() as session:
        progress_records = session.query(CommunicationProgress).filter_by(user_id=user_id).all()
        progress_map: dict[str, dict] = {}
        for p in progress_records:
            progress_map[p.topic] = {
                "lesson_completed": p.lesson_completed,
                "exercise_score": p.exercise_score,
            }

    # ── Overall Progress ──
    total = len(COMM_TOPICS)
    completed = sum(1 for t in COMM_TOPICS if progress_map.get(t["name"], {}).get("lesson_completed", 0))
    exercises_done = sum(1 for t in COMM_TOPICS if progress_map.get(t["name"], {}).get("exercise_score") is not None)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Lessons Completed", f"{completed}/{total}")
    with col2:
        st.metric("Exercises Done", f"{exercises_done}/{total}")
    with col3:
        pct = int((completed + exercises_done) / (total * 2) * 100) if total > 0 else 0
        st.metric("Overall Progress", f"{pct}%")

    st.progress(pct / 100)
    st.markdown("---")

    # ── Topic Cards ──
    for i, topic in enumerate(COMM_TOPICS):
        tp = progress_map.get(topic["name"], {})
        lesson_done = tp.get("lesson_completed", 0)
        exercise_done = tp.get("exercise_score") is not None

        status = "✅" if lesson_done and exercise_done else "📖"
        with st.expander(f"{status} {topic['icon']} {topic['name']}", expanded=(i == 0 and not lesson_done)):
            tab_lesson, tab_exercise = st.tabs(["📖 Lesson", "🏋️ Exercise"])

            with tab_lesson:
                st.markdown(topic["lesson"])

                if not lesson_done:
                    if st.button(f"✅ Mark Lesson Complete", key=f"comm_lesson_{topic['name']}"):
                        with db_session() as session:
                            existing = session.query(CommunicationProgress).filter_by(
                                user_id=user_id, topic=topic["name"],
                            ).first()
                            if existing:
                                existing.lesson_completed = 1
                                existing.completed_at = datetime.utcnow()
                            else:
                                session.add(CommunicationProgress(
                                    user_id=user_id, topic=topic["name"],
                                    lesson_completed=1, completed_at=datetime.utcnow(),
                                ))
                        st.rerun()
                else:
                    st.success("Lesson completed! ✅")

            with tab_exercise:
                if not lesson_done:
                    st.info("Complete the lesson first to unlock the exercise.")
                elif exercise_done:
                    st.success(f"Exercise completed! Score: {tp.get('exercise_score', 0)}%")
                else:
                    _render_exercise(user_id, topic)


def _render_exercise(user_id: int, topic: dict) -> None:
    """Renders the exercise for a topic."""
    exercise = topic["exercise"]

    if exercise["type"] == "reflection":
        st.markdown(f"**📝 Exercise:** {exercise['prompt']}")
        for tip in exercise.get("tips", []):
            st.markdown(f"  💡 {tip}")

        response = st.text_area(
            "Your response:", key=f"comm_ex_{topic['name']}",
            height=150, placeholder="Write your response here...",
        )

        if st.button("✅ Submit Exercise", key=f"comm_submit_{topic['name']}"):
            if len(response.strip()) < 20:
                st.warning("Please write at least 20 characters.")
            else:
                # Score based on response length and quality heuristics
                word_count = len(response.split())
                score = min(int(word_count / 50 * 100), 100)  # More words = higher score (capped)
                score = max(score, 60)  # Minimum 60 for submitting

                with db_session() as session:
                    existing = session.query(CommunicationProgress).filter_by(
                        user_id=user_id, topic=topic["name"],
                    ).first()
                    if existing:
                        existing.exercise_score = score
                        existing.completed_at = datetime.utcnow()
                    else:
                        session.add(CommunicationProgress(
                            user_id=user_id, topic=topic["name"],
                            lesson_completed=1, exercise_score=score,
                            completed_at=datetime.utcnow(),
                        ))
                st.success(f"Exercise submitted! Score: {score}%")
                st.rerun()

    elif exercise["type"] == "quiz":
        questions = exercise["questions"]
        with st.form(f"comm_quiz_{topic['name']}"):
            answers: list[int] = []
            for j, q in enumerate(questions):
                st.markdown(f"**Q{j + 1}.** {q['q']}")
                ans = st.radio(
                    "Select:", q["options"],
                    key=f"cex_{topic['name']}_{j}",
                    horizontal=True, label_visibility="collapsed",
                )
                answers.append(q["options"].index(ans))

            if st.form_submit_button("Submit Quiz"):
                correct = sum(1 for j, a in enumerate(answers) if a == questions[j]["answer"])
                score = int(correct / len(questions) * 100)

                with db_session() as session:
                    existing = session.query(CommunicationProgress).filter_by(
                        user_id=user_id, topic=topic["name"],
                    ).first()
                    if existing:
                        existing.exercise_score = score
                        existing.completed_at = datetime.utcnow()
                    else:
                        session.add(CommunicationProgress(
                            user_id=user_id, topic=topic["name"],
                            lesson_completed=1, exercise_score=score,
                            completed_at=datetime.utcnow(),
                        ))

                st.success(f"Quiz score: {score}% ({correct}/{len(questions)})")
                for j, q in enumerate(questions):
                    if answers[j] == q["answer"]:
                        st.markdown(f"✅ Q{j + 1}: Correct!")
                    else:
                        st.markdown(f"❌ Q{j + 1}: Correct answer: {q['options'][q['answer']]}")
                st.rerun()
