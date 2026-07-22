"""
AI Engine Module for TalentSphere Elevate.
Exposes modular engines for recommendation, skill gaps, roadmaps, resume analysis, and career prediction.
"""
from ai.recommendation_engine import RecommendationEngine
from ai.skill_gap import SkillGapEngine
from ai.roadmap_generator import RoadmapGenerator
from ai.resume_analyzer import ResumeAnalyzer
from ai.career_predictor import CareerPredictor
from ai.coding_engine import CodingEngine
from ai.placement_engine import PlacementEngine
from ai.interview_engine import InterviewEngine
from ai.job_matching import JobMatchingEngine
from ai.internship_engine import InternshipEngine

class AIEngine:
    """Facade for the AI Engine submodules."""
    def __init__(self):
        self.recommendation_engine = RecommendationEngine()
        self.skill_gap = SkillGapEngine()
        self.roadmap_generator = RoadmapGenerator()
        self.resume_analyzer = ResumeAnalyzer()
        self.career_predictor = CareerPredictor()
        self.coding_engine = CodingEngine()
        self.placement_engine = PlacementEngine()
        self.interview_engine = InterviewEngine()
        self.job_matching = JobMatchingEngine()
        self.internship_engine = InternshipEngine()
