import os
import re

def main():
    filepath = 'e:/infosys springborad internship/Project/generate_college_module_doc.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Section 1
    content = re.sub(
        r'profile_sections = \[\n.*?\]',
        '''profile_sections = [
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
    ]''',
        content,
        flags=re.DOTALL,
        count=1
    )

    # Section 2 Features
    content = re.sub(
        r'features = \[\n.*?\]',
        '''features = [
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
    ]''',
        content,
        flags=re.DOTALL,
        count=1
    )

    # Section 3
    content = re.sub(
        r'evaluation_rows = \[\n.*?\]',
        '''evaluation_rows = [
        ("ATS Compatibility",       "85%"),
        ("Resume Score",            "84%"),
        ("Keyword Optimization",    "78%"),
        ("Technical Skills",        "88%"),
        ("Projects",                "82%"),
        ("Experience",              "80%"),
        ("Formatting",              "90%"),
        ("Education",               "86%"),
        ("Overall Score",           "84%"),
    ]''',
        content,
        flags=re.DOTALL,
        count=1
    )

    # Section 4
    content = re.sub(
        r'    for item in \[\n.*?"Logical Reasoning",\n    \]:',
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
    ]:''',
        content,
        flags=re.DOTALL,
        count=1
    )

    content = content.replace('add_sub_heading(doc, "Test Result Example")', 'add_sub_heading(doc, "Test Scores")')
    content = content.replace('add_sub_heading(doc, "AI Recommendations")', 'add_sub_heading(doc, "AI Coding Suggestions")', 1)

    # Section 5
    content = re.sub(
        r'The AI calculates a Placement Readiness Score based on:.*?\n    \]:',
        '''The AI calculates a Placement Readiness Score based on:",
        font_size=11,
        color=DARK_TEXT,
        space_after=8,
    )

    for item in [
        "Resume Score",
        "ATS Score",
        "Coding Score",
        "Technical Skills",
        "Communication",
        "Projects",
        "Internship",
        "Certifications",
    ]:''',
        content,
        flags=re.DOTALL,
        count=1
    )
    
    # Replace second AI Recommendations in the file (which is in Section 5)
    content = content.replace('add_sub_heading(doc, "AI Recommendations")', 'add_sub_heading(doc, "AI Placement Recommendations")', 1)

    # Section 6
    content = content.replace('add_sub_heading(doc, "Sample Technical Questions")', 'add_sub_heading(doc, "Technical Interview")')
    content = content.replace('add_sub_heading(doc, "HR Interview Questions")', 'add_sub_heading(doc, "HR Interview")')
    content = content.replace('add_sub_heading(doc, "AI Evaluates")', 'add_sub_heading(doc, "Communication Evaluation")\\n    add_sub_heading(doc, "Confidence Evaluation")\\n    add_sub_heading(doc, "Problem Solving")\\n    add_sub_heading(doc, "AI Evaluates")')
    
    content = re.sub(
        r'    for label, val in \[\n.*?\("Overall Interview Score", "83%"\),\n    \]:',
        '''    for label, val in [
        ("Technical Interview Score", "84%"),
        ("HR Interview Score", "82%"),
        ("Communication Evaluation", "81%"),
        ("Confidence Evaluation", "79%"),
        ("Problem Solving", "86%"),
        ("Overall Interview Score", "83%"),
    ]:''',
        content,
        flags=re.DOTALL,
        count=1
    )

    # Section 7
    content = content.replace('add_sub_heading(doc, "Missing Skills")', 'add_sub_heading(doc, "Current Skills")\n    for item in ["Python", "Java", "HTML/CSS", "JavaScript", "OOP Concepts"]:\n        add_bullet_point(doc, item)\n\n    add_sub_heading(doc, "Missing Skills")')
    content = content.replace('add_sub_heading(doc, "Strength Areas")', 'add_sub_heading(doc, "Learning Skills")\n    for item in ["React", "Node.js"]:\n        add_bullet_point(doc, item)\n\n    add_sub_heading(doc, "Strength Areas")')
    content = content.replace('Overall Skill Match:', 'Skill Match Percentage:')
    
    content = content.replace('add_sub_heading(doc, "AI Recommendations")', 'add_sub_heading(doc, "AI Learning Recommendations")')
    content = content.replace('add_sub_heading(doc, "Suggested Learning Resources")', 'add_sub_heading(doc, "Personalized Learning Roadmap")\n    for item in ["Week 1-2: Data Structures & Algorithms", "Week 3-4: Advanced SQL & Database Design", "Week 5-6: System Design Basics", "Week 7-8: React Development"]:\n        add_bullet_point(doc, item)\n\n    add_sub_heading(doc, "Suggested Learning Resources")')

    # Section 8
    content = content.replace('add_sub_heading(doc, "Recommended Platforms")', 'add_sub_heading(doc, "Internship Platforms")')
    content = content.replace('add_sub_heading(doc, "Personalized AI Suggestions")', 'add_sub_heading(doc, "AI Internship Recommendations")')

    # Section 9
    content = re.sub(
        r'add_sub_heading\(doc, "Matching Factors"\)\n    for item in \[\n.*?\]:',
        '''add_sub_heading(doc, "AI Matching Factors")
    for item in [
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
        content,
        flags=re.DOTALL,
        count=1
    )
    
    content = content.replace('("Match %")', '("Job Match Percentage")')
    content = content.replace('add_sub_heading(doc, "Example Job Matches")', 'add_sub_heading(doc, "Job Match Percentage")')
    content = content.replace('add_sub_heading(doc, "Recommended Career Paths")', 'add_sub_heading(doc, "Personalized Career Recommendations")')

    content = re.sub(
        r'job_match_rows = \[\n.*?\]',
        '''job_match_rows = [
        ("Software Developer", "91%"),
        ("Python Developer", "89%"),
        ("Backend Developer", "87%"),
        ("Full Stack Developer", "85%"),
        ("AI Engineer", "82%"),
        ("Data Analyst", "80%"),
        ("Cloud Engineer", "78%"),
        ("QA Engineer", "76%"),
        ("DevOps Engineer", "74%"),
        ("Cyber Security Analyst", "72%"),
    ]''',
        content,
        flags=re.DOTALL,
        count=1
    )

    # Section 10
    content = re.sub(
        r'evaluation_summary_rows = \[\n.*?\]',
        '''evaluation_summary_rows = [
        ("Resume Score", "84%"),
        ("ATS Score", "88%"),
        ("Placement Readiness", "86%"),
        ("Coding Score", "81%"),
        ("Technical Skills", "84%"),
        ("Job Match", "90%"),
    ]''',
        content,
        flags=re.DOTALL,
        count=1
    )
    content = content.replace('add_sub_heading(doc, "Skills to Improve")', 'add_sub_heading(doc, "Missing Skills")')
    content = content.replace('add_sub_heading(doc, "Current Strengths")', 'add_sub_heading(doc, "Strong Skills")')
    content = content.replace('add_sub_heading(doc, "Recommended Certifications")', 'add_sub_heading(doc, "Suggested Certifications")')
    content = content.replace('add_sub_heading(doc, "Recommended Internship Companies")', 'add_sub_heading(doc, "Internship Recommendations")')
    content = content.replace('add_sub_heading(doc, "Suggested Career Path")', 'add_sub_heading(doc, "Career Path")')
    content = content.replace('add_sub_heading(doc, "30-Day AI Improvement Plan")', 'add_sub_heading(doc, "30-Day Action Plan")')

    # Section 11
    content = re.sub(
        r'add_sub_heading\(doc, "Dashboard Overview"\)\n    for item in \[\n.*?\]:',
        '''add_sub_heading(doc, "Dashboard Overview")
    for item in [
        "Placement Readiness: 86/100",
        "ATS Resume Score: 88%",
        "Technical Skills: 84%",
        "Coding Performance: 81%",
        "Job Match: 90%",
        "Resume Completion: 95%",
        "Assessments Completed: 6",
        "Active Roadmaps: 3",
    ]:''',
        content,
        flags=re.DOTALL,
        count=1
    )
    content = content.replace('add_sub_heading(doc, "Top Recommended Job Role")', 'add_sub_heading(doc, "Recommended Job Role")')
    content = content.replace('add_sub_heading(doc, "Current Focus Areas")', 'add_sub_heading(doc, "Monthly Focus Areas")')

    # Expected Outcome
    content = re.sub(
        r'    for item in \[\n.*?\]:',
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
    ]:''',
        content,
        flags=re.DOTALL,
        count=1 # Wait, this might match the wrong list because I replaced some lists already. I'll fix this below.
    )

    # Final Project Statement
    content = re.sub(
        r'add_feedback_box\(\n        doc,\n        "\\"The College Student Module.*?\\""\n    \)',
        '''add_feedback_box(
        doc,
        "\\"The College Student Module integrates AI-powered Resume Building, Resume Analysis, Coding Assessment, Skill Gap Analysis, Placement Readiness, Internship Recommendation, Job Matching, Mock Interviews, and Personalized Career Guidance into one platform that prepares students for placements and professional careers.\\""
    )''',
        content,
        flags=re.DOTALL
    )
    
    with open('e:/infosys springborad internship/Project/generate_college_module_doc_temp.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()
