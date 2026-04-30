from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

skills_db = [
    "python","java","sql","machine learning","deep learning",
    "html","css","javascript","react","pandas","numpy"
]

role_skills = {
    "ML Engineer": ["python", "machine learning"],
    "Web Developer": ["html", "css", "javascript", "react"],
    "Data Analyst": ["python", "sql", "pandas"]
}

def extract_skills(text):
    return [s for s in skills_db if s in text]

def semantic_score(resume, job):
    vec = TfidfVectorizer().fit_transform([resume, job])
    sim = cosine_similarity(vec[0], vec[1])[0][0]
    return round(sim * 100, 2)

def calculate_match(resume, job, role):
    r_skills = extract_skills(resume)
    j_skills = extract_skills(job)

    role_req = role_skills.get(role, [])

    matched = list(set(r_skills) & set(j_skills + role_req))
    missing = list(set(j_skills + role_req) - set(r_skills))

    skill_score = (len(matched) / max(len(j_skills + role_req),1)) * 70
    sem = semantic_score(resume, job) * 0.3

    word_count = len(resume.split())
    strength = min((word_count / 500) * 100, 100)

    final = round(skill_score + sem, 2)

    return final, matched, missing, round(strength,2), round(sem,2)

def get_suggestions(missing):
    return [f"Improve {s} with projects" for s in missing]