"""
AI Mentor Chatbot Module for TalentSphere Elevate — High School.

Provider-agnostic architecture:
- ChatProvider (abstract) → RuleBasedProvider (always available) / GeminiProvider (optional)
- If GOOGLE_API_KEY is set, uses Gemini; otherwise rule-based.
- Conversation history stored in ChatHistory table.
- UI is completely decoupled from the provider.

Covers: Career Guidance, Programming, Python, Resume, Interview,
Roadmap, Skills, Certifications, College Preparation.
"""

import streamlit as st
import os
import json
from abc import ABC, abstractmethod
from datetime import datetime
from database import db_session, ChatHistory


# ──────────────────────────────────────────────────────────────────────────────
# Chat Provider Interface (Strategy Pattern)
# ──────────────────────────────────────────────────────────────────────────────

class ChatProvider(ABC):
    """Abstract base class for chat providers."""

    @abstractmethod
    def get_response(self, message: str, history: list[dict]) -> str:
        """Returns a response for the given message and conversation history."""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Returns the name of the provider."""
        pass


class RuleBasedProvider(ChatProvider):
    """Rule-based fallback chatbot engine."""

    KNOWLEDGE_BASE: dict[str, str] = {
        # Career Guidance
        "career": (
            "Great question about careers! Here are some tips:\n"
            "1. Take the AI Career Quiz to discover your strengths\n"
            "2. Complete the Interest Assessment to find your ideal stream\n"
            "3. Explore careers in the Career Explorer\n"
            "4. Set career goals and generate personalized roadmaps\n"
            "5. Talk to professionals in fields that interest you"
        ),
        "career guidance": (
            "For career guidance, I recommend:\n"
            "1. Start with self-assessment — understand your interests and strengths\n"
            "2. Research careers that align with your profile\n"
            "3. Talk to people already in those careers\n"
            "4. Build relevant skills through courses and projects\n"
            "5. Create a 90-day action plan using the Future Skills Roadmap"
        ),
        # Programming
        "programming": (
            "To start programming:\n"
            "1. Choose a language — Python is perfect for beginners\n"
            "2. Learn the basics: variables, loops, functions, data structures\n"
            "3. Practice daily on platforms like HackerRank or LeetCode\n"
            "4. Build projects — start small (calculator, to-do app)\n"
            "5. Check out the Coding Basics section in TalentSphere!"
        ),
        "python": (
            "Python is one of the most popular programming languages!\n\n"
            "**Why Python?**\n"
            "- Easy to learn and read\n"
            "- Used in AI, web dev, data science, automation\n"
            "- Huge community and libraries\n\n"
            "**Getting Started:**\n"
            "1. Install Python from python.org\n"
            "2. Use VS Code or PyCharm as your editor\n"
            "3. Learn: variables, data types, loops, functions\n"
            "4. Try the Coding Basics module right here in TalentSphere!"
        ),
        "code": (
            "Want to learn to code? Here's a roadmap:\n"
            "1. Start with Python — it's beginner-friendly\n"
            "2. Learn HTML/CSS for web development\n"
            "3. Practice problem-solving on coding platforms\n"
            "4. Build small projects to apply what you learn\n"
            "5. Use our Coding Basics module for structured lessons!"
        ),
        # Resume
        "resume": (
            "Tips for building a great resume:\n"
            "1. Include: Education, Skills, Projects, Activities\n"
            "2. Use action verbs (built, designed, led, improved)\n"
            "3. Quantify achievements when possible\n"
            "4. Keep it to 1 page for high school\n"
            "5. Use the Resume Builder in TalentSphere for a professional layout!"
        ),
        # Interview
        "interview": (
            "Interview preparation tips:\n"
            "1. Research the company/school thoroughly\n"
            "2. Practice the STAR method for behavioral questions\n"
            "3. Prepare 3-5 questions to ask the interviewer\n"
            "4. Dress appropriately and arrive early\n"
            "5. Practice with friends or in front of a mirror\n"
            "6. Check our Communication Skills module for more!"
        ),
        # Roadmap
        "roadmap": (
            "To create your learning roadmap:\n"
            "1. Complete the Career Quiz to identify your direction\n"
            "2. Go to Future Skills Roadmap\n"
            "3. A personalized 30/60/90 day plan will be generated\n"
            "4. Follow the milestones and track your progress\n"
            "5. Update daily using the Daily Learning Tasks feature!"
        ),
        # Skills
        "skills": (
            "Essential skills for high school students:\n\n"
            "**Technical:** Programming, Data Analysis, Web Development\n"
            "**Soft Skills:** Communication, Leadership, Teamwork\n"
            "**Academic:** Critical Thinking, Research, Time Management\n\n"
            "Use TalentSphere's modules to build these skills systematically!"
        ),
        # Certifications
        "certifications": (
            "Great certifications for high school students:\n"
            "1. Google IT Support Certificate\n"
            "2. HackerRank Python Certification\n"
            "3. freeCodeCamp Responsive Web Design\n"
            "4. Google Digital Marketing Fundamentals\n"
            "5. Codecademy Language Certifications\n"
            "6. AWS Cloud Practitioner (advanced)\n\n"
            "Check the Coding Basics module for our built-in certificate!"
        ),
        "certification": (
            "Great certifications for high school students:\n"
            "1. Google IT Support Certificate\n"
            "2. HackerRank Python Certification\n"
            "3. freeCodeCamp Responsive Web Design\n"
            "4. Google Digital Marketing Fundamentals\n"
            "5. Codecademy Language Certifications"
        ),
        # College
        "college": (
            "College preparation tips:\n"
            "1. Build a strong academic profile (GPA, AP courses)\n"
            "2. Participate in extracurriculars (clubs, sports, volunteering)\n"
            "3. Develop leadership experience\n"
            "4. Start preparing for entrance exams early\n"
            "5. Build a portfolio of projects\n"
            "6. Research colleges and their requirements\n"
            "7. Write compelling personal statements"
        ),
        "college preparation": (
            "Steps for college preparation:\n"
            "1. Take challenging courses (AP, honors)\n"
            "2. Score well on standardized tests (SAT/ACT/JEE)\n"
            "3. Build meaningful extracurriculars\n"
            "4. Get strong recommendation letters\n"
            "5. Write authentic personal essays\n"
            "6. Apply to a balanced list of schools"
        ),
        # General
        "hello": "Hello! 👋 I'm your AI Career Mentor. I can help you with career guidance, programming, resume building, interview prep, and more. What would you like to know?",
        "hi": "Hi there! 👋 I'm your AI Career Mentor. Ask me anything about careers, coding, skills, or college preparation!",
        "help": (
            "I can help you with:\n"
            "🎯 **Career Guidance** — Exploring career paths\n"
            "💻 **Programming** — Python, coding basics\n"
            "📄 **Resume** — Building your resume\n"
            "💼 **Interview** — Interview preparation\n"
            "🗺️ **Roadmap** — Learning paths\n"
            "🛠️ **Skills** — Skill development\n"
            "📜 **Certifications** — Recommended certs\n"
            "🎓 **College** — College preparation\n\n"
            "Just type your question!"
        ),
        "thank": "You're welcome! 😊 Feel free to ask more questions anytime. Good luck on your career journey!",
        "thanks": "You're welcome! 😊 Keep learning and growing. I'm here whenever you need guidance!",
    }

    def get_response(self, message: str, history: list[dict]) -> str:
        """Matches user message against knowledge base keywords."""
        msg_lower = message.lower().strip()

        # Direct match
        for key, response in self.KNOWLEDGE_BASE.items():
            if key in msg_lower:
                return response

        # Fuzzy match — check if any keyword appears as a word
        words = set(msg_lower.split())
        for key, response in self.KNOWLEDGE_BASE.items():
            key_words = set(key.split())
            if key_words.intersection(words):
                return response

        # Default response
        return (
            "That's a great question! While I don't have a specific answer for that, "
            "here are some things I can help with:\n\n"
            "🎯 Career guidance and exploration\n"
            "💻 Programming and Python\n"
            "📄 Resume building tips\n"
            "💼 Interview preparation\n"
            "🗺️ Learning roadmaps\n"
            "🛠️ Skill development\n"
            "📜 Certifications\n"
            "🎓 College preparation\n\n"
            "Try asking about any of these topics!"
        )

    def get_provider_name(self) -> str:
        return "Rule-Based Engine"


class GeminiProvider(ChatProvider):
    """Google Gemini AI chat provider."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._model = None

    def _get_model(self):
        """Lazy-initialize the Gemini model."""
        if self._model is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._model = genai.GenerativeModel('gemini-2.0-flash')
            except Exception:
                return None
        return self._model

    def get_response(self, message: str, history: list[dict]) -> str:
        """Gets a response from Google Gemini."""
        model = self._get_model()
        if model is None:
            # Fallback to rule-based
            return RuleBasedProvider().get_response(message, history)

        try:
            # Build conversation context
            system_prompt = (
                "You are an AI Career Mentor for high school students on the TalentSphere Elevate platform. "
                "You help with: career guidance, programming (especially Python), resume building, "
                "interview preparation, learning roadmaps, skill development, certifications, "
                "and college preparation. Be encouraging, specific, and actionable. "
                "Keep responses concise (under 300 words)."
            )

            # Build chat history for context
            chat_messages = [f"System: {system_prompt}"]
            for h in history[-10:]:  # Last 10 messages for context
                role = "Student" if h["role"] == "user" else "Mentor"
                chat_messages.append(f"{role}: {h['message']}")
            chat_messages.append(f"Student: {message}")

            full_prompt = "\n".join(chat_messages) + "\nMentor:"

            response = model.generate_content(full_prompt)
            return response.text if response.text else "I'm sorry, I couldn't generate a response. Please try again."

        except Exception as e:
            # Fallback to rule-based on any error
            return RuleBasedProvider().get_response(message, history)

    def get_provider_name(self) -> str:
        return "Google Gemini AI"


def _get_chat_provider() -> ChatProvider:
    """Factory function to get the appropriate chat provider."""
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if api_key:
        return GeminiProvider(api_key)
    return RuleBasedProvider()


def _load_chat_history(user_id: int) -> list[dict]:
    """Loads chat history from database."""
    with db_session() as session:
        records = (
            session.query(ChatHistory)
            .filter_by(user_id=user_id)
            .order_by(ChatHistory.created_at.asc())
            .all()
        )
        return [{"role": r.role, "message": r.message} for r in records]


def _save_message(user_id: int, role: str, message: str) -> None:
    """Saves a chat message to the database."""
    with db_session() as session:
        session.add(ChatHistory(
            user_id=user_id, role=role, message=message,
        ))


def render_ai_mentor(user_id: int) -> None:
    """Renders the AI Mentor Chatbot page."""
    st.header("🤖 Mentor Chatbot")

    provider = _get_chat_provider()
    st.caption(f"Powered by: {provider.get_provider_name()}")

    st.write("Ask me anything about careers, coding, skills, college, or personal development!")

    # Initialize chat session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = _load_chat_history(user_id)

    # Display chat history
    for msg in st.session_state.chat_messages:
        role = msg["role"]
        avatar = "🧑‍🎓" if role == "user" else "🤖"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["message"])

    # Welcome message if empty
    if not st.session_state.chat_messages:
        with st.chat_message("assistant", avatar="🤖"):
            welcome = (
                "Hello! 👋 I'm your AI Career Mentor. I'm here to help you with:\n\n"
                "🎯 Career guidance and exploration\n"
                "💻 Programming and Python\n"
                "📄 Resume building tips\n"
                "💼 Interview preparation\n"
                "🗺️ Learning roadmaps\n"
                "🛠️ Skill development\n"
                "📜 Certifications\n"
                "🎓 College preparation\n\n"
                "Type your question below to get started!"
            )
            st.markdown(welcome)

    # Chat input
    user_input = st.chat_input("Ask your AI Mentor...")

    if user_input:
        # Display user message
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(user_input)

        # Save user message
        st.session_state.chat_messages.append({"role": "user", "message": user_input})
        _save_message(user_id, "user", user_input)

        # Get AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                response = provider.get_response(user_input, st.session_state.chat_messages)
            
            # Sanitize markdown code blocks to prevent StreamlitSyntaxHighlighter crash
            import re
            safe_response = re.sub(r'```[a-zA-Z0-9]+', '```text', response)
            st.markdown(safe_response)

        # Save assistant response
        st.session_state.chat_messages.append({"role": "assistant", "message": safe_response})
        _save_message(user_id, "assistant", safe_response)

    # Sidebar quick actions
    with st.sidebar:
        st.markdown("---")
        st.subheader("💬 Quick Questions")
        quick_questions = [
            "How do I start learning Python?",
            "What career is right for me?",
            "How to prepare for interviews?",
            "Best certifications for students?",
            "How to build a resume?",
        ]
        for qq in quick_questions:
            if st.button(qq, key=f"qq_{qq[:20]}", use_container_width=True):
                st.session_state["pending_question"] = qq
                st.rerun()

    # Handle quick question from sidebar
    if "pending_question" in st.session_state:
        pq = st.session_state.pop("pending_question")
        st.session_state.chat_messages.append({"role": "user", "message": pq})
        _save_message(user_id, "user", pq)

        response = provider.get_response(pq, st.session_state.chat_messages)
        
        # Sanitize markdown
        import re
        safe_response = re.sub(r'```[a-zA-Z0-9]+', '```text', response)
        
        st.session_state.chat_messages.append({"role": "assistant", "message": safe_response})
        _save_message(user_id, "assistant", safe_response)
        st.rerun()

    # Clear chat button
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        with db_session() as session:
            session.query(ChatHistory).filter_by(user_id=user_id).delete()
        st.session_state.chat_messages = []
        st.rerun()
