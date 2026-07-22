"""
Career Data Catalog for TalentSphere Elevate.

Single-responsibility module containing the career catalog used by
the Career Explorer. Each entry provides the full detail set displayed
on career cards and in the detail view.
"""

CAREER_CATEGORIES = [
    "All",
    "Software Development",
    "Artificial Intelligence",
    "Data & Analytics",
    "Cyber Security",
]

CAREER_CATALOG = [
    {
        "name": "Software Engineer",
        "category": "Software Development",
        "icon": "💻",
        "description": (
            "Design, develop, and maintain software systems that power "
            "applications, platforms, and services used by millions. "
            "Software Engineers solve complex problems through code and "
            "collaborate with cross-functional teams to ship reliable products."
        ),
        "required_skills": [
            "Python / Java / C++",
            "Data Structures & Algorithms",
            "Version Control (Git)",
            "Problem Solving",
            "System Design Basics",
        ],
        "education_path": (
            "Bachelor's in Computer Science or related field. "
            "Self-taught paths via bootcamps and online courses are also viable."
        ),
        "career_outlook": (
            "Excellent — 25% projected growth through 2032. Median salary "
            "$124,200/year (U.S. Bureau of Labor Statistics)."
        ),
        "beginner_projects": [
            "Build a personal to-do list CLI application",
            "Create a calculator with a graphical interface",
            "Develop a simple blog with a database backend",
        ],
        "suggested_courses": [
            "CS50: Introduction to Computer Science (Harvard)",
            "Python for Everybody (University of Michigan)",
            "The Odin Project — Full Stack JavaScript",
        ],
    },
    {
        "name": "AI Engineer",
        "category": "Artificial Intelligence",
        "icon": "🤖",
        "description": (
            "Build and deploy artificial intelligence models and systems "
            "that enable machines to learn, reason, and make decisions. "
            "AI Engineers work at the intersection of software engineering "
            "and machine learning research."
        ),
        "required_skills": [
            "Python & NumPy / PyTorch",
            "Machine Learning Algorithms",
            "Linear Algebra & Statistics",
            "Data Preprocessing",
            "Model Deployment (MLOps)",
        ],
        "education_path": (
            "Bachelor's in Computer Science, AI, or Mathematics. "
            "Master's degree often preferred for research-oriented roles."
        ),
        "career_outlook": (
            "Exceptional — AI roles are among the fastest-growing in tech. "
            "Median salary $136,000/year with strong demand across industries."
        ),
        "beginner_projects": [
            "Train a handwritten digit classifier (MNIST)",
            "Build a movie recommendation system",
            "Create a chatbot using an NLP library",
        ],
        "suggested_courses": [
            "Machine Learning by Andrew Ng (Stanford / Coursera)",
            "Deep Learning Specialization (deeplearning.ai)",
            "Fast.ai — Practical Deep Learning for Coders",
        ],
    },
    {
        "name": "Data Scientist",
        "category": "Data & Analytics",
        "icon": "📊",
        "description": (
            "Extract meaningful insights from large datasets using statistical "
            "analysis, machine learning, and visualization techniques. "
            "Data Scientists turn raw data into actionable business strategies."
        ),
        "required_skills": [
            "Python & Pandas",
            "SQL & Database Querying",
            "Statistics & Probability",
            "Data Visualization (Matplotlib, Plotly)",
            "Machine Learning Basics",
        ],
        "education_path": (
            "Bachelor's in Statistics, Mathematics, Computer Science, or "
            "related field. Many professionals enter through data analytics roles."
        ),
        "career_outlook": (
            "Very strong — 35% projected growth through 2032. Median salary "
            "$103,500/year. High demand across healthcare, finance, and tech."
        ),
        "beginner_projects": [
            "Perform exploratory data analysis on a Kaggle dataset",
            "Build a sales forecasting model",
            "Create an interactive dashboard with Streamlit",
        ],
        "suggested_courses": [
            "Google Data Analytics Professional Certificate",
            "IBM Data Science Professional Certificate",
            "Statistics with Python (University of Michigan)",
        ],
    },
    {
        "name": "Cyber Security Analyst",
        "category": "Cyber Security",
        "icon": "🔒",
        "description": (
            "Protect organizations from cyber threats by monitoring networks, "
            "analyzing vulnerabilities, and implementing security measures. "
            "Cyber Security Analysts are the front line of digital defense."
        ),
        "required_skills": [
            "Networking (TCP/IP, DNS, Firewalls)",
            "Linux & Windows Administration",
            "Vulnerability Assessment",
            "Security Frameworks (NIST, ISO 27001)",
            "Incident Response",
        ],
        "education_path": (
            "Bachelor's in Cyber Security, IT, or Computer Science. "
            "Industry certifications (CompTIA Security+, CEH) are highly valued."
        ),
        "career_outlook": (
            "Excellent — 32% projected growth through 2032. Median salary "
            "$112,000/year. Critical shortage of qualified professionals."
        ),
        "beginner_projects": [
            "Set up a home lab with virtual machines",
            "Build a password strength checker tool",
            "Complete beginner rooms on TryHackMe",
        ],
        "suggested_courses": [
            "CompTIA Security+ Preparation (Professor Messer)",
            "Introduction to Cyber Security (Cisco Networking Academy)",
            "Google Cybersecurity Professional Certificate",
        ],
    },
    {
        "name": "Web Developer",
        "category": "Software Development",
        "icon": "🌐",
        "description": (
            "Build and maintain websites and web applications that deliver "
            "engaging user experiences. Web Developers work with front-end "
            "and back-end technologies to bring designs to life on the internet."
        ),
        "required_skills": [
            "HTML, CSS & JavaScript",
            "React.js / Vue.js / Angular",
            "Backend (Node.js / Django / Flask)",
            "Responsive Design",
            "REST APIs & Databases",
        ],
        "education_path": (
            "Bachelor's in Computer Science or Web Development. "
            "Bootcamps and self-taught paths are extremely common and accepted."
        ),
        "career_outlook": (
            "Strong — 16% projected growth through 2032. Median salary "
            "$80,730/year. Freelance and remote opportunities are abundant."
        ),
        "beginner_projects": [
            "Build a responsive personal portfolio website",
            "Create a weather app using a public API",
            "Develop an e-commerce product listing page",
        ],
        "suggested_courses": [
            "The Odin Project — Foundations",
            "freeCodeCamp Responsive Web Design Certification",
            "Meta Front-End Developer Professional Certificate",
        ],
    },
    {
        "name": "Game Developer",
        "category": "Software Development",
        "icon": "🎮",
        "description": (
            "Design and develop video games for PCs, consoles, and mobile "
            "devices. Game Developers combine programming, art, and storytelling "
            "to create immersive interactive entertainment experiences."
        ),
        "required_skills": [
            "C# / C++ Programming",
            "Unity or Unreal Engine",
            "Game Physics & Math",
            "3D Modeling Basics",
            "Game Design Principles",
        ],
        "education_path": (
            "Bachelor's in Game Development, Computer Science, or related field. "
            "Many successful developers are self-taught through game jams and tutorials."
        ),
        "career_outlook": (
            "Growing — the global gaming market exceeds $180B. Median salary "
            "$83,000/year. Indie development and mobile gaming create new opportunities."
        ),
        "beginner_projects": [
            "Build a 2D platformer game in Unity",
            "Create a text-based adventure RPG",
            "Design a simple puzzle game prototype",
        ],
        "suggested_courses": [
            "CS50's Introduction to Game Development (Harvard)",
            "Unity Essentials Pathway (Unity Learn)",
            "Unreal Engine 5 Beginner Tutorial (Epic Games)",
        ],
    },
]
