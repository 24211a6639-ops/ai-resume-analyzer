# matcher.py

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Skill database
skills_db = [
    "python", "java", "c++", "sql", "mysql", "mongodb",
    "machine learning", "deep learning", "nlp", "data science",
    "tensorflow", "pytorch", "pandas", "numpy",
    "html", "css", "javascript", "react",
    "flask", "django", "streamlit",
    "aws", "docker", "kubernetes",
    "git", "github", "api"
]

# Extract skills
def extract_skills(text):
    text = text.lower()
    found = []

    for skill in skills_db:
        if skill in text:
            found.append(skill)

    return list(set(found))


# Calculate match
def calculate_match(resume_text, job_text):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    if len(job_skills) == 0:
        return 0, matched, missing

    score = round((len(matched) / len(job_skills)) * 100, 2)

    return score, matched, missing


# Suggestions
def get_suggestions(missing_skills):
    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"👉 Learn {skill} to improve your resume")

    return suggestions


# Optional semantic similarity
def semantic_similarity(text1, text2):
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()

    sim = cosine_similarity([vectors[0]], [vectors[1]])[0][0]

    return round(sim * 100, 2)