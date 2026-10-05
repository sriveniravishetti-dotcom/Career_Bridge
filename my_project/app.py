import streamlit as st
from rag import generate_career_response, client

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="CareerBridge",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("🚀 CareerBridge")
st.subheader("AI-Powered Career & Skill Roadmap")

st.write(
    "Your personalized path from skills to career."
)

st.markdown(
    """
    Discover your skill gaps, build a learning roadmap,
    and prepare for your dream career.
    """
)

# -----------------------------
# Student Details
# -----------------------------
st.header("👩‍🎓 Student Details")

student_name = st.text_input(
    "Student Name",
    placeholder="Enter your name"
)

branch = st.selectbox(
    "Branch",
    ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil", "Other"]
)

year = st.selectbox(
    "Year",
    ["1st Year", "2nd Year", "3rd Year", "4th Year"]
)

career_goal = st.selectbox(
    "Dream Career",
    [
        "Not Sure - Recommend for Me",
        "Data Analyst",
        "Data Scientist",
        "AI/ML Engineer",
        "Software Developer",
        "Web Developer",
        "Cloud Engineer",
        "Cybersecurity Analyst"
    ]
)

# -----------------------------
# Skills
# -----------------------------
st.header("🧠 Your Current Skills")

skills = st.multiselect(
    "Select the skills you already know",
    [
        "Python",
        "C",
        "Java",
        "HTML",
        "CSS",
        "JavaScript",
        "SQL",
        "Excel",
        "Power BI",
        "Machine Learning",
        "Data Analytics",
        "Git & GitHub",
        "Cloud Computing"
    ]
)

# -----------------------------
# Analyze Button
# -----------------------------
if st.button("🔍 Analyze My Career Path", type="primary"):

    if not student_name:
        st.warning("Please enter your name.")

    else:
        st.success(f"Welcome, {student_name}! 🎉")

        st.subheader("🤖 AI Career Guidance")

        user_query = f"""
I am a {year} year {branch} student.
My dream career is {career_goal}.
My current skills are: {", ".join(skills)}.

First identify the skills I am missing for my dream career.

Give me personalized career guidance based on:
- My education level
- My branch
- My dream career
- My current skills
- My missing skills

For each missing skill, explain what I should learn and how I can practice it.

Also include:
1. Recommended career
2. Required skills
3. My current skills
4. My missing skills
5. Learning roadmap
6. Suggested projects
7. Internship preparation

Use only the career knowledge provided by CareerBridge.
Do not invent unsupported career information.
"""

        with st.spinner("Generating your personalized career guidance..."):
            ai_response = generate_career_response(user_query)

        st.markdown(ai_response)
        # -----------------------------
        # Career Skill Requirements
        # -----------------------------
        career_skills = {
            "Data Analyst": [
                "Python",
                "SQL",
                "Excel",
                "Power BI",
                "Data Analytics",
                "Statistics"
            ],

            "Data Scientist": [
                "Python",
                "SQL",
                "Machine Learning",
                "Data Analytics"
            ],

            "AI/ML Engineer": [
                "Python",
                "Machine Learning",
                "SQL",
                "Git & GitHub"
            ],

            "Software Developer": [
                "Python",
                "Java",
                "Git & GitHub",
                "SQL"
            ],

            "Web Developer": [
                "HTML",
                "CSS",
                "JavaScript",
                "Git & GitHub"
            ],

            "Cloud Engineer": [
                "Python",
                "Git & GitHub",
                "Cloud Computing",
                "SQL"
            ],

            "Cybersecurity Analyst": [
                "Python",
                "SQL",
                "Git & GitHub"
            ]
        }

        # -----------------------------
        # Career Recommendation
        # -----------------------------
        if career_goal == "Not Sure - Recommend for Me":

            career_scores = {}

            for career, required in career_skills.items():

                score = sum(
                    1 for skill in required
                    if skill in skills
                )

                career_scores[career] = score

            recommended_career = max(
                career_scores,
                key=career_scores.get
            )

            career_goal = recommended_career

            # Calculate Career Match Score
            total_required = len(career_skills[career_goal])
            matched_skills = career_scores[career_goal]

            match_score = round(
                (matched_skills / total_required) * 100
            )
            required_skills_for_match = career_skills[career_goal]

            matching_skills = [
                skill for skill in required_skills_for_match
                if skill in skills
            ]

            missing_recommended_skills = [
                skill for skill in required_skills_for_match
                if skill not in skills
            ]
            st.subheader("🔎 Career Skill Match")

            st.write("### ✅ Matching Skills")

            if matching_skills:
                for skill in matching_skills:
                    st.write(f"🟢 {skill}")
            else:
                st.info("No matching skills yet.")
                st.write("### 🔴 Skills to Develop")
            if missing_recommended_skills:
                for skill in missing_recommended_skills:
                    st.write(f"🔴 {skill}")
            else:
                st.success("You already have all required skills! 🎉")

            st.info(
                f"🎯 CareerBridge recommends: **{career_goal}**\n\n"
                f"📊 Career Match Score: **{match_score}%**"
            )

            st.info(
                f"🎯 Based on your current skills, "
                f"CareerBridge recommends: **{career_goal}**"
            )

        required_skills = career_skills[career_goal]

        # Find missing skills
        missing_skills = [
            skill for skill in required_skills
            if skill not in skills
        ]

        # -----------------------------
        # Results
        # -----------------------------
        st.header("📊 Career Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Target Career",
                career_goal
            )

        with col2:
            st.metric(
                "Skill Gap",
                len(missing_skills)
            )

        # -----------------------------
        # Current Skills
        # -----------------------------
        st.subheader("✅ Your Current Skills")

        if skills:
            for skill in skills:
                st.write(f"• {skill}")
        else:
            st.info("No skills selected yet.")

        # -----------------------------
        # Missing Skills
        # -----------------------------
        st.subheader("🎯 Skills You Need")

        if missing_skills:
            for skill in missing_skills:
                st.write(f"🔴 {skill}")
        else:
            st.success(
                "Excellent! You already have the required skills."
            )

        # -----------------------------
        # Learning Roadmap
        # -----------------------------
        st.header("🗺️ Personalized Learning Roadmap")

        if missing_skills:

            for index, skill in enumerate(missing_skills, 1):

                st.markdown(
                    f"""
                    ### Step {index}: Learn {skill}

                    📚 Focus on the fundamentals of **{skill}**

                    🛠️ Practice through small projects

                    💻 Add the project to your portfolio

                    🎯 Use the skill in an internship-level project
                    """
                )

        else:

            st.success(
                "You are ready to start building advanced projects "
                "and preparing for intaernships."
            )
            # -----------------------------
        # Personalized Learning Roadmap
        # -----------------------------
        st.header("🗺️ Personalized Learning Roadmap")

        skill_guidance = {
            "Excel": {
                "learn": "Learn formulas, data cleaning, sorting, filtering, pivot tables, and charts.",
                "practice": "Practice by analyzing a small sales or student dataset.",
                "project": "Build an Excel Sales Analysis Dashboard."
            },

            "Power BI": {
                "learn": "Learn Power Query, data modeling, visualizations, dashboards, and basic DAX.",
                "practice": "Create dashboards using real datasets.",
                "project": "Build a Power BI Sales Dashboard."
            },

            "Data Analytics": {
                "learn": "Learn data cleaning, exploratory data analysis, and data visualization.",
                "practice": "Analyze real datasets and identify useful insights.",
                "project": "Build an E-Commerce Data Analytics project."
            },

            "Statistics": {
                "learn": "Learn descriptive statistics, probability, correlation, and basic statistical analysis.",
                "practice": "Apply statistical concepts to real datasets.",
                "project": "Build a Student Performance Analysis project."
            },

            "Machine Learning": {
                "learn": "Learn supervised and unsupervised machine learning fundamentals.",
                "practice": "Train simple ML models using real datasets.",
                "project": "Build a Customer Churn Prediction project."
            },

            "Git & GitHub": {
                "learn": "Learn repositories, commits, branches, and GitHub basics.",
                "practice": "Upload your projects and maintain them on GitHub.",
                "project": "Create a professional GitHub project portfolio."
            },

            "SQL": {
                "learn": "Learn queries, filtering, joins, grouping, aggregation, and subqueries.",
                "practice": "Solve SQL problems using sample databases.",
                "project": "Build a database analysis project."
            },

            "Python": {
                "learn": "Strengthen Python programming and data handling.",
                "practice": "Solve coding problems and work with datasets.",
                "project": "Build a Python-based data analysis project."
            }
        }

        if missing_skills:

            for index, skill in enumerate(missing_skills, 1):

                st.markdown(f"### Step {index}: {skill}")

                if skill in skill_guidance:

                    guidance = skill_guidance[skill]

                    st.write(
                        f"📚 **What to learn:** {guidance['learn']}"
                    )

                    st.write(
                        f"🛠️ **How to practice:** {guidance['practice']}"
                    )

                    st.write(
                        f"💻 **Suggested project:** {guidance['project']}"
                    )

                    st.write(
                        "🎯 **Goal:** Add the completed project to your portfolio."
                    )

                else:

                    st.write(
                        f"📚 Learn the fundamentals of **{skill}** "
                        "and practice through projects."
                    )

        else:

            st.success(
                "🎉 You have completed the required skills! "
                "Now focus on advanced projects and internship preparation."
            )

        # -----------------------------
        # Career Preparation
        # -----------------------------
        st.header("💼 Career Preparation")

        st.write("### Recommended next steps")

        st.checkbox("Complete skill-based projects")
        st.checkbox("Build GitHub portfolio")
        st.checkbox("Create professional resume")
        st.checkbox("Practice technical interviews")
        st.checkbox("Apply for internships")

        st.success(
            "CareerBridge has created your initial career roadmap! 🚀"
        )
        st.divider()

st.divider()

st.header("💼 AI Interview Preparation")

st.write(
    "Practice interview questions and get AI-based feedback on your answers."
)

interview_type = st.selectbox(
    "Choose Interview Type",
    ["Technical Interview", "HR Interview", "Project Interview"],
    key="ai_interview_type"
)

if interview_type == "Technical Interview":

    questions = [
        "What is Python?",
        "What is SQL?",
        "What is a primary key?",
        "What is data analysis?",
        "What is the difference between HTML and CSS?"
    ]

elif interview_type == "HR Interview":

    questions = [
        "Tell me about yourself.",
        "What are your strengths?",
        "What is your weakness?",
        "Why should we hire you?",
        "Where do you see yourself in five years?"
    ]

else:

    questions = [
        "Explain your project.",
        "What technologies did you use?",
        "What was your role in the project?",
        "What challenges did you face?",
        "How does RAG help your project?"
    ]

question = st.selectbox(
    "Choose an Interview Question",
    questions,
    key="ai_interview_question"
)

st.subheader("❓ Interview Question")
st.write(question)

student_answer = st.text_area(
    "✍️ Your Answer",
    placeholder="Type your answer here...",
    height=150,
    key="student_interview_answer"
)

if st.button("🔍 Analyze My Answer", key="analyze_interview_answer"):

    if not student_answer.strip():

        st.warning("Please type your answer first.")

    else:

        evaluation_prompt = f"""
You are CareerBridge, an AI interview evaluator.

Interview Type:
{interview_type}

Interview Question:
{question}

Student Answer:
{student_answer}

Analyze the student's answer fairly.

Give the result in this format:

Result: Correct / Partially Correct / Incorrect

Score: X/10

Feedback:
Give short and clear feedback about the student's answer.

Improvement:
Explain what the student should improve or add.

Keep the evaluation beginner-friendly and useful for interview preparation.
"""

        try:
            evaluation_response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=evaluation_prompt
            )
            st.subheader("📊 AI Evaluation")
            st.write(evaluation_response.text)

        except Exception:
            st.warning(
                "⚠️ AI interview evaluation is temporarily unavailable. "
                "Please try again after a few moments."
        )
            
