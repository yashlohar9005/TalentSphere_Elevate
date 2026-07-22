"""Quick validation script for all new modules."""
import sys
try:
    from database import init_db
    init_db()
    print("✅ Database initialized — all tables created")

    from modules.high_school import HighSchoolPortal
    print("✅ HighSchoolPortal imported")

    from modules.base_portal import BasePortal
    print("✅ BasePortal imported")

    from modules.hs_features.career_quiz import render_career_quiz, QUIZ_QUESTIONS
    print(f"✅ Career Quiz — {len(QUIZ_QUESTIONS)} questions loaded")

    from modules.hs_features.interest_assessment import render_interest_assessment, STREAMS
    print(f"✅ Interest Assessment — {len(STREAMS)} streams loaded")

    from modules.hs_features.future_roadmap import render_future_roadmap, ROADMAP_TEMPLATES
    print(f"✅ Future Roadmap — {len(ROADMAP_TEMPLATES)} templates loaded")

    from modules.hs_features.daily_tasks import render_daily_tasks, TASK_TEMPLATES
    print(f"✅ Daily Tasks — {len(TASK_TEMPLATES)} categories loaded")

    from modules.hs_features.coding_basics import render_coding_basics, CODING_TOPICS
    print(f"✅ Coding Basics — {len(CODING_TOPICS)} topics loaded")

    from modules.hs_features.aptitude_practice import render_aptitude_practice, APT_CATEGORIES
    print(f"✅ Aptitude Practice — {len(APT_CATEGORIES)} categories loaded")

    from modules.hs_features.communication_skills import render_communication_skills, COMM_TOPICS
    print(f"✅ Communication Skills — {len(COMM_TOPICS)} topics loaded")

    from modules.hs_features.goal_tracker import render_goal_tracker
    print("✅ Goal Tracker imported")

    from modules.hs_features.ai_mentor import render_ai_mentor, RuleBasedProvider, GeminiProvider
    print("✅ AI Mentor Chatbot imported")

    # Test rule-based provider
    provider = RuleBasedProvider()
    response = provider.get_response("How to learn Python?", [])
    assert len(response) > 0, "Rule-based provider returned empty response"
    print(f"✅ Rule-based chatbot works — provider: {provider.get_provider_name()}")

    from database import (
        CareerQuizResult, InterestProfile, DailyTask, CodingProgress,
        AptitudeResult, CommunicationProgress, Goal, ChatHistory
    )
    print("✅ All 8 new database models imported")

    print("\n" + "=" * 50)
    print("🎉 ALL VALIDATIONS PASSED — No import errors!")
    print("=" * 50)

except Exception as e:
    print(f"\n❌ VALIDATION FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
