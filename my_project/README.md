# 🚀 CareerBridge – AI-Powered Career & Skill Roadmap

CareerBridge is an AI-powered career guidance application designed to help students identify their skill gaps, choose suitable career paths, build personalized learning roadmaps, and prepare for interviews.

## 🎯 Objectives

- Recommend suitable career paths based on student skills
- Identify required and missing skills
- Provide a personalized learning roadmap
- Suggest practical projects
- Support internship preparation
- Provide AI-based interview practice and answer evaluation

## 🧠 Key Features

### 👩‍🎓 Student Profile
Students can enter:
- Name
- Branch
- Academic year
- Dream career
- Current technical skills

### 🔎 Career & Skill Analysis
CareerBridge analyzes the student's current skills and identifies the skills required for the selected career.

### 🗺️ Personalized Learning Roadmap
The system provides:
- Skills to learn
- Learning guidance
- Practice suggestions
- Project recommendations

### 💼 Interview Preparation
Students can practice:
- Technical interview questions
- HR interview questions
- Project-related questions

Students can enter their own answers and receive feedback from the AI system.

## 🔥 RAG-Based Architecture

CareerBridge uses **Retrieval-Augmented Generation (RAG)**.

The system follows:

Student Input  
↓  
Career Knowledge Base  
↓  
Text Chunking  
↓  
Sentence Embeddings  
↓  
Similarity Search  
↓  
Relevant Career Information  
↓  
Gemini AI  
↓  
Personalized Career Guidance

The career information is retrieved from the project's knowledge base before generating the response.

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- Sentence Transformers
- NumPy
- RAG
- Git & GitHub

## 📂 Project Structure

```text
my_project/
│
├── knowledge_base/
│   └── career_data.txt
│
├── app.py
├── rag.py
├── requirements.txt
├── README.md
└── .gitignore