import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------
# Load spaCy model safely
# ---------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


# ---------------------------
# Skills database
# ---------------------------
skills_db = [
    "python", "java", "c++", "sql", "mysql", "mongodb",
    "machine learning", "deep learning", "nlp", "data science",
    "tensorflow", "pytorch", "pandas", "numpy",
    "html", "css", "javascript", "react",
    "flask", "django", "streamlit",
    "aws", "docker", "kubernetes",
    "git", "github", "api"
]


# ---------------------------
# Extract skills using NLP
# ---------------------------
def extract_skills(text):
    text = text.lower()
    doc = nlp(text)

    found = set()

    # Direct matching
    for skill in skills_db:
        if skill in text:
            found.add(skill)

    # NLP token matching
    for token in doc:
        for skill in skills_db:
            if token.text in skill or skill in token.text:
                found.add(skill)

    return list(found)


# ---------------------------
# Calculate match score
# ---------------------------
def calculate_match(resume_text, job_text):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    # Avoid division error
    if len(job_skills) == 0:
        return 0, matched, missing, 0

    # Skill score (70%)
    skill_score = (len(matched) / len(job_skills)) * 70

    # Resume strength (30%)
    word_count = len(resume_text.split())
    resume_score = min((word_count / 500) * 30, 30)

    total_score = min(skill_score + resume_score, 100)

    return round(total_score, 2), matched, missing, round(resume_score, 2)


# ---------------------------
# Suggestions
# ---------------------------
def get_suggestions(missing_skills):
    learning_map = {
        "python": "Practice Python projects (automation, ML)",
        "sql": "Learn joins, queries, and DB design",
        "machine learning": "Build ML models (classification, regression)",
        "deep learning": "Learn CNN, NLP basics",
        "aws": "Learn EC2, S3 basics",
        "docker": "Understand containerization",
        "react": "Build frontend apps using React"
    }

    suggestions = []

    for skill in missing_skills:
        if skill in learning_map:
            suggestions.append(f"👉 {learning_map[skill]}")
        else:
            suggestions.append(f"👉 Learn {skill}")

    return suggestions


# ---------------------------
# Optional: Semantic similarity (advanced)
# ---------------------------
def semantic_similarity(text1, text2):
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()

    sim = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    return round(sim * 100, 2)