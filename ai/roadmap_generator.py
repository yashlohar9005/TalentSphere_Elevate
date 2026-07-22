"""
Roadmap Generator for TalentSphere Elevate.
Generates structured 30/60/90 day plans.
"""

class RoadmapGenerator:
    def generate_roadmap(self, career_stage: str, category: str) -> dict:
        """
        Generates 30, 60, 90 day plans based on user profile.
        """
        if career_stage == "high_school":
            if category == "STEM":
                title = "Intro to Computer Science Pathway"
                plan = [
                    ("30-Day Plan", ["Learn Python Basics", "Complete simple coding exercises"]),
                    ("60-Day Plan", ["Build a simple App", "Learn about algorithms"]),
                    ("90-Day Plan", ["Take AP Computer Science prep", "Participate in a Hackathon"])
                ]
            else:
                title = "Communications & Arts Pathway"
                plan = [
                    ("30-Day Plan", ["Start a personal blog", "Write weekly entries"]),
                    ("60-Day Plan", ["Join the Debate Team", "Write a structured article"]),
                    ("90-Day Plan", ["Take AP English Literature prep", "Enter a writing competition"])
                ]
        elif career_stage == "college":
            if category == "Technical & Hard Skills Focused":
                title = "Software Engineering Internship Prep"
                plan = [
                    ("30-Day Plan", ["Update Resume with Projects", "Review Data Structures"]),
                    ("60-Day Plan", ["Practice LeetCode / Technical Questions", "Attend Career Fair"]),
                    ("90-Day Plan", ["Apply to 20 Internships", "Conduct Mock Interviews"])
                ]
            else:
                title = "Leadership & Management Pathway"
                plan = [
                    ("30-Day Plan", ["Refine LinkedIn Profile", "Join a Student Org"]),
                    ("60-Day Plan", ["Conduct 3 Informational Interviews", "Run for Leadership Board"]),
                    ("90-Day Plan", ["Apply to Management Training Programs", "Organize a campus event"])
                ]
        else: # professional
            if category == "Engineering Leader":
                title = "Path to Staff Engineer / Manager"
                plan = [
                    ("30-Day Plan", ["Read 'Designing Data-Intensive Applications'", "Lead a technical design review"]),
                    ("60-Day Plan", ["Complete AWS Solutions Architect course", "Mentor a junior developer"]),
                    ("90-Day Plan", ["Pass AWS Cert exam", "Propose a major architectural improvement to leadership"])
                ]
            elif category == "Technical Specialist":
                title = "Cloud Native Expert"
                plan = [
                    ("30-Day Plan", ["Master Docker fundamentals", "Deploy a simple app to AWS ECS"]),
                    ("60-Day Plan", ["Take CKA preparation course", "Implement monitoring with Prometheus/Grafana"]),
                    ("90-Day Plan", ["Pass CKA exam", "Migrate a monolithic service to Kubernetes"])
                ]
            else:
                title = "Product / Management Track"
                plan = [
                    ("30-Day Plan", ["Complete Agile basics course", "Run a successful sprint retrospective"]),
                    ("60-Day Plan", ["Prepare for CSM exam", "Improve team velocity by 10%"]),
                    ("90-Day Plan", ["Pass CSM exam", "Present quarterly roadmap to stakeholders"])
                ]
                
        # Format the plan into the required output
        roadmap = {
            "title": title,
            "roadmap_plan": plan,
            "flat_steps": [f"[{phase}] {task}" for phase, tasks in plan for task in tasks],
            "daily_tasks": ["Spend 1 hour reading documentation", "Write 20 lines of code"],
            "weekly_goals": [plan[0][1][0] if plan else "Review concepts"],
            "monthly_goals": [phase for phase, _ in plan],
            "estimated_completion": "90 Days",
            "skill_timeline": "Foundational (0-30 days) -> Intermediate (30-60 days) -> Advanced (60-90 days)",
            "resources": ["Official Documentation", "Video Tutorials", "Interactive Platforms"],
            "difficulty": "Intermediate",
            "priority": "High"
        }
        return roadmap

    def generate_career_roadmap(self, career_name: str) -> dict:
        """
        Generates a career-specific 30/60/90 day roadmap for Career Explorer goals.
        Returns the same dict format as generate_roadmap() for compatibility with
        BasePortal.generate_roadmap().
        """
        career_plans = {
            "Software Engineer": {
                "title": "Software Engineer Career Pathway",
                "plan": [
                    ("30-Day Plan", ["Learn Python or Java basics", "Complete 20 coding challenges on HackerRank"]),
                    ("60-Day Plan", ["Build a CLI project (e.g., to-do app)", "Learn Git & GitHub workflow"]),
                    ("90-Day Plan", ["Build a full-stack web application", "Contribute to an open-source project"]),
                ],
            },
            "AI Engineer": {
                "title": "AI Engineer Career Pathway",
                "plan": [
                    ("30-Day Plan", ["Learn Python & NumPy fundamentals", "Complete an intro to Machine Learning course"]),
                    ("60-Day Plan", ["Build a simple image classifier", "Study linear algebra & statistics basics"]),
                    ("90-Day Plan", ["Train a sentiment analysis model", "Publish a project on GitHub with documentation"]),
                ],
            },
            "Data Scientist": {
                "title": "Data Scientist Career Pathway",
                "plan": [
                    ("30-Day Plan", ["Learn Python & Pandas for data manipulation", "Complete a statistics fundamentals course"]),
                    ("60-Day Plan", ["Perform EDA on a Kaggle dataset", "Learn SQL for data querying"]),
                    ("90-Day Plan", ["Build a predictive model end-to-end", "Create an interactive dashboard with Plotly"]),
                ],
            },
            "Cyber Security Analyst": {
                "title": "Cyber Security Analyst Career Pathway",
                "plan": [
                    ("30-Day Plan", ["Learn networking basics (TCP/IP, DNS)", "Set up a home lab with VirtualBox"]),
                    ("60-Day Plan", ["Complete an Ethical Hacking intro course", "Practice on TryHackMe or HackTheBox"]),
                    ("90-Day Plan", ["Study for CompTIA Security+ certification", "Perform a full vulnerability assessment"]),
                ],
            },
            "Web Developer": {
                "title": "Web Developer Career Pathway",
                "plan": [
                    ("30-Day Plan", ["Master HTML & CSS fundamentals", "Build a responsive personal portfolio"]),
                    ("60-Day Plan", ["Learn JavaScript & DOM manipulation", "Build a dynamic weather app"]),
                    ("90-Day Plan", ["Learn React.js or Vue.js framework", "Deploy a full-stack project online"]),
                ],
            },
            "Game Developer": {
                "title": "Game Developer Career Pathway",
                "plan": [
                    ("30-Day Plan", ["Learn C# basics", "Complete Unity beginner tutorials"]),
                    ("60-Day Plan", ["Build a 2D platformer game", "Learn game physics & collision detection"]),
                    ("90-Day Plan", ["Design and publish a complete game prototype", "Create a game design document (GDD)"]),
                ],
            },
        }

        career = career_plans.get(career_name, {
            "title": f"{career_name} Career Pathway",
            "plan": [
                ("30-Day Plan", ["Research the field and identify key skills", "Find and start an introductory course"]),
                ("60-Day Plan", ["Complete a beginner project", "Join an online community in this field"]),
                ("90-Day Plan", ["Build a portfolio-worthy project", "Connect with professionals in this field"]),
            ],
        })

        plan = career["plan"]
        return {
            "title": career["title"],
            "roadmap_plan": plan,
            "flat_steps": [f"[{phase}] {task}" for phase, tasks in plan for task in tasks],
            "daily_tasks": ["Spend 1 hour coding", "Review logic"],
            "weekly_goals": [plan[0][1][0]],
            "monthly_goals": [phase for phase, _ in plan],
            "estimated_completion": "90 Days",
            "skill_timeline": "Beginner -> Intermediate -> Project Ready",
            "resources": ["Codecademy", "LeetCode", "YouTube"],
            "difficulty": "Beginner to Intermediate",
            "priority": "High"
        }
