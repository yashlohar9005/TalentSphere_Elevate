"""
Database Module for TalentSphere Elevate

This module sets up the SQLite database using SQLAlchemy ORM.
It defines the core models used across the application:
- User: Stores user credentials and profile type.
- Assessment: Stores results from career/skill assessments.
- Roadmap: Stores generated learning paths for users.
- Progress: Tracks user completion of roadmap milestones.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, joinedload, selectinload

# Create the declarative base for the ORM models
Base = declarative_base()

class User(Base):
    """
    User model representing registered users in the platform.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    full_name = Column(String(100), nullable=True)  # Optional display name
    dob = Column(String(10), nullable=True)  # Date of Birth in DD/MM/YYYY format
    user_type = Column(String(50), nullable=False)  # High School, College, Professional, Admin
    is_active = Column(Integer, default=1) # 1 for True, 0 for False (deactivated)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    assessments = relationship("Assessment", back_populates="user", cascade="all, delete-orphan")
    roadmaps = relationship("Roadmap", back_populates="user", cascade="all, delete-orphan")
    resume_data = relationship("ResumeData", back_populates="user", uselist=False, cascade="all, delete-orphan")
    inbox = relationship("UserInbox", back_populates="user", cascade="all, delete-orphan")
    career_goals = relationship("CareerGoal", back_populates="user", cascade="all, delete-orphan")
    quiz_results = relationship("CareerQuizResult", back_populates="user", cascade="all, delete-orphan")
    interest_profiles = relationship("InterestProfile", back_populates="user", cascade="all, delete-orphan")
    daily_tasks = relationship("DailyTask", back_populates="user", cascade="all, delete-orphan")
    coding_progress = relationship("CodingProgress", back_populates="user", cascade="all, delete-orphan")
    aptitude_results = relationship("AptitudeResult", back_populates="user", cascade="all, delete-orphan")
    communication_progress = relationship("CommunicationProgress", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    chat_history = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    college_student_profile = relationship("CollegeStudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Assessment(Base):
    """
    Assessment model storing user skill gap analysis results.
    """
    __tablename__ = 'assessments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String(100), nullable=False) # e.g., 'Programming', 'Soft Skills'
    score = Column(Integer, nullable=False)
    details = Column(Text, nullable=True) # JSON or detailed text of the assessment
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="assessments")

class Roadmap(Base):
    """
    Roadmap model representing a tailored learning path for a user.
    """
    __tablename__ = 'roadmaps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False) # JSON or markdown content of the roadmap
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="roadmaps")
    progress_items = relationship("Progress", back_populates="roadmap", cascade="all, delete-orphan")

class Progress(Base):
    """
    Progress model tracking completion of specific milestones in a roadmap.
    """
    __tablename__ = 'progress'

    id = Column(Integer, primary_key=True, autoincrement=True)
    roadmap_id = Column(Integer, ForeignKey('roadmaps.id'), nullable=False)
    milestone_name = Column(String(200), nullable=False)
    is_completed = Column(Integer, default=0) # 0 for False, 1 for True
    completed_at = Column(DateTime, nullable=True)

    roadmap = relationship("Roadmap", back_populates="progress_items")


class ResumeData(Base):
    """
    ResumeData model storing user's resume details as structured JSON.
    """
    __tablename__ = 'resume_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    content = Column(Text, nullable=False) # JSON containing resume details
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="resume_data")

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CareerPath(Base):
    __tablename__ = 'career_paths'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    skills = Column(Text, nullable=True) # JSON list
    certifications = Column(Text, nullable=True) # JSON list
    created_at = Column(DateTime, default=datetime.utcnow)


class CareerGoal(Base):
    """
    CareerGoal model storing a user's selected career exploration goals.
    Created when users click 'Add to Goal' in the Career Explorer.
    """
    __tablename__ = 'career_goals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    career_name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="career_goals")

class Quiz(Base):
    __tablename__ = 'quizzes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    is_published = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(Text, nullable=False) # JSON list
    correct_answer = Column(String(200), nullable=False)
    
    quiz = relationship("Quiz", back_populates="questions")

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    target_group = Column(String(100), nullable=False) # 'High School Student', 'All', or user_id
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserInbox(Base):
    __tablename__ = 'user_inbox'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    notification_type = Column(String(50), nullable=False) # Information, Warning, Success, Achievement, Reminder
    message = Column(Text, nullable=False)
    is_read = Column(Integer, default=0) # 0 False, 1 True
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="inbox")


# ──────────────────────────────────────────────────────────────────────────────
# High School Module — New Models
# ──────────────────────────────────────────────────────────────────────────────

class CareerQuizResult(Base):
    """Stores AI Career Quiz results for a user."""
    __tablename__ = 'career_quiz_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    scores = Column(Text, nullable=False)           # JSON: category → score
    personality_type = Column(String(100), nullable=False)
    recommended_careers = Column(Text, nullable=False)  # JSON list
    confidence_level = Column(Integer, nullable=False)   # 0–100
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quiz_results")


class InterestProfile(Base):
    """Stores Interest Assessment results across career streams."""
    __tablename__ = 'interest_profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    scores = Column(Text, nullable=False)            # JSON: stream → score
    recommended_streams = Column(Text, nullable=False)  # JSON list
    skill_suggestions = Column(Text, nullable=False)    # JSON list
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="interest_profiles")


class DailyTask(Base):
    """Stores daily learning tasks with completion status."""
    __tablename__ = 'daily_tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    task_date = Column(String(10), nullable=False)   # YYYY-MM-DD
    task_text = Column(String(300), nullable=False)
    category = Column(String(50), nullable=False)    # coding, aptitude, career, reading, communication
    is_completed = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="daily_tasks")


class CodingProgress(Base):
    """Tracks coding lesson and quiz progress per topic."""
    __tablename__ = 'coding_progress'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    topic = Column(String(100), nullable=False)
    lesson_completed = Column(Integer, default=0)    # 0 or 1
    quiz_score = Column(Integer, nullable=True)      # 0–100
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="coding_progress")


class AptitudeResult(Base):
    """Stores aptitude practice quiz results."""
    __tablename__ = 'aptitude_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String(100), nullable=False)   # Quantitative, Logical, Verbal, etc.
    difficulty = Column(String(20), nullable=False)   # Easy, Medium, Hard
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    time_taken_seconds = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)             # JSON with per-question results
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="aptitude_results")


class CommunicationProgress(Base):
    """Tracks communication skills module progress per topic."""
    __tablename__ = 'communication_progress'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    topic = Column(String(100), nullable=False)
    lesson_completed = Column(Integer, default=0)
    exercise_score = Column(Integer, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="communication_progress")


class Goal(Base):
    """Student-defined goals with deadline and progress tracking."""
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(String(10), nullable=True)      # YYYY-MM-DD
    progress = Column(Integer, default=0)              # 0–100
    status = Column(String(20), default="Active")      # Active, Completed, Cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="goals")


class ChatHistory(Base):
    """Stores AI Mentor Chatbot conversation history."""
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(String(20), nullable=False)          # 'user' or 'assistant'
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_history")

class StudentProfile(Base):
    """
    Personal Information module for High School Students.
    Stores comprehensive profile data for reports, certificates, and AI engines.
    """
    __tablename__ = 'student_profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    
    # Basic Details
    full_name = Column(String(100), nullable=True)
    dob = Column(String(20), nullable=True)
    gender = Column(String(20), nullable=True)
    blood_group = Column(String(10), nullable=True)
    mobile = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    
    # Academic Details
    school_name = Column(String(200), nullable=True)
    student_class = Column(String(50), nullable=True)
    board = Column(String(100), nullable=True)
    percentage = Column(String(50), nullable=True)
    favorite_subject = Column(String(100), nullable=True)
    least_favorite_subject = Column(String(100), nullable=True)
    
    # Career Information
    dream_career = Column(String(200), nullable=True)
    interest = Column(String(200), nullable=True)
    hobbies = Column(Text, nullable=True)
    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)
    
    # Address
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="student_profile")


class CollegeStudentProfile(Base):
    """
    College Student Profile module.
    Stores academic, technical, and career information for college students
    required for placement preparation and AI-based career recommendations.
    One profile per user.
    """
    __tablename__ = 'college_student_profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)

    # Section 1 — Personal Information
    full_name = Column(String(100), nullable=True)
    dob = Column(String(20), nullable=True)
    gender = Column(String(20), nullable=True)
    mobile = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)

    # Section 2 — Academic Information
    college_name = Column(String(200), nullable=True)
    university_name = Column(String(200), nullable=True)
    degree = Column(String(50), nullable=True)
    department = Column(String(100), nullable=True)
    year_of_study = Column(String(50), nullable=True)
    semester = Column(String(20), nullable=True)
    cgpa = Column(String(20), nullable=True)
    percentage = Column(String(20), nullable=True)

    # Section 3 — Technical Skills (stored as JSON)
    programming_languages = Column(Text, nullable=True)
    frameworks = Column(Text, nullable=True)
    databases = Column(Text, nullable=True)
    tools = Column(Text, nullable=True)

    # Section 4 — Career Information
    interested_job_roles = Column(Text, nullable=True)  # JSON list
    preferred_industry = Column(String(200), nullable=True)
    employment_type = Column(String(50), nullable=True)
    preferred_work_location = Column(String(200), nullable=True)

    # Section 5 — Resume Upload
    resume_file_path = Column(String(500), nullable=True)

    # Section 6 — Career Goal
    short_term_goal = Column(Text, nullable=True)
    long_term_goal = Column(Text, nullable=True)
    target_company = Column(String(200), nullable=True)
    dream_role = Column(String(200), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="college_student_profile")

# ──────────────────────────────────────────────────────────────────────────────
# College Module — Enhanced AI Models
# ──────────────────────────────────────────────────────────────────────────────

class ATSResult(Base):
    __tablename__ = 'ats_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    resume_score = Column(Integer, default=0)
    ats_compatibility = Column(Integer, default=0)
    keyword_match = Column(Integer, default=0)
    formatting_score = Column(Integer, default=0)
    education_score = Column(Integer, default=0)
    project_score = Column(Integer, default=0)
    experience_score = Column(Integer, default=0)
    technical_skills_score = Column(Integer, default=0)
    soft_skills_score = Column(Integer, default=0)
    feedback_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class CollegeCodingTest(Base):
    __tablename__ = 'college_coding_tests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    topic = Column(String(100), nullable=False)
    score = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    weak_topics = Column(Text, nullable=True) # JSON list
    strong_topics = Column(Text, nullable=True) # JSON list
    ai_suggestions = Column(Text, nullable=True)
    completed_at = Column(DateTime, default=datetime.utcnow)

class PlacementReadiness(Base):
    __tablename__ = 'placement_readiness'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    placement_score = Column(Integer, default=0)
    industry_readiness = Column(Integer, default=0)
    overall_recommendation = Column(Text, nullable=True)
    details_json = Column(Text, nullable=True) # Contains the breakdown of weights
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MockInterviewResult(Base):
    __tablename__ = 'mock_interview_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    interview_type = Column(String(50), nullable=False) # Technical, HR, Behavioral
    confidence_score = Column(Integer, default=0)
    communication_score = Column(Integer, default=0)
    technical_accuracy = Column(Integer, default=0)
    answer_relevance = Column(Integer, default=0)
    problem_solving = Column(Integer, default=0)
    overall_score = Column(Integer, default=0)
    ai_feedback = Column(Text, nullable=True)
    improvement_suggestions = Column(Text, nullable=True) # JSON list
    completed_at = Column(DateTime, default=datetime.utcnow)

class JobMatchResult(Base):
    __tablename__ = 'job_match_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    job_role = Column(String(100), nullable=False)
    match_percentage = Column(Integer, default=0)
    reasons = Column(Text, nullable=True) # JSON list
    missing_skills = Column(Text, nullable=True) # JSON list
    salary_range = Column(String(100), nullable=True)
    career_recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class InternshipRecommendation(Base):
    __tablename__ = 'internship_recommendations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    company = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    required_skills = Column(Text, nullable=True) # JSON list
    eligibility = Column(Text, nullable=True)
    match_percentage = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database Setup and Initialization

DATABASE_URL = "sqlite:///talentsphere.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)

def init_db():
    """
    Initializes the database by creating all defined tables.
    """
    Base.metadata.create_all(bind=engine)

from contextlib import contextmanager

@contextmanager
def db_session():
    """
    Context manager for safely acquiring and releasing database sessions.
    Prevents connection pooling leaks.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    # Initialize the database when this script is run directly
    init_db()
    print("Database initialized and tables created successfully.")
