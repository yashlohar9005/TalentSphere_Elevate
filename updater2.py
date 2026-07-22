import os

def main():
    filepath = 'e:/infosys springborad internship/Project/generate_college_module_doc.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Section 1
    content = content.replace(
'''    profile_sections = [
        "Personal Information (Name, DOB, Gender, Contact, Location)",
        "Academic Information (College, University, Degree, Department, Year, CGPA/Percentage)",
        "Technical Skills (Programming Languages, Frameworks, Databases, Tools)",
        "Career Information (Interested Job Roles, Preferred Industry, Employment Type)",
        "Resume Upload (PDF / DOCX)",
        "Career Goal (Short-term, Long-term, Target Company, Dream Role)",
    ]''',
'''    profile_sections = [
        "Resume Upload",
        "Personal Information",
        "Academic Information",
        "Technical Skills",
        "Career Information",
        "Career Goals",
        "Preferred Job Roles",
        "Preferred Work Location",
        "Programming Languages",
        "Frameworks",
        "Databases",
        "Tools",
        "Certifications",
        "Achievements",
        "Languages Known",
    ]''')

    # Section 2
    content = content.replace(
'''    features = [
        "Pre-designed ATS Resume Templates",
        "Auto-formatting",
        "Personal Information Section",
        "Education Section",
        "Technical Skills Section",
        "Projects Section",
        "Internship / Experience Section",
        "Certifications Section",
        "Achievements Section",
        "Career Objective Section",
        "GitHub & LinkedIn Profile Integration",
        "ATS Resume Preview",
        "ATS Resume Analysis",
        "Download Resume as PDF/DOCX",
    ]''',
'''    features = [
        "ATS Templates",
        "Resume Preview",
        "ATS Analysis",
        "PDF Download",
        "Personal Details",
        "Education",
        "Skills",
        "Projects",
        "Internship",
        "Certifications",
        "GitHub",
        "LinkedIn",
        "Career Objective",
        "AI Resume Suggestions",
        "ATS Optimization Tips",
    ]''')

    # Section 3
    content = content.replace(
'''    evaluation_rows = [
        ("ATS Compatibility",       "85%"),
        ("Keyword Optimization",    "78%"),
        ("Technical Skills Match",  "88%"),
        ("Project Quality",         "82%"),
        ("Experience Quality",      "80%"),
        ("Resume Formatting",       "90%"),
        ("Education Profile",       "86%"),
    ]''',
'''    evaluation_rows = [
        ("ATS Compatibility",       "85%"),
        ("Resume Score",            "84%"),
        ("Keyword Optimization",    "78%"),
        ("Technical Skills",        "88%"),
        ("Projects",                "82%"),
        ("Experience",              "80%"),
        ("Formatting",              "90%"),
        ("Education",               "86%"),
        ("Overall Score",           "84%"),
    ]''')

    # Section 4
    content = content.replace(
'''    for item in [
        "Python",
        "Java",
        "C/C++",
        "Data Structures",
        "Algorithms",
        "SQL",
        "DBMS",
        "Operating Systems",
        "Computer Networks",
        "Object-Oriented Programming (OOP)",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Aptitude",
        "Logical Reasoning",
    ]:''',
'''    for item in [
        "Python",
        "Java",
        "C/C++",
        "SQL",
        "DBMS",
        "Data Structures",
        "Algorithms",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Operating Systems",
        "Computer Networks",
        "Aptitude",
        "Logical Reasoning",
    ]:''')

    content = content.replace('add_sub_heading(doc, "Test Result Example")', 'add_sub_heading(doc, "Test Scores")')
    
    # We have multiple 'add_sub_heading(doc, "AI Recommendations")'
    # we can just use replace sequentially or manually locate them.
    # Actually, Section 4 has one, Section 5 has one, Section 7 has one.
    
    # Section 5
    content = content.replace(
'''    for item in [
        "ATS Resume Score",
        "Technical Skills Assessment",
        "Coding Practice Performance",
        "Projects & Portfolio",
        "Internship / Work Experience",
        "Communication Skills",
        "Aptitude & Logical Reasoning",
        "Career Goal Alignment",
        "Skill Match with Target Job Role",
        "Certifications & Learning Progress",
    ]:''',
'''    for item in [
        "Resume Score",
        "ATS Score",
        "Coding Score",
        "Technical Skills",
        "Communication",
        "Projects",
        "Internship",
        "Certifications",
    ]:''')

    # Section 6
    content = content.replace('add_sub_heading(doc, "Sample Technical Questions")', 'add_sub_heading(doc, "Technical Interview")')
    content = content.replace('add_sub_heading(doc, "HR Interview Questions")', 'add_sub_heading(doc, "HR Interview")')
    content = content.replace('add_sub_heading(doc, "AI Evaluates")', 'add_sub_heading(doc, "Communication Evaluation")\n    add_sub_heading(doc, "Confidence Evaluation")\n    add_sub_heading(doc, "Problem Solving")\n    add_sub_heading(doc, "AI Evaluates")')
    
    content = content.replace(
'''    for label, val in [
        ("Technical Score", "84%"),
        ("Communication Score", "81%"),
        ("Confidence Score", "79%"),
        ("Problem Solving", "86%"),
        ("Overall Interview Score", "83%"),
    ]:''',
'''    for label, val in [
        ("Technical Interview Score", "84%"),
        ("HR Interview Score", "82%"),
        ("Communication Evaluation", "81%"),
        ("Confidence Evaluation", "79%"),
        ("Problem Solving", "86%"),
        ("Overall Interview Score", "83%"),
    ]:''')

    # Section 7
    content = content.replace('add_sub_heading(doc, "Missing Skills")', 'add_sub_heading(doc, "Current Skills")\n    for item in ["Python", "Java", "HTML/CSS", "JavaScript", "OOP Concepts"]:\n        add_bullet_point(doc, item)\n\n    add_sub_heading(doc, "Missing Skills")')
    content = content.replace('add_sub_heading(doc, "Strength Areas")', 'add_sub_heading(doc, "Learning Skills")\n    for item in ["React", "Node.js"]:\n        add_bullet_point(doc, item)\n\n    add_sub_heading(doc, "Strength Areas")')
    content = content.replace('Overall Skill Match:', 'Skill Match Percentage:')
    
    content = content.replace('add_sub_heading(doc, "Suggested Learning Resources")', 'add_sub_heading(doc, "Personalized Learning Roadmap")\n    for item in ["Week 1-2: Data Structures & Algorithms", "Week 3-4: Advanced SQL & Database Design", "Week 5-6: System Design Basics", "Week 7-8: React Development"]:\n        add_bullet_point(doc, item)\n\n    add_sub_heading(doc, "Suggested Learning Resources")')

    # Section 8
    content = content.replace('add_sub_heading(doc, "Recommended Platforms")', 'add_sub_heading(doc, "Internship Platforms")')
    content = content.replace('add_sub_heading(doc, "Personalized AI Suggestions")', 'add_sub_heading(doc, "AI Internship Recommendations")')

    # Section 9
    content = content.replace('add_sub_heading(doc, "Matching Factors")', 'add_sub_heading(doc, "AI Matching Factors")')
    
    content = content.replace(
'''    for item in [
        "Technical Skills",
        "Programming Languages",
        "Projects & Portfolio",
        "Resume ATS Score",
        "Coding Practice Performance",
        "Skill Gap Analysis",
        "CGPA / Academic Performance",
        "Internship / Work Experience",
        "Certifications",
        "Preferred Job Role",
        "Preferred Work Location",
        "Communication Skills",
        "Career Goals",
    ]:''',
'''    for item in [
        "Technical Skills",
        "Programming Languages",
        "Projects & Portfolio",
        "Resume ATS Score",
        "Coding Practice Performance",
        "Skill Gap Analysis",
        "CGPA / Academic Performance",
        "Internship / Work Experience",
        "Certifications",
        "Preferred Job Role",
        "Preferred Work Location",
        "Communication Skills",
        "Career Goals",
    ]:''') # same list but wait, requirement is: Software Developer, Backend Developer, Full Stack Developer, Python Developer, AI Engineer, Data Analyst, Cloud Engineer, QA Engineer, DevOps Engineer, Cyber Security Analyst
    # Ah, these are the Job Match percentages. I should replace example job matches

    content = content.replace('add_score_table(doc, job_match_rows, header_labels=("Job Role", "Match %"))', 'add_score_table(doc, job_match_rows, header_labels=("Job Role", "Job Match Percentage"))')
    content = content.replace('add_sub_heading(doc, "Example Job Matches")', 'add_sub_heading(doc, "Job Match Percentage")')
    content = content.replace('add_sub_heading(doc, "Recommended Career Paths")', 'add_sub_heading(doc, "Personalized Career Recommendations")')

    content = content.replace(
'''    job_match_rows = [
        ("Software Developer", "91%"),
        ("Python Developer", "89%"),
        ("Backend Developer", "87%"),
        ("Full Stack Developer", "85%"),
        ("AI/ML Engineer", "82%"),
        ("Data Analyst", "80%"),
        ("Cloud Engineer", "78%"),
        ("QA Engineer", "76%"),
        ("DevOps Engineer", "74%"),
        ("Cyber Security Analyst", "72%"),
    ]''',
'''    job_match_rows = [
        ("Software Developer", "91%"),
        ("Backend Developer", "89%"),
        ("Full Stack Developer", "87%"),
        ("Python Developer", "85%"),
        ("AI Engineer", "82%"),
        ("Data Analyst", "80%"),
        ("Cloud Engineer", "78%"),
        ("QA Engineer", "76%"),
        ("DevOps Engineer", "74%"),
        ("Cyber Security Analyst", "72%"),
    ]''')

    # Section 10
    content = content.replace(
'''    evaluation_summary_rows = [
        ("ATS Resume Score", "88%"),
        ("Technical Skills", "84%"),
        ("Coding Practice Score", "81%"),
        ("Project Portfolio", "87%"),
        ("Internship Readiness", "82%"),
        ("Communication Skills", "79%"),
        ("Job Match Score", "90%"),
        ("Overall Placement Readiness", "86%"),
    ]''',
'''    evaluation_summary_rows = [
        ("Resume Score", "84%"),
        ("ATS Score", "88%"),
        ("Placement Readiness", "86%"),
        ("Coding Score", "81%"),
        ("Technical Skills", "84%"),
        ("Job Match", "90%"),
    ]''')

    content = content.replace('add_sub_heading(doc, "Skills to Improve")', 'add_sub_heading(doc, "Missing Skills")')
    content = content.replace('add_sub_heading(doc, "Current Strengths")', 'add_sub_heading(doc, "Strong Skills")')
    content = content.replace('add_sub_heading(doc, "Recommended Certifications")', 'add_sub_heading(doc, "Suggested Certifications")')
    content = content.replace('add_sub_heading(doc, "Recommended Internship Companies")', 'add_sub_heading(doc, "Internship Recommendations")')
    content = content.replace('add_sub_heading(doc, "Suggested Career Path")', 'add_sub_heading(doc, "Career Path")')
    content = content.replace('add_sub_heading(doc, "30-Day AI Improvement Plan")', 'add_sub_heading(doc, "30-Day Action Plan")')

    # Section 11
    content = content.replace(
'''    for item in [
        "Placement Readiness Score: 86/100",
        "ATS Resume Score: 88%",
        "Technical Skills Score: 84%",
        "Coding Practice Score: 81%",
        "Job Match Score: 90%",
        "Active Learning Roadmaps: 3",
        "Completed Assessments: 6",
        "Resume Completion: 95%",
    ]:''',
'''    for item in [
        "Placement Readiness: 86/100",
        "ATS Resume Score: 88%",
        "Technical Skills: 84%",
        "Coding Performance: 81%",
        "Job Match: 90%",
        "Resume Completion: 95%",
        "Assessments Completed: 6",
        "Active Roadmaps: 3",
    ]:''')
    content = content.replace('add_sub_heading(doc, "Top Recommended Job Role")', 'add_sub_heading(doc, "Recommended Job Role")')
    content = content.replace('add_sub_heading(doc, "Current Focus Areas")', 'add_sub_heading(doc, "Monthly Focus Areas")')

    # Expected Outcome
    content = content.replace(
'''    for item in [
        "Build ATS-friendly professional resumes",
        "Analyze resumes using AI-powered ATS evaluation",
        "Identify technical skill gaps",
        "Improve coding performance through practice tests",
        "Receive personalized AI learning recommendations",
        "Prepare for campus placements",
        "Practice AI-powered mock interviews",
        "Track placement readiness score",
        "Discover internship opportunities",
        "Match with suitable job roles",
        "Receive career roadmap and skill development guidance",
        "Build industry-ready technical profiles",
        "Improve communication and interview skills",
        "Increase overall employability",
    ]:''',
'''    for item in [
        "AI-powered Resume Builder",
        "ATS Resume Analysis",
        "Coding Practice",
        "Skill Gap Analysis",
        "Placement Readiness",
        "Mock Interview",
        "Internship Recommendation",
        "Job Matching",
        "Personalized Learning Roadmap",
        "Career Guidance",
        "Industry Readiness",
    ]:''')

    # Final Project Statement
    content = content.replace(
'''        "\\"The College Student Module of TalentSphere Elevate is an AI-powered career development "
        "platform designed to prepare undergraduate students for internships and campus placements. "
        "The system combines student profile management, ATS-friendly resume building, AI resume "
        "evaluation, coding practice, skill gap analysis, placement readiness assessment, internship "
        "recommendations, job matching, mock interviews, and personalized career guidance into a single "
        "platform. By leveraging Artificial Intelligence, the module helps students identify their "
        "strengths, improve missing skills, build industry-ready profiles, and confidently prepare for "
        "successful careers in the software industry.\\""''',
'''        "\\"The College Student Module integrates AI-powered Resume Building, Resume Analysis, Coding Assessment, Skill Gap Analysis, Placement Readiness, Internship Recommendation, Job Matching, Mock Interviews, and Personalized Career Guidance into one platform that prepares students for placements and professional careers.\\""''')

    # Manually fix specific occurrences
    # AI Recommendations in section 4 -> AI Coding Suggestions
    # AI Recommendations in section 5 -> AI Placement Recommendations
    # AI Recommendations in section 7 -> AI Learning Recommendations
    
    parts = content.split('add_sub_heading(doc, "AI Recommendations")')
    # Let's count them. 
    # original: 
    # Section 3: AI Recommendations (1st) -> Remains "AI Recommendations"
    # Section 4: AI Recommendations (2nd) -> "AI Coding Suggestions"
    # Section 5: AI Recommendations (3rd) -> "AI Placement Recommendations"
    # Section 7: AI Recommendations (4th) -> "AI Learning Recommendations"
    
    if len(parts) == 5:
        content = parts[0] + 'add_sub_heading(doc, "AI Recommendations")' + parts[1] + 'add_sub_heading(doc, "AI Coding Suggestions")' + parts[2] + 'add_sub_heading(doc, "AI Placement Recommendations")' + parts[3] + 'add_sub_heading(doc, "AI Learning Recommendations")' + parts[4]

    with open('e:/infosys springborad internship/Project/generate_college_module_doc.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()
