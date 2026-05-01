from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS_DB = [
    "python",
    "java",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "streamlit",
    "flask",
    "django",
    "fastapi",
    "rest api",
    "api integration",
    "git",
    "github",
    "pandas",
    "numpy",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "nlp",
    "opencv",
    "tesseract",
    "ocr",
    "data analysis",
    "data visualization",
    "plotly",
    "logging",
    "error handling",
    "validation",
    "cli",
    "oop",
]

ROLE_SKILLS = {
    "Python Developer": [
        "python",
        "oop",
        "rest api",
        "api integration",
        "git",
        "github",
        "logging",
        "error handling",
        "validation",
        "cli",
    ],
    "AI/ML Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "nlp",
        "pandas",
        "numpy",
        "scikit-learn",
    ],
    "Data Analyst": ["python", "sql", "pandas", "numpy", "data analysis", "data visualization"],
    "Web Developer": ["html", "css", "javascript", "react", "api integration", "git"],
    "Backend Developer": ["python", "flask", "django", "fastapi", "rest api", "sql", "logging"],
}


def normalize_text(text):
    return (text or "").lower()


def unique_preserve_order(items):
    seen = set()
    unique_items = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)
    return unique_items


def extract_skills(text):
    normalized = normalize_text(text)
    return [skill for skill in SKILLS_DB if skill in normalized]


def semantic_score(resume, job):
    if not resume.strip() or not job.strip():
        return 0.0

    vec = TfidfVectorizer(stop_words="english").fit_transform([resume, job])
    sim = cosine_similarity(vec[0], vec[1])[0][0]
    return float(round(sim * 100, 2))


def get_suggestions(missing):
    suggestions = []
    for skill in missing[:6]:
        suggestions.append(
            {
                "title": f"Add evidence for {skill.title()}",
                "body": (
                    f"Add one project bullet, coursework line, or tool mention that truthfully shows "
                    f"how you used {skill}. Keep it specific and measurable."
                ),
            }
        )

    if not suggestions:
        return []

    suggestions.append(
        {
            "title": "Mirror the job description",
            "body": "Use the same role keywords where they honestly match your experience, especially in project bullets.",
        }
    )
    return suggestions


def analyze_resume(resume, job, role):
    resume_text = normalize_text(resume)
    job_text = normalize_text(job)
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)
    required_skills = unique_preserve_order(job_skills + ROLE_SKILLS.get(role, []))

    matched = [skill for skill in required_skills if skill in resume_skills]
    missing = [skill for skill in required_skills if skill not in resume_skills]

    skill_score = round((len(matched) / max(len(required_skills), 1)) * 100, 2)
    sem_score = semantic_score(resume_text, job_text)
    word_count = len(resume_text.split())
    resume_strength = round(min((word_count / 500) * 100, 100), 2)
    final_score = float(round((skill_score * 0.55) + (sem_score * 0.3) + (resume_strength * 0.15), 2))

    return {
        "match_score": final_score,
        "skill_score": skill_score,
        "semantic_score": sem_score,
        "resume_strength": resume_strength,
        "word_count": word_count,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": get_suggestions(missing),
        "resume_text": resume_text,
    }


def calculate_match(resume, job, role):
    analysis = analyze_resume(resume, job, role)
    return (
        analysis["match_score"],
        analysis["matched_skills"],
        analysis["missing_skills"],
        analysis["resume_strength"],
        analysis["semantic_score"],
    )
