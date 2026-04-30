# app.py

import streamlit as st
from parser import extract_text
from matcher import calculate_match, get_suggestions

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# Title
st.title("📄 AI Resume Analyzer")

# Upload resume
uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

# Job description
job_desc = st.text_area("Enter Job Description")

if uploaded_file is not None and job_desc:

    # Save file temporarily
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract text
    resume_text = extract_text(uploaded_file.name)

    if not resume_text.strip():
        st.error("❌ Failed to extract text from resume")
        st.stop()

    # Calculate match
    score, matched, missing = calculate_match(resume_text, job_desc)

    suggestions = get_suggestions(missing)

    # Output
    st.markdown("## 📊 Match Result")

    st.progress(score / 100)

    st.metric("🎯 Match Score", f"{score}%")

    # Matched skills
    st.markdown("### ✅ Matched Skills")
    for skill in matched:
        st.success(skill)

    # Missing skills
    st.markdown("### ❌ Missing Skills")
    for skill in missing:
        st.error(skill)

    # Suggestions
    st.markdown("### 💡 Suggestions")
    for s in suggestions:
        st.info(s)

else:
    st.info("📌 Upload resume and enter job description")
