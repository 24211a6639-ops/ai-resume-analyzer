from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Skill database
skills_db = [
    "python", "java", "c++", "sql", "mysql", "mongodb",
    "machine learning", "deep learning", "nlp", "data science",
    "tensorflow", "pytorch", "pandas", "numpy",
    "html", "css", "javascript", "react",
    "flask", "django", "streamlit",
    "aws", "docker", "git", "github"
]

# Role-based skills
role_skills = {
    "ML Engineer": ["python", "machine learning", "tensorflow", "pytorch"],
    "Web Developer": ["html", "css", "javascript", "react"],
    "Data Analyst": ["python", "sql", "pandas"]
}

# Extract skills
def extract_skills(text):
    found = []
    for skill in skills_db:
        if skill in text:
            found.append(skill)
    return list(set(found))

# Semantic similarity (REAL NLP)
def semantic_score(resume_text, job_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_text])
    sim = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(sim * 100, 2)

# Main matching
def calculate_match(resume_text, job_text, role):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    # Role-based skills
    role_required = role_skills.get(role, [])

    matched = list(set(resume_skills) & set(job_skills + role_required))
    missing = list(set(job_skills + role_required) - set(resume_skills))

    if len(job_skills) == 0:
        return 0, matched, missing, 0, 0

    # Skill score (70%)
    skill_score = (len(matched) / len(job_skills + role_required)) * 70

    # Semantic score (30%)
    sem_score = semantic_score(resume_text, job_text) * 0.3

    # Resume strength
    word_count = len(resume_text.split())
    resume_strength = min((word_count / 500) * 100, 100)

    final_score = round(skill_score + sem_score, 2)

    return final_score, matched, missing, round(resume_strength, 2), round(sem_score, 2)

# Suggestions
def get_suggestions(missing_skills):
    learning_map = {
        "sql": "Build SQL projects (joins, queries, DB design)",
        "python": "Add Python projects (automation, ML)",
        "react": "Build frontend apps using React",
        "machine learning": "Create ML models (classification/regression)"
    }

    suggestions = []
    for skill in missing_skills:
        if skill in learning_map:
            suggestions.append(f"👉 {learning_map[skill]}")
        else:
            suggestions.append(f"👉 Learn {skill}")

    return suggestions