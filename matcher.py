# matcher.py

import spacy

nlp = spacy.load("en_core_web_sm")

skills_db = [
    "python", "java", "c++", "sql", "mysql", "mongodb",
    "machine learning", "deep learning", "natural language processing",
    "data science", "tensorflow", "pytorch", "pandas", "numpy",
    "html", "css", "javascript", "react",
    "flask", "django", "streamlit",
    "aws", "docker", "kubernetes",
    "git", "github", "api"
]


def extract_skills(text):
    text = text.lower()
    doc = nlp(text)

    found = set()

    for skill in skills_db:
        if skill in text:
            found.add(skill)

    for token in doc:
        for skill in skills_db:
            if token.text in skill or skill in token.text:
                found.add(skill)

    return list(found)


def calculate_match(resume_text, job_text):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    if len(job_skills) == 0:
        return 0, matched, missing, 0

    # Skill score (70%)
    skill_score = (len(matched) / len(job_skills)) * 70

    # Resume strength (30%)
    word_count = len(resume_text.split())
    resume_score = min((word_count / 500) * 30, 30)

    total_score = min(skill_score + resume_score, 100)

    return round(total_score, 2), matched, missing, round(resume_score, 2)


def get_suggestions(missing_skills):
    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"👉 Learn {skill} to improve your resume")

    return suggestions