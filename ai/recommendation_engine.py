"""
Recommendation Engine for TalentSphere Elevate.
Provides rule-based actionable recommendations for career growth.
"""

class RecommendationEngine:
    def generate_recommendations(self, career_stage: str, assessment_category: str, skills: dict, progress: dict = None) -> dict:
        """
        Generate recommendations using rule-based logic.
        Can be replaced by Gemini/OpenAI in the future.
        """
        # Default structures
        recommendations = {
            "courses": [],
            "projects": [],
            "certifications": [],
            "career_suggestions": []
        }
        
        # High School logic
        if career_stage == "high_school":
            if assessment_category == "STEM":
                recommendations["courses"] = ["Intro to Computer Science", "AP Physics"]
                recommendations["projects"] = ["Build a simple calculator app", "Science fair physics model"]
                recommendations["career_suggestions"] = ["Software Engineer", "Data Scientist", "Mechanical Engineer"]
            else:
                recommendations["courses"] = ["Creative Writing 101", "Public Speaking Mastery"]
                recommendations["projects"] = ["Start a personal blog", "Join the debate team"]
                recommendations["career_suggestions"] = ["Journalist", "Communications Manager", "UX Designer"]
                
        # College logic
        elif career_stage == "college":
            if assessment_category == "Technical & Hard Skills Focused":
                recommendations["courses"] = ["Advanced Algorithms", "System Design Basics"]
                recommendations["projects"] = ["Contribute to an open-source repo", "Build a full-stack web app"]
                recommendations["certifications"] = ["AWS Certified Cloud Practitioner"]
                recommendations["career_suggestions"] = ["Backend Engineer", "Cloud Solutions Architect"]
            else:
                recommendations["courses"] = ["Leadership and Organizational Behavior", "Project Management 101"]
                recommendations["projects"] = ["Organize a campus hackathon", "Lead a student organization"]
                recommendations["certifications"] = ["Certified Scrum Master (CSM) Basics"]
                recommendations["career_suggestions"] = ["Product Manager", "Management Consultant"]
                
        # Professional logic
        elif career_stage == "professional":
            if assessment_category == "Engineering Leader":
                recommendations["courses"] = ["Advanced System Design", "Engineering Management 101"]
                recommendations["projects"] = ["Architect a scalable microservices backend"]
                recommendations["certifications"] = ["AWS Certified Solutions Architect - Professional"]
                recommendations["career_suggestions"] = ["Staff Engineer", "Engineering Manager"]
            elif assessment_category == "Technical Specialist":
                recommendations["courses"] = ["Kubernetes in Action", "Advanced Python Concurrency"]
                recommendations["projects"] = ["Build a CI/CD pipeline from scratch"]
                recommendations["certifications"] = ["Certified Kubernetes Administrator (CKA)"]
                recommendations["career_suggestions"] = ["Principal Engineer", "Cloud Native Expert"]
            else:
                recommendations["courses"] = ["Agile Product Management", "Data-Driven Decision Making"]
                recommendations["projects"] = ["Lead a cross-functional sprint delivery"]
                recommendations["certifications"] = ["Certified Scrum Master (CSM)"]
                recommendations["career_suggestions"] = ["Senior Product Manager", "Director of Product"]
                
        return recommendations

    def get_career_recommendations(self, career_name: str) -> dict:
        """
        Returns career-specific recommendations for the Career Explorer.
        Provides tailored courses, projects, and certifications for a given career.
        """
        career_recs = {
            "Software Engineer": {
                "courses": ["Data Structures & Algorithms", "Object-Oriented Programming", "Software Engineering Principles"],
                "projects": ["Build a CLI task manager", "Create a REST API", "Develop a chat application"],
                "certifications": ["AWS Certified Cloud Practitioner", "Oracle Certified Java Programmer"],
            },
            "AI Engineer": {
                "courses": ["Machine Learning Fundamentals", "Deep Learning with PyTorch", "Natural Language Processing"],
                "projects": ["Train an image classifier", "Build a sentiment analysis tool", "Create a chatbot with NLP"],
                "certifications": ["TensorFlow Developer Certificate", "Google Cloud ML Engineer"],
            },
            "Data Scientist": {
                "courses": ["Statistics & Probability", "Data Analysis with Python", "SQL for Data Science"],
                "projects": ["Exploratory data analysis on a public dataset", "Build a predictive model", "Create an interactive dashboard"],
                "certifications": ["IBM Data Science Professional Certificate", "Google Data Analytics Certificate"],
            },
            "Cyber Security Analyst": {
                "courses": ["Network Security Fundamentals", "Ethical Hacking Basics", "Cryptography 101"],
                "projects": ["Set up a home lab firewall", "Perform a vulnerability scan", "Build a password strength checker"],
                "certifications": ["CompTIA Security+", "Certified Ethical Hacker (CEH)"],
            },
            "Web Developer": {
                "courses": ["HTML, CSS & JavaScript Mastery", "React.js for Beginners", "Backend with Node.js"],
                "projects": ["Build a personal portfolio website", "Create a weather app", "Develop an e-commerce storefront"],
                "certifications": ["Meta Front-End Developer Certificate", "freeCodeCamp Responsive Web Design"],
            },
            "Game Developer": {
                "courses": ["Game Design Principles", "Unity for Beginners", "C# Programming Fundamentals"],
                "projects": ["Build a 2D platformer game", "Create a puzzle game prototype", "Design a text-based RPG"],
                "certifications": ["Unity Certified Developer", "Unreal Engine Certification"],
            },
        }

        return career_recs.get(career_name, {
            "courses": ["Explore introductory courses in this field"],
            "projects": ["Start a beginner project related to this career"],
            "certifications": [],
        })
