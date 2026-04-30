import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy safely
try:
    nlp = spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

skills_db = [
    "python", "java", "sql", "machine learning", "deep learning",
    "nlp", "data science", "tensorflow", "pytorch",
    "html", "css", "javascript", "react",
    "flask", "django", "streamlit",
    "aws", "docker", "git"
]

# Extract skills
def extract_skills(text):
    text = text.lower()
    found = []

    for skill in skills_db:
        if skill in text:
            found.append(skill)

    return list(set(found))

# Match score
def calculate_match(resume_text, job_text):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    if len(job_skills) == 0:
        return 0, matched, missing, 0

    skill_score = (len(matched) / len(job_skills)) * 70

    word_count = len(resume_text.split())
    resume_score = min((word_count / 500) * 30, 30)

    total_score = min(skill_score + resume_score, 100)

    return round(total_score, 2), matched, missing, round(resume_score, 2)

# Suggestions
def get_suggestions(missing):
    suggestions = []
    for skill in missing:
        suggestions.append(f"👉 Learn {skill}")
    return suggestions

# Semantic similarity
def semantic_similarity(text1, text2):
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    sim = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    return round(sim * 100, 2)