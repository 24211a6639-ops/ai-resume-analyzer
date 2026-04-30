import streamlit as st

import plotly.express as px
from parser import extract_text
from matcher import calculate_match, get_suggestions
import tempfile

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("TEST APP WORKING")
st.write("If you see this, deployment is fine")

file = st.file_uploader("Upload Resume", type=["pdf","docx"])
job = st.text_area("Enter Job Description")

role = st.selectbox("Role", ["ML Engineer","Web Developer","Data Analyst"])

if file and job:

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.getbuffer())
        path = tmp.name

    text = extract_text(path)

    score, matched, missing, strength, sem = calculate_match(text, job, role)

    st.metric("Score", f"{score}%")
    st.metric("Resume Strength", f"{strength}%")
    st.metric("Semantic", f"{sem}%")

    st.progress(score/100)

    fig = px.bar(x=["Matched","Missing"], y=[len(matched),len(missing)])
    st.plotly_chart(fig)

    st.subheader("Matched Skills")
    st.write(matched)

    st.subheader("Missing Skills")
    st.write(missing)

    st.subheader("Suggestions")
    for s in get_suggestions(missing):
        st.info(s)

else:
    st.info("Upload resume + job description")