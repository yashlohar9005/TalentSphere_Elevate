"""
Career Predictor for TalentSphere Elevate.
Predicts career path, readiness, and growth.
"""

class CareerPredictor:
    def predict_career(self, profile_data: dict) -> dict:
        """
        Predict Career Path, Promotion Readiness, Placement Readiness, Career Growth Score.
        profile_data expects: 
        {
            "career_stage": "professional",
            "category": "Engineering Leader",
            "readiness_percentage": 85,
            "assessments_completed": 3,
            "roadmaps_completed": 1
        }
        """
        category = profile_data.get("category", "General")
        stage = profile_data.get("career_stage", "college")
        readiness_pct = profile_data.get("readiness_percentage", 50)
        assessments = profile_data.get("assessments_completed", 0)
        roadmaps = profile_data.get("roadmaps_completed", 0)
        
        # Base logic
        career_path = f"Trajectory towards {category}"
        
        engagement_bonus = min((assessments + roadmaps) * 5, 20)
        
        promotion_readiness = min(readiness_pct + engagement_bonus, 100) if stage == "professional" else 0
        placement_readiness = min(readiness_pct + engagement_bonus, 100) if stage in ["high_school", "college"] else 0
        
        career_growth_score = min(int((readiness_pct * 0.7) + (engagement_bonus * 3)), 100)
        
        return {
            "career_path": career_path,
            "promotion_readiness": promotion_readiness,
            "placement_readiness": placement_readiness,
            "career_growth_score": career_growth_score
        }
