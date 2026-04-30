import streamlit as st
import plotly.express as px
from myparser import extract_text
from matcher import calculate_match, get_suggestions, semantic_similarity

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------- STYLE ----------
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
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
menu = st.sidebar.radio("📌 Navigation", ["Upload", "Results", "Insights"])

# ---------- STATE ----------
if "data" not in st.session_state:
    st.session_state.data = None

# ---------- UPLOAD ----------
if menu == "Upload":

    st.title("📄 AI Resume Analyzer")

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    job_desc = st.text_area("Enter Job Description")

    if st.button("Analyze"):

        if not uploaded_file or not job_desc:
            st.warning("Please upload file and enter job description")
            st.stop()

        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        resume_text = extract_text(uploaded_file.name)

        if not resume_text.strip():
            st.error("Text extraction failed")
            st.stop()

        score, matched, missing, resume_score = calculate_match(resume_text, job_desc)
        suggestions = get_suggestions(missing)
        sim = semantic_similarity(resume_text, job_desc)

        st.session_state.data = {
            "score": score,
            "matched": matched,
            "missing": missing,
            "resume_score": resume_score,
            "suggestions": suggestions,
            "sim": sim
        }

        st.success("Analysis complete → Go to Results")

# ---------- RESULTS ----------
elif menu == "Results":

    data = st.session_state.data

    if not data:
        st.warning("Run analysis first")
        st.stop()

    st.title("📊 Results")

    st.progress(data["score"] / 100)

    col1, col2, col3 = st.columns(3)

    col1.metric("Match Score", f"{data['score']}%")
    col2.metric("Resume Strength", f"{data['resume_score']}%")
    col3.metric("Semantic Match", f"{data['sim']}%")

    st.markdown("### ✅ Matched Skills")
    for s in data["matched"]:
        st.success(s)

    st.markdown("### ❌ Missing Skills")
    for s in data["missing"]:
        st.error(s)

# ---------- INSIGHTS ----------
elif menu == "Insights":

    data = st.session_state.data

    if not data:
        st.warning("Run analysis first")
        st.stop()

    st.title("📈 Insights")

    # Pie chart
    fig = px.pie(
        names=["Matched", "Missing"],
        values=[len(data["matched"]), len(data["missing"])],
        color_discrete_sequence=["green", "red"]
    )

    st.plotly_chart(fig)

    st.markdown("### 💡 Suggestions")
    for s in data["suggestions"]:
        st.info(s)

    # Download report
    report = f"""
Score: {data['score']}%
Resume Strength: {data['resume_score']}

Matched: {data['matched']}
Missing: {data['missing']}

Suggestions:
{chr(10).join(data['suggestions'])}
"""

    st.download_button("Download Report", report)
