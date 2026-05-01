# AI Resume Analyzer

A polished Streamlit dashboard that analyzes a resume against a job description and returns a match score, skill-gap view, ATS checks, and practical improvement suggestions.

## Features

- PDF and DOCX resume parsing
- Job-description keyword and skill matching
- Role-specific scoring for Python Developer, AI/ML Engineer, Data Analyst, Web Developer, and Backend Developer
- Interactive dashboard with score cards, Plotly gauge chart, and score breakdown chart
- Matched skills and missing skills displayed as clean visual chips
- Action plan with resume improvement suggestions
- ATS readiness checklist
- Responsive custom styling with a professional color palette

## Tech Stack

- Python
- Streamlit
- Scikit-learn
- Plotly
- PyPDF2
- python-docx

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Repository

```text
app.py              Streamlit dashboard UI
matcher.py          Skill extraction, scoring, and suggestions
parser.py           PDF/DOCX text extraction
requirements.txt    Python dependencies
README.md           Project documentation
```
