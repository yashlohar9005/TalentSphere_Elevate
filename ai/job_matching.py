class JobMatchingEngine:
    def __init__(self):
        self.roles = [
            "Software Developer", "Software Engineer", "Backend Developer", "Frontend Developer", 
            "Python Developer", "Full Stack Developer", "AI Engineer", "Machine Learning Engineer", 
            "Cloud Engineer", "DevOps Engineer", "QA Engineer", "Cyber Security", 
            "Data Analyst"
        ]
        
        # Simplified mapping of required skills per role
        self.role_skills = {
            "Software Developer": ["java", "python", "c++", "git", "sql"],
            "Software Engineer": ["java", "python", "c++", "git", "sql", "data structures"],
            "Backend Developer": ["node.js", "python", "java", "sql", "api", "docker"],
            "Frontend Developer": ["html", "css", "javascript", "react", "angular", "vue"],
            "Python Developer": ["python", "django", "flask", "sql", "api"],
            "Full Stack Developer": ["react", "node.js", "javascript", "html", "css", "sql", "mongodb"],
            "AI Engineer": ["python", "tensorflow", "pytorch", "machine learning", "nlp"],
            "Machine Learning Engineer": ["python", "scikit-learn", "tensorflow", "statistics"],
            "Cloud Engineer": ["aws", "azure", "gcp", "docker", "kubernetes", "linux"],
            "DevOps Engineer": ["ci/cd", "jenkins", "docker", "kubernetes", "aws", "linux", "bash"],
            "QA Engineer": ["selenium", "testing", "java", "python", "automation"],
            "Cyber Security": ["security", "network", "linux", "firewalls", "cryptography"],
            "Data Analyst": ["sql", "python", "excel", "tableau", "statistics", "pandas"]
        }
        
    def get_job_match(self, role: str, student_skills: str, cgpa: float) -> dict:
        """
        Generate Match % against a specific role based on skills and CGPA.
        """
        req_skills = self.role_skills.get(role, [])
        student_skills_lower = student_skills.lower()
        
        matched = []
        missing = []
        for rs in req_skills:
            if rs in student_skills_lower:
                matched.append(rs)
            else:
                missing.append(rs)
                
        skill_match_pct = (len(matched) / max(len(req_skills), 1)) * 100
        cgpa_match_pct = min((cgpa / 8.0) * 100, 100) # Baseline CGPA expectation 8.0
        
        final_match = int((skill_match_pct * 0.7) + (cgpa_match_pct * 0.3))
        
        reasons = []
        if skill_match_pct > 80:
            reasons.append(f"Strong technical skill alignment for {role}.")
        elif skill_match_pct < 40:
            reasons.append(f"Significant skill gaps exist for {role}.")
            
        if cgpa >= 8.5:
            reasons.append("Excellent academic record boosts your profile.")
            
        salary_map = {
            "Software Developer": "$70k - $100k",
            "Software Engineer": "$80k - $120k",
            "Frontend Developer": "$70k - $110k",
            "Backend Developer": "$80k - $120k",
            "AI Engineer": "$100k - $140k",
            "Data Analyst": "$65k - $90k",
            "Full Stack Developer": "$80k - $120k",
            "Cloud Engineer": "$90k - $130k",
            "Cyber Security": "$90k - $130k",
        }
        
        company_map = {
            "AI Engineer": ["Google", "OpenAI", "Meta"],
            "Cloud Engineer": ["Amazon", "Microsoft", "Google"],
            "Frontend Developer": ["Netflix", "Airbnb", "Meta"],
            "Data Analyst": ["Bloomberg", "JPMorgan", "Deloitte"]
        }
        
        recommendation = f"Focus on building projects using {' and '.join(missing[:2])}." if missing else f"You are an excellent fit for {role}. Start applying!"
        courses = [f"Mastering {m.capitalize()}" for m in missing[:3]] if missing else ["Advanced System Design", "Interview Prep"]
        
        return {
            "role": role,
            "match_percentage": final_match,
            "reasons": reasons,
            "missing_skills": missing,
            "recommended_courses": courses,
            "salary_range": salary_map.get(role, "$75k - $110k"),
            "hiring_companies": company_map.get(role, ["TCS", "Infosys", "Wipro", "Accenture"]),
            "career_recommendation": recommendation
        }
