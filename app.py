import streamlit as st
import plotly.express as px
from myparser import extract_text   # or parser.py if you didn't rename
from matcher import calculate_match, get_suggestions

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------------- THEME ----------------
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

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "📌 Navigation",
    ["📤 Upload", "📊 Results", "📈 Insights"]
)

# ---------------- HEADER ----------------
st.markdown("""
<div class="glass">
<h1>🚀 AI Resume Analyzer</h1>
<p>Analyze your resume like an ATS system and improve your chances.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])

with col2:
    job_desc = st.text_area("💼 Enter Job Description")

# ---------------- PROCESSING ----------------
if uploaded_file and job_desc:

    # Save file
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Analyzing your resume..."):
        resume_text = extract_text(uploaded_file.name)

    # Debug
    st.write("🔍 Extracted length:", len(resume_text))

    if not resume_text.strip():
        st.error("❌ Resume extraction failed")
        st.stop()

    # Calculate
    score, matched, missing, resume_score = calculate_match(resume_text, job_desc)
    suggestions = get_suggestions(missing)

    # ---------------- RESULTS ----------------
    if menu == "📊 Results":

        st.markdown("## 📊 Match Result")

        # Progress bar
        st.progress(score / 100)

        # Metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🎯 Match Score", f"{score}%")

        with col2:
            st.metric("📄 Resume Strength", f"{resume_score}%")

        with col3:
            st.metric("🧠 Skills Found", len(matched))

        # Status
        if score >= 80:
            st.markdown("🔥 **Excellent Resume – Job Ready**")
        elif score >= 60:
            st.markdown("👍 **Good Resume – Improve More**")
        else:
            st.markdown("⚠️ **Needs Improvement**")

        # Matched Skills
        st.markdown("### ✅ Matched Skills")
        for skill in matched:
            st.markdown(f"""
            <div class="glass">🟢 <b>{skill}</b></div>
            """, unsafe_allow_html=True)

        # Missing Skills
        st.markdown("### ❌ Missing Skills")
        for skill in missing:
            st.markdown(f"""
            <div class="glass">🔴 <b>{skill}</b></div>
            """, unsafe_allow_html=True)

        # Suggestions
        st.markdown("### 💡 Suggestions")
        for s in suggestions:
            st.markdown(f"""
            <div class="glass">💡 {s}</div>
            """, unsafe_allow_html=True)

        # ---------------- CHART ----------------
        data = {
            "Category": ["Matched", "Missing"],
            "Count": [len(matched), len(missing)]
        }

        fig = px.pie(
            names=data["Category"],
            values=data["Count"],
            color_discrete_sequence=["#22c55e", "#ef4444"]
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------- DOWNLOAD REPORT ----------------
        report = f"""
Resume Match Report

Score: {score}%
Resume Strength: {resume_score}%

Matched Skills:
{matched}

Missing Skills:
{missing}

Suggestions:
{chr(10).join(suggestions)}
"""

        st.download_button(
            "📥 Download Report",
            report,
            file_name="resume_report.txt"
        )

    # ---------------- INSIGHTS ----------------
    if menu == "📈 Insights":

        st.markdown("## 📈 Insights")

        st.write("### 🧠 Skills Summary")
        st.write("Matched:", ", ".join(matched))
        st.write("Missing:", ", ".join(missing))

        st.write("### 📊 Performance")
        st.progress(score / 100)

else:
    st.info("📌 Please upload resume and enter job description")