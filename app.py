import streamlit as st
import plotly.express as px
from parser import extract_text
from matcher import calculate_match, get_suggestions

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------- MODERN UI ----------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

.glass {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

h1, h2, h3 {
    color: #38bdf8;
}

.stButton>button {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("📄 AI Resume Analyzer")

# ---------- INPUT ----------
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
job_desc = st.text_area("Enter Job Description")

# ---------- MAIN ----------
if uploaded_file and job_desc:

    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    resume_text = extract_text(uploaded_file.name)

    score, matched, missing = calculate_match(resume_text, job_desc)
    suggestions = get_suggestions(missing)

    # ---------- RESULT ----------
    st.markdown("## 📊 Match Result")

    st.progress(score / 100)

    col1, col2, col3 = st.columns(3)

    col1.metric("🎯 Score", f"{score}%")
    col2.metric("📄 Skills Found", len(matched))
    col3.metric("❌ Missing", len(missing))

    # ---------- MATCHED ----------
    st.markdown("### ✅ Matched Skills")
    for skill in matched:
        st.markdown(f'<div class="glass">✅ {skill}</div>', unsafe_allow_html=True)

    # ---------- MISSING ----------
    st.markdown("### ❌ Missing Skills")
    for skill in missing:
        st.markdown(f'<div class="glass">🔴 {skill}</div>', unsafe_allow_html=True)

    # ---------- SUGGESTIONS ----------
    st.markdown("### 💡 Suggestions")
    for s in suggestions:
        st.markdown(f'<div class="glass">💡 {s}</div>', unsafe_allow_html=True)

    # ---------- CHART ----------
    data = {
        "Category": ["Matched", "Missing"],
        "Count": [len(matched), len(missing)]
    }

    fig = px.pie(
        names=data["Category"],
        values=data["Count"],
        color_discrete_sequence=["#22c55e", "#ef4444"]
    )

    st.plotly_chart(fig)

    # ---------- STATUS ----------
    if score >= 80:
        st.success("🔥 Excellent Resume – Job Ready")
    elif score >= 60:
        st.warning("👍 Good Resume – Improve More")
    else:
        st.error("⚠️ Needs Improvement")

else:
    st.info("📌 Upload resume and enter job description")
