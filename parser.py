from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_skills(text):
    skills_db = [
        "python","java","machine learning","deep learning",
        "opencv","sql","pandas","numpy","tensorflow","pytorch",
        "nlp","data science","flask","streamlit","api"
    ]

    found = []
    text = text.lower()

    for skill in skills_db:
        if skill in text:
            found.append(skill)

    return found


def calculate_match(resume_text, job_text):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched = set(resume_skills) & set(job_skills)

    if len(job_skills) == 0:
        return 0, [], []

    score = int((len(matched) / len(job_skills)) * 100)

    missing = list(set(job_skills) - set(resume_skills))

    return score, matched, missing


def advanced_match(resume_text, job_text):
    documents = [resume_text, job_text]

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return int(similarity[0][0] * 100)