import random

class InternshipEngine:
    def get_recommendations(self, cgpa: float, skills: str, location: str, role: str) -> list:
        """
        Recommends internships based on CGPA, skills, projects, and preferred location/role.
        """
        # Simulated database of internships
        mock_internships = [
            {"company": "Google", "role": "Software Engineering Intern", "location": "Bangalore", "req_skills": ["python", "java", "data structures"]},
            {"company": "Microsoft", "role": "Cloud Intern", "location": "Hyderabad", "req_skills": ["azure", "c#", "networking"]},
            {"company": "Amazon", "role": "SDE Intern", "location": "Remote", "req_skills": ["java", "aws", "algorithms"]},
            {"company": "Infosys", "role": "Systems Engineer Intern", "location": "Pune", "req_skills": ["python", "sql", "html"]},
            {"company": "TCS", "role": "Data Analyst Intern", "location": "Mumbai", "req_skills": ["sql", "python", "excel"]},
            {"company": "LocalTech", "role": "Web Dev Intern", "location": "Remote", "req_skills": ["react", "javascript", "css"]}
        ]
        
        student_skills = skills.lower()
        results = []
        
        for intern in mock_internships:
            # Simple matching logic
            matched_skills = [s for s in intern["req_skills"] if s in student_skills]
            match_pct = int((len(matched_skills) / len(intern["req_skills"])) * 100)
            
            # Boost score based on location or role match
            if location.lower() in intern["location"].lower() or intern["location"] == "Remote":
                match_pct += 10
            if role.lower() in intern["role"].lower():
                match_pct += 15
                
            match_pct = min(match_pct, 100)
            
            if cgpa >= 8.0:
                eligibility = "Eligible"
            elif cgpa >= 7.0 and intern["company"] not in ["Google", "Microsoft", "Amazon"]:
                eligibility = "Eligible"
            else:
                eligibility = "CGPA Requirement Not Met (Requires 8.0+)"
                match_pct -= 20 # Penalize match percentage if ineligible
                
            if match_pct > 30:
                reason = "Strong match across skills and location." if match_pct >= 80 else "Partial match, consider upskilling."
                readiness = "High" if match_pct >= 80 and eligibility == "Eligible" else "Medium" if match_pct >= 50 else "Low"
                roadmap = ["Complete assigned technical courses", "Update your resume", "Apply via career portal"]
                
                results.append({
                    "company": intern["company"],
                    "role": intern["role"],
                    "location": intern["location"],
                    "required_skills": intern["req_skills"],
                    "eligibility": eligibility,
                    "match_percentage": match_pct,
                    "reason_for_recommendation": reason,
                    "application_readiness": readiness,
                    "learning_roadmap": roadmap
                })
                
        # Sort by best match
        results = sorted(results, key=lambda x: x["match_percentage"], reverse=True)
        return results
