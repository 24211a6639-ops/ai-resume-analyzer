import streamlit as st
import plotly.express as px
from parser import extract_text
from matcher import calculate_match, get_suggestions

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------- UI ----------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}
.glass {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Resume Analyzer (Upgraded)")

# Sidebar
menu = st.sidebar.radio("Navigation", ["Upload", "Results"])

# Inputs
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
job_desc = st.text_area("Enter Job Description")

role = st.selectbox("Select Role", ["ML Engineer", "Web Developer", "Data Analyst"])

if uploaded_file and job_desc:

    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    resume_text = extract_text(uploaded_file.name)

    score, matched, missing, strength, sem_score = calculate_match(
        resume_text, job_desc, role
    )

    suggestions = get_suggestions(missing)

    st.markdown("## 📊 ATS Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("🎯 Score", f"{score}%")
    col2.metric("📄 Resume Strength", f"{strength}%")
    col3.metric("🧠 Semantic Score", f"{sem_score}%")

    st.progress(score / 100)

    # Charts
    fig = px.bar(
        x=["Matched", "Missing"],
        y=[len(matched), len(missing)],
        color=["Matched", "Missing"]
    )
    st.plotly_chart(fig)

    # Skills
    st.markdown("### ✅ Matched Skills")
    for s in matched:
        st.markdown(f'<div class="glass">✔ {s}</div>', unsafe_allow_html=True)

    st.markdown("### ❌ Missing Skills")
    for s in missing:
        st.markdown(f'<div class="glass">✖ {s}</div>', unsafe_allow_html=True)

    # Suggestions
    st.markdown("### 💡 Suggestions")
    for s in suggestions:
        st.info(s)

    # Feedback
    if score >= 80:
        st.success("🔥 Excellent Resume")
    elif score >= 60:
        st.warning("👍 Good but improve")
    else:
        st.error("⚠️ Needs improvement")

else:
    st.info("Upload resume and enter job description")
