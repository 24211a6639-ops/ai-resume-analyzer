import streamlit as st
from extractor import extract_text
from parser import extract_skills, calculate_match, advanced_match

st.title("AI Resume Analyzer 🚀")
st.markdown("### 🔍 Smart Resume Analyzer with AI Matching")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description here")

if uploaded_file:
    st.success("File uploaded successfully!")

    text = extract_text(uploaded_file) or ""

    st.subheader("Extracted Text:")
    st.write(text[:500])

    skills = extract_skills(text)

    st.subheader("Extracted Skills:")
    st.write(skills)

    if job_desc:
        score, matched, missing = calculate_match(text, job_desc)
        ai_score = advanced_match(text, job_desc)

        st.subheader("Keyword Match Score:")
        st.success(f"{score}%")

        st.subheader("AI Semantic Match Score:")
        st.info(f"{ai_score}%")

        st.subheader("Matched Skills:")
        st.write(list(matched))

        st.subheader("Missing Skills:")
        st.write(missing)

        if missing:
            st.subheader("Recommended Skills to Learn:")
            for skill in missing:
                st.write(f"👉 Learn {skill}")

        st.download_button("Download Skills Report", str(skills))