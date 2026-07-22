"""
College Student Profile module for TalentSphere Elevate.

Handles a comprehensive student profile with sections for:
  1. Personal Information
  2. Academic Information
  3. Technical Skills
  4. Career Information
  5. Resume Upload
  6. Career Goal
  7. Save / Update

One profile per user; prevents duplicates via upsert logic.
"""

import os
import json
import streamlit as st
from database import db_session, CollegeStudentProfile, User

# ───────────────────────────────────────────────────────────────────────
# Constants — dropdown / multi-select options
# ───────────────────────────────────────────────────────────────────────

GENDER_OPTIONS = ["Select", "Male", "Female", "Other"]

DEGREE_OPTIONS = [
    "Select", "B.E.", "B.Tech", "B.Sc", "BCA", "MCA", "M.Tech", "Diploma", "Other"
]

YEAR_OPTIONS = [
    "Select", "First Year", "Second Year", "Third Year", "Final Year", "Postgraduate"
]

PROGRAMMING_LANGUAGES = [
    "Python", "Java", "C", "C++", "JavaScript", "PHP", "SQL",
    "TypeScript", "Go", "Rust", "Ruby", "Kotlin", "Swift", "R",
]

FRAMEWORKS = [
    "Django", "Flask", "React", "Node.js", "Spring Boot",
    "Angular", "Vue.js", "Express.js", "FastAPI", ".NET", "Laravel",
]

DATABASES = [
    "MySQL", "PostgreSQL", "SQLite", "MongoDB",
    "Redis", "Oracle", "Firebase", "Cassandra",
]

TOOLS = [
    "Git", "GitHub", "Docker", "VS Code", "Figma",
    "Postman", "Jira", "Linux", "AWS", "Azure", "Kubernetes",
]

JOB_ROLES = [
    "Software Engineer", "Data Scientist", "AI Engineer",
    "Machine Learning Engineer", "Web Developer", "Backend Developer",
    "Frontend Developer", "Full Stack Developer",
    "Cyber Security Analyst", "Cloud Engineer", "DevOps Engineer",
    "Mobile App Developer", "Database Administrator", "QA Engineer",
    "UI/UX Designer", "Product Manager",
]

RESUME_UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "uploads", "resumes")


# ───────────────────────────────────────────────────────────────────────
# Helper utilities
# ───────────────────────────────────────────────────────────────────────

def _json_load(value: str | None, default=None):
    """Safely deserialise a JSON string; returns *default* on failure."""
    if not value:
        return default if default is not None else []
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return default if default is not None else []


def _safe_index(options: list, value: str | None, fallback: int = 0) -> int:
    """Return the list index for *value*, falling back to *fallback*."""
    if value and value in options:
        return options.index(value)
    return fallback


def _save_uploaded_resume(user_id: int, uploaded_file) -> str:
    """Persist the uploaded resume file and return its path."""
    os.makedirs(RESUME_UPLOAD_DIR, exist_ok=True)
    filename = f"{user_id}_{uploaded_file.name}"
    filepath = os.path.join(RESUME_UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filepath


# ───────────────────────────────────────────────────────────────────────
# Main render function
# ───────────────────────────────────────────────────────────────────────

def render_college_profile(user_id: int, ai_engine=None):
    """Render the College Student Profile page."""

    st.header("🎓 Student Profile")
    st.write(
        "Complete your academic and career profile to receive personalised career "
        "recommendations, resume analysis, internship suggestions, coding roadmaps, "
        "and placement guidance."
    )

    # ── Fetch existing profile ──────────────────────────────────────────
    with db_session() as session:
        profile = session.query(CollegeStudentProfile).filter_by(user_id=user_id).first()

        if profile:
            pd = {
                # Personal
                "full_name": profile.full_name or "",
                "dob": profile.dob or "",
                "gender": profile.gender or "Select",
                "mobile": profile.mobile or "",
                "email": profile.email or "",
                "city": profile.city or "",
                "state": profile.state or "",
                # Academic
                "college_name": profile.college_name or "",
                "university_name": profile.university_name or "",
                "degree": profile.degree or "Select",
                "department": profile.department or "",
                "year_of_study": profile.year_of_study or "Select",
                "semester": profile.semester or "",
                "cgpa": profile.cgpa or "",
                "percentage": profile.percentage or "",
                # Technical Skills
                "programming_languages": _json_load(profile.programming_languages),
                "frameworks": _json_load(profile.frameworks),
                "databases": _json_load(profile.databases),
                "tools": _json_load(profile.tools),
                # Career
                "interested_job_roles": _json_load(profile.interested_job_roles),
                "preferred_industry": profile.preferred_industry or "",
                "employment_type": profile.employment_type or "Select",
                "preferred_work_location": profile.preferred_work_location or "",
                # Resume
                "resume_file_path": profile.resume_file_path or "",
                # Career Goal
                "short_term_goal": profile.short_term_goal or "",
                "long_term_goal": profile.long_term_goal or "",
                "target_company": profile.target_company or "",
                "dream_role": profile.dream_role or "",
            }
            is_existing = True
        else:
            pd = {
                "full_name": "", "dob": "", "gender": "Select",
                "mobile": "", "email": "", "city": "", "state": "",
                "college_name": "", "university_name": "", "degree": "Select",
                "department": "", "year_of_study": "Select", "semester": "",
                "cgpa": "", "percentage": "",
                "programming_languages": [], "frameworks": [], "databases": [], "tools": [],
                "interested_job_roles": [], "preferred_industry": "",
                "employment_type": "Select", "preferred_work_location": "",
                "resume_file_path": "",
                "short_term_goal": "", "long_term_goal": "",
                "target_company": "", "dream_role": "",
            }
            is_existing = False

    # ── Resume upload (outside form — st.file_uploader not allowed inside forms) ──
    with st.expander("📎 Resume Upload", expanded=True):
        if pd["resume_file_path"]:
            st.success(f"📄 **Current Resume:** `{os.path.basename(pd['resume_file_path'])}`")

        uploaded_file = st.file_uploader(
            "Upload New Resume (PDF or DOCX)",
            type=["pdf", "docx"],
            key="col_resume_uploader",
            help="Upload your latest resume. Accepted formats: PDF, DOCX.",
        )

        if uploaded_file:
            st.info(f"📄 Selected: **{uploaded_file.name}** — will be saved when you click Save / Update Profile below.")
            if st.button("Extract Data with AI Parser") and ai_engine:
                with st.spinner("AI parsing resume..."):
                    parsed_data = ai_engine.resume_analyzer.parse_resume(uploaded_file.getvalue(), uploaded_file.name)
                    st.success("Extracted successfully! Please check the populated fields below.")
                    
                    if parsed_data.get("name") and not pd["full_name"]: pd["full_name"] = parsed_data["name"]
                    if parsed_data.get("email") and not pd["email"]: pd["email"] = parsed_data["email"]
                    if parsed_data.get("phone") and not pd["mobile"]: pd["mobile"] = parsed_data["phone"]
                    if parsed_data.get("college") and not pd["college_name"]: pd["college_name"] = parsed_data["college"]

    # ── Main form ───────────────────────────────────────────────────────
    with st.form("college_student_profile_form"):

        # ── Section 1 — Personal Information ────────────────────────────
        with st.expander("👤 Personal Information", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name *", value=pd["full_name"])
                gender = st.selectbox("Gender", GENDER_OPTIONS, index=_safe_index(GENDER_OPTIONS, pd["gender"]))
                mobile = st.text_input("Mobile Number", value=pd["mobile"])
                city = st.text_input("City", value=pd["city"])
            with col2:
                dob = st.date_input("Date of Birth")
                email = st.text_input("Email Address *", value=pd["email"])
                state = st.text_input("State", value=pd["state"])

        # ── Section 2 — Academic Information ────────────────────────────
        with st.expander("🏫 Academic Information", expanded=True):
            col3, col4 = st.columns(2)
            with col3:
                college_name = st.text_input("College Name *", value=pd["college_name"])
                degree = st.selectbox("Degree *", DEGREE_OPTIONS, index=_safe_index(DEGREE_OPTIONS, pd["degree"]))
                year_of_study = st.selectbox("Year of Study *", YEAR_OPTIONS, index=_safe_index(YEAR_OPTIONS, pd["year_of_study"]))
                cgpa = st.text_input("CGPA", value=pd["cgpa"])
            with col4:
                university_name = st.text_input("University Name", value=pd["university_name"])
                department = st.text_input("Department / Branch *", value=pd["department"])
                semester = st.text_input("Semester", value=pd["semester"])
                percentage = st.text_input("Percentage", value=pd["percentage"])

        # ── Section 3 — Technical Skills ────────────────────────────────
        with st.expander("💻 Technical Skills", expanded=True):
            programming_languages = st.multiselect(
                "Programming Languages",
                options=PROGRAMMING_LANGUAGES,
                default=[x for x in pd["programming_languages"] if x in PROGRAMMING_LANGUAGES],
            )
            frameworks = st.multiselect(
                "Frameworks",
                options=FRAMEWORKS,
                default=[x for x in pd["frameworks"] if x in FRAMEWORKS],
            )
            databases_sel = st.multiselect(
                "Databases",
                options=DATABASES,
                default=[x for x in pd["databases"] if x in DATABASES],
            )
            tools_sel = st.multiselect(
                "Tools",
                options=TOOLS,
                default=[x for x in pd["tools"] if x in TOOLS],
            )

        # ── Section 4 — Career Information ──────────────────────────────
        with st.expander("🎯 Career Information", expanded=True):
            interested_job_roles = st.multiselect(
                "Interested Job Roles *",
                options=JOB_ROLES,
                default=[x for x in pd["interested_job_roles"] if x in JOB_ROLES],
            )
            col5, col6 = st.columns(2)
            with col5:
                preferred_industry = st.text_input("Preferred Industry", value=pd["preferred_industry"])
                employment_options = ["Select", "Internship", "Full-time", "Both"]
                employment_type = st.selectbox(
                    "Internship / Full-time",
                    employment_options,
                    index=_safe_index(employment_options, pd["employment_type"]),
                )
            with col6:
                preferred_work_location = st.text_input("Preferred Work Location", value=pd["preferred_work_location"])

        # ── Section 6 — Career Goal ─────────────────────────────────────
        with st.expander("🚀 Career Goal", expanded=True):
            col7, col8 = st.columns(2)
            with col7:
                short_term_goal = st.text_area("Short-Term Goal", value=pd["short_term_goal"], height=100)
                target_company = st.text_input("Target Company", value=pd["target_company"])
            with col8:
                long_term_goal = st.text_area("Long-Term Goal", value=pd["long_term_goal"], height=100)
                dream_role = st.text_input("Dream Role", value=pd["dream_role"])

        # ── Section 7 — Save ────────────────────────────────────────────
        st.markdown("---")
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            save_btn = st.form_submit_button(
                label="💾 Update Profile" if is_existing else "💾 Save Profile",
                use_container_width=True,
            )
        with btn_col2:
            cancel_btn = st.form_submit_button("❌ Cancel", use_container_width=True)

    # ── Handle Cancel ───────────────────────────────────────────────────
    if cancel_btn:
        st.info("No changes were saved.")
        return

    # ── Handle Save / Update ────────────────────────────────────────────
    if save_btn:
        # ── Validation ──────────────────────────────────────────────────
        errors = []
        if not full_name.strip():
            errors.append("**Full Name** is required.")
        if not email.strip() or "@" not in email:
            errors.append("A valid **Email Address** is required.")
        if not college_name.strip():
            errors.append("**College Name** is required.")
        if degree == "Select":
            errors.append("**Degree** is required.")
        if not department.strip():
            errors.append("**Department / Branch** is required.")
        if year_of_study == "Select":
            errors.append("**Year of Study** is required.")
        if not cgpa.strip() and not percentage.strip():
            errors.append("Either **CGPA** or **Percentage** is required.")
        if not interested_job_roles:
            errors.append("At least one **Interested Job Role** must be selected.")

        if errors:
            for err in errors:
                st.error(err)
            return

        # ── Save resume file if uploaded ────────────────────────────────
        resume_path = pd["resume_file_path"]
        if uploaded_file:
            try:
                resume_path = _save_uploaded_resume(user_id, uploaded_file)
            except Exception as e:
                st.error(f"Failed to save resume file: {e}")
                return

        # ── Persist to database ─────────────────────────────────────────
        try:
            with db_session() as session:
                db_profile = session.query(CollegeStudentProfile).filter_by(user_id=user_id).first()
                if not db_profile:
                    db_profile = CollegeStudentProfile(user_id=user_id)
                    session.add(db_profile)

                # Personal Information
                db_profile.full_name = full_name.strip()
                db_profile.dob = str(dob)
                db_profile.gender = gender if gender != "Select" else None
                db_profile.mobile = mobile.strip()
                db_profile.email = email.strip()
                db_profile.city = city.strip()
                db_profile.state = state.strip()

                # Academic Information
                db_profile.college_name = college_name.strip()
                db_profile.university_name = university_name.strip()
                db_profile.degree = degree if degree != "Select" else None
                db_profile.department = department.strip()
                db_profile.year_of_study = year_of_study if year_of_study != "Select" else None
                db_profile.semester = semester.strip()
                db_profile.cgpa = cgpa.strip()
                db_profile.percentage = percentage.strip()

                # Technical Skills (JSON)
                db_profile.programming_languages = json.dumps(programming_languages)
                db_profile.frameworks = json.dumps(frameworks)
                db_profile.databases = json.dumps(databases_sel)
                db_profile.tools = json.dumps(tools_sel)

                # Career Information
                db_profile.interested_job_roles = json.dumps(interested_job_roles)
                db_profile.preferred_industry = preferred_industry.strip()
                db_profile.employment_type = employment_type if employment_type != "Select" else None
                db_profile.preferred_work_location = preferred_work_location.strip()

                # Resume
                db_profile.resume_file_path = resume_path

                # Career Goal
                db_profile.short_term_goal = short_term_goal.strip()
                db_profile.long_term_goal = long_term_goal.strip()
                db_profile.target_company = target_company.strip()
                db_profile.dream_role = dream_role.strip()

                # Keep User table's full_name in sync
                user = session.query(User).filter_by(id=user_id).first()
                if user and full_name.strip():
                    user.full_name = full_name.strip()

            st.success("✅ Profile Saved Successfully")
            st.balloons()
            st.rerun()

        except Exception as e:
            st.error(f"Failed to save profile: {e}")
