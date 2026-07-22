"""
Skill Gap Engine for TalentSphere Elevate.
Analyzes current skills against required benchmarks.
"""

class SkillGapEngine:
    def analyze_gap(self, current_skills: dict, required_skills: dict, target_role: str = "") -> dict:
        """
        Compare current skills to required skills and identify gaps.
        Generates courses, certifications, and project recommendations.
        """
        missing_skills = {}
        total_required = 0
        total_current = 0
        
        for skill, required_level in required_skills.items():
            current_level = current_skills.get(skill, 0)
            total_required += required_level
            total_current += min(current_level, required_level)  # cap at required level
            
            if current_level < required_level:
                missing_skills[skill] = required_level - current_level

        readiness_percentage = int((total_current / total_required * 100) if total_required > 0 else 100)
        
        # Priority Ranking: sort missing skills by largest gap
        priority_ranking = sorted(missing_skills.items(), key=lambda item: item[1], reverse=True)
        priority_skills = [skill for skill, gap in priority_ranking]
        
        learning_suggestions = [f"Focus on improving {skill} to close the gap." for skill in priority_skills]
        
        # Course, cert, project recommendations
        courses = []
        projects = []
        certs = []
        
        for skill in priority_skills[:3]:
            courses.append(f"Mastering {skill} 101")
            projects.append(f"Build a practical system using {skill}")
            certs.append(f"Certified {skill} Professional")
            
        return {
            "target_role": target_role,
            "missing_skills": missing_skills,
            "readiness_percentage": readiness_percentage,
            "priority_ranking": priority_skills,
            "learning_suggestions": learning_suggestions,
            "recommended_courses": courses,
            "recommended_projects": projects,
            "recommended_certifications": certs
        }
