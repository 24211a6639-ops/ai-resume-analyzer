# AI Resume Analyzer

![build](https://img.shields.io/badge/build-passing-brightgreen)
![license](https://img.shields.io/badge/license-MIT-yellow)
![python](https://img.shields.io/badge/python-3.8%2B-blue)
![streamlit](https://img.shields.io/badge/streamlit-app-red)

A polished Streamlit dashboard that analyzes a resume against a job description and returns a match score, skill-gap view, ATS checks, and practical improvement suggestions.

## 🚀 Live Demo

👉 **[Click here to try the app](https://ai-resume-analyzer-4r7gp52twb247p2whw58sv.streamlit.app)**

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

**AI Resume Analyzer** is an intelligent Streamlit dashboard that compares your resume with any job description and gives you a detailed analysis — including a match score, missing skills, ATS readiness, and actionable improvement tips.

---

## Features

- 📄 **PDF and DOCX Resume Parsing** — Upload your resume in any common format
- 🎯 **Job Description Matching** — Keyword and skill matching against the job description
- 📊 **Role-Specific Scoring** — Tailored scoring for:
  - Python Developer
  - AI/ML Engineer
  - Data Analyst
  - Web Developer
  - Backend Developer
- 📈 **Interactive Dashboard** — Score cards, Plotly gauge chart, and score breakdown chart
- ✅ **Matched & Missing Skills** — Displayed as clean visual chips
- 💡 **Action Plan** — Resume improvement suggestions
- 🤖 **ATS Readiness Checklist** — Make sure recruiters can find you
- 🎨 **Responsive UI** — Professional custom styling and color palette

---

## Demo

### 🔗 Try it live:
**[https://ai-resume-analyzer-4r7gp52twb247p2whw58sv.streamlit.app](https://ai-resume-analyzer-4r7gp52twb247p2whw58sv.streamlit.app)**

### How it works:
1. Upload your resume (PDF or DOCX)
2. Paste the job description
3. Select your target role
4. Get your match score, skill gaps, ATS check & improvement tips instantly!

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core language |
| Streamlit | Web dashboard UI |
| Scikit-learn | Skill matching & scoring |
| Plotly | Interactive charts |
| PyPDF2 | PDF parsing |
| python-docx | DOCX parsing |

---

## Installation

### Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/24211a6639-ops/ai-resume-analyzer.git
cd ai-resume-analyzer

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## Usage

1. Open the app (live or locally)
2. **Upload** your resume in PDF or DOCX format
3. **Paste** the job description in the text box
4. **Select** your target role from the dropdown
5. Click **Analyze** and get your results instantly!

---

## Project Structure

```
ai-resume-analyzer/
│
├── app.py              # Streamlit dashboard UI
├── matcher.py          # Skill extraction, scoring & suggestions
├── parser.py           # PDF/DOCX text extraction
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Git ignore rules
```

---

## Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the [MIT License](LICENSE).

---

> Made with ❤️ by [24211a6639-ops](https://github.com/24211a6639-ops) • [🚀 Try the Live App](https://ai-resume-analyzer-4r7gp52twb247p2whw58sv.streamlit.app)
