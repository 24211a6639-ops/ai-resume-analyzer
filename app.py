import html

import plotly.graph_objects as go
import streamlit as st

from matcher import analyze_resume
from parser import extract_text_from_upload


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles():
    st.markdown(
        """
        <style>
            :root {
                --bg: #f6f8fb;
                --panel: #ffffff;
                --ink: #162033;
                --muted: #61708a;
                --line: #dbe4ef;
                --blue: #2563eb;
                --teal: #0891b2;
                --green: #16a34a;
                --amber: #d97706;
                --rose: #e11d48;
                --violet: #7c3aed;
            }

            .stApp {
                background:
                    linear-gradient(180deg, rgba(37, 99, 235, 0.06), rgba(246, 248, 251, 0) 260px),
                    var(--bg);
                color: var(--ink);
            }

            section[data-testid="stSidebar"] {
                background: #0f172a;
                border-right: 1px solid rgba(255, 255, 255, 0.08);
            }

            section[data-testid="stSidebar"] * {
                color: #e5edf8;
            }

            .block-container {
                padding-top: 1.6rem;
                padding-bottom: 2.2rem;
                max-width: 1240px;
            }

            .app-header {
                border: 1px solid var(--line);
                background: var(--panel);
                border-radius: 8px;
                padding: 22px 24px;
                box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
                margin-bottom: 18px;
            }

            .eyebrow {
                color: var(--teal);
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0;
                text-transform: uppercase;
                margin-bottom: 7px;
            }

            .app-title {
                color: var(--ink);
                font-size: clamp(2rem, 3vw, 3.2rem);
                font-weight: 850;
                line-height: 1.05;
                margin: 0;
                letter-spacing: 0;
            }

            .app-subtitle {
                max-width: 790px;
                color: var(--muted);
                font-size: 1.02rem;
                line-height: 1.55;
                margin-top: 10px;
                margin-bottom: 0;
            }

            .panel {
                border: 1px solid var(--line);
                background: var(--panel);
                border-radius: 8px;
                padding: 18px;
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
                min-height: 100%;
            }

            .section-label {
                color: var(--ink);
                font-size: 1rem;
                font-weight: 800;
                margin-bottom: 10px;
            }

            .metric-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 12px;
                margin-bottom: 14px;
            }

            .metric-card {
                border: 1px solid var(--line);
                background: var(--panel);
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
            }

            .metric-label {
                color: var(--muted);
                font-size: 0.78rem;
                font-weight: 700;
                margin-bottom: 6px;
            }

            .metric-value {
                color: var(--ink);
                font-size: 1.8rem;
                line-height: 1;
                font-weight: 850;
            }

            .metric-note {
                color: var(--muted);
                font-size: 0.78rem;
                margin-top: 7px;
            }

            .pill-row {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin: 8px 0 2px;
            }

            .pill {
                display: inline-flex;
                align-items: center;
                border-radius: 999px;
                padding: 7px 10px;
                font-size: 0.82rem;
                font-weight: 700;
                border: 1px solid transparent;
                word-break: break-word;
            }

            .pill.good {
                background: #dcfce7;
                color: #14532d;
                border-color: #86efac;
            }

            .pill.warn {
                background: #fff7ed;
                color: #9a3412;
                border-color: #fed7aa;
            }

            .insight {
                border-left: 4px solid var(--blue);
                background: #eff6ff;
                border-radius: 8px;
                padding: 12px 14px;
                color: #1e3a8a;
                margin-bottom: 10px;
                font-size: 0.92rem;
                line-height: 1.45;
            }

            .action-item {
                border: 1px solid var(--line);
                background: #ffffff;
                border-radius: 8px;
                padding: 12px 14px;
                margin-bottom: 10px;
            }

            .action-title {
                color: var(--ink);
                font-weight: 800;
                margin-bottom: 4px;
            }

            .action-body {
                color: var(--muted);
                font-size: 0.9rem;
                line-height: 1.45;
            }

            .empty-state {
                border: 1px dashed #b9c7dc;
                background: #ffffff;
                border-radius: 8px;
                padding: 26px;
                color: var(--muted);
                text-align: center;
            }

            div[data-testid="stFileUploader"] {
                border: 1px solid var(--line);
                border-radius: 8px;
                padding: 8px;
                background: #fbfdff;
            }

            .stTextArea textarea {
                border-radius: 8px;
            }

            .stButton > button {
                border-radius: 8px;
                font-weight: 800;
                border: 1px solid #1d4ed8;
                background: #2563eb;
                color: white;
            }

            @media (max-width: 900px) {
                .metric-grid {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }
            }

            @media (max-width: 640px) {
                .metric-grid {
                    grid-template-columns: 1fr;
                }

                .app-header {
                    padding: 18px;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def score_band(score):
    if score >= 80:
        return "Strong match", "#16a34a"
    if score >= 60:
        return "Good potential", "#0891b2"
    if score >= 40:
        return "Needs tailoring", "#d97706"
    return "Needs work", "#e11d48"


def render_header():
    st.markdown(
        """
        <div class="app-header">
            <div class="eyebrow">AI Resume Dashboard</div>
            <h1 class="app-title">AI Resume Analyzer</h1>
            <p class="app-subtitle">
                Upload a resume, paste a job description, and get a clean match dashboard with skill gaps,
                ATS readiness signals, and practical next steps.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_cards(analysis):
    match_label, match_color = score_band(analysis["match_score"])
    cards = [
        ("Match Score", f"{analysis['match_score']}%", match_label, match_color),
        ("Skill Coverage", f"{analysis['skill_score']}%", "Skills matched", "#7c3aed"),
        ("Semantic Fit", f"{analysis['semantic_score']}%", "Content similarity", "#0891b2"),
        ("Resume Strength", f"{analysis['resume_strength']}%", f"{analysis['word_count']} words", "#d97706"),
    ]

    html_cards = ['<div class="metric-grid">']
    for label, value, note, color in cards:
        html_cards.append(
            f"""
            <div class="metric-card">
                <div class="metric-label">{html.escape(label)}</div>
                <div class="metric-value" style="color:{color};">{html.escape(value)}</div>
                <div class="metric-note">{html.escape(note)}</div>
            </div>
            """
        )
    html_cards.append("</div>")
    st.markdown("".join(html_cards), unsafe_allow_html=True)


def gauge_chart(score):
    label, color = score_band(score)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "%", "font": {"size": 38, "color": "#162033"}},
            title={"text": label, "font": {"size": 16, "color": "#61708a"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 0, "tickcolor": "#dbe4ef"},
                "bar": {"color": color, "thickness": 0.22},
                "bgcolor": "#ffffff",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "#ffe4e6"},
                    {"range": [40, 60], "color": "#ffedd5"},
                    {"range": [60, 80], "color": "#e0f2fe"},
                    {"range": [80, 100], "color": "#dcfce7"},
                ],
            },
        )
    )
    fig.update_layout(
        height=275,
        margin={"l": 18, "r": 18, "t": 30, "b": 8},
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Arial"},
    )
    return fig


def breakdown_chart(analysis):
    labels = ["Skill Coverage", "Semantic Fit", "Resume Strength"]
    values = [
        analysis["skill_score"],
        analysis["semantic_score"],
        analysis["resume_strength"],
    ]
    colors = ["#7c3aed", "#0891b2", "#d97706"]
    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker={"color": colors, "line": {"width": 0}},
            text=[f"{v}%" for v in values],
            textposition="auto",
        )
    )
    fig.update_xaxes(range=[0, 100], showgrid=True, gridcolor="#e5edf8")
    fig.update_yaxes(showgrid=False)
    fig.update_layout(
        height=275,
        margin={"l": 8, "r": 18, "t": 18, "b": 16},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Arial", "color": "#162033"},
    )
    return fig


def render_pills(title, items, kind):
    st.markdown(f'<div class="section-label">{html.escape(title)}</div>', unsafe_allow_html=True)
    if not items:
        st.markdown('<div class="empty-state">No items found yet.</div>', unsafe_allow_html=True)
        return

    pill_markup = ['<div class="pill-row">']
    for item in items:
        pill_markup.append(f'<span class="pill {kind}">{html.escape(item.title())}</span>')
    pill_markup.append("</div>")
    st.markdown("".join(pill_markup), unsafe_allow_html=True)


def render_action_plan(suggestions):
    if not suggestions:
        st.markdown(
            """
            <div class="insight">
                Strong alignment detected. Keep the resume tailored by quantifying impact and keeping project links visible.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for index, suggestion in enumerate(suggestions, start=1):
        st.markdown(
            f"""
            <div class="action-item">
                <div class="action-title">Step {index}: {html.escape(suggestion['title'])}</div>
                <div class="action-body">{html.escape(suggestion['body'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_ats_checks(analysis):
    checks = [
        ("Contact details", True, "Name, email, phone, GitHub, and LinkedIn should be visible at the top."),
        ("Keyword alignment", bool(analysis["matched_skills"]), "Use exact terms from the job description where truthful."),
        ("Skill gaps", len(analysis["missing_skills"]) <= 3, "Add missing high-value skills through projects or coursework."),
        ("Resume length", analysis["word_count"] >= 250, "A short resume may miss important keywords and proof points."),
        ("Project evidence", any(term in analysis["resume_text"] for term in ["github", "project", "deployed", "built"]), "Add project links and measurable outcomes."),
    ]

    for label, passed, detail in checks:
        icon = "PASS" if passed else "FIX"
        kind = "good" if passed else "warn"
        st.markdown(
            f"""
            <div class="action-item">
                <div class="action-title"><span class="pill {kind}">{icon}</span> {html.escape(label)}</div>
                <div class="action-body">{html.escape(detail)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def load_inputs():
    with st.sidebar:
        st.markdown("### Analyzer Setup")
        role = st.selectbox(
            "Target role",
            [
                "Python Developer",
                "AI/ML Engineer",
                "Data Analyst",
                "Web Developer",
                "Backend Developer",
            ],
        )
        st.markdown("---")
        min_score = st.slider("Target match score", 50, 95, 75, 5)
        show_resume_text = st.checkbox("Show extracted resume text", value=False)
        st.markdown("---")
        st.caption("Tip: paste the complete job description for the best analysis.")

    left, right = st.columns([0.95, 1.05], gap="large")

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Resume Input</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload resume",
            type=["pdf", "docx"],
            accept_multiple_files=False,
        )
        pasted_resume = st.text_area(
            "Or paste resume text",
            height=170,
            placeholder="Paste resume text here if you do not want to upload a file.",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Job Description</div>', unsafe_allow_html=True)
        job_description = st.text_area(
            "Paste job description",
            height=300,
            placeholder="Paste the job description, responsibilities, and required skills here.",
        )
        analyze_clicked = st.button("Analyze Resume", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    resume_text = ""
    parse_error = ""
    if uploaded_file:
        resume_text, parse_error = extract_text_from_upload(uploaded_file)
    elif pasted_resume.strip():
        resume_text = pasted_resume.lower()

    return {
        "role": role,
        "min_score": min_score,
        "show_resume_text": show_resume_text,
        "resume_text": resume_text,
        "job_description": job_description.lower(),
        "parse_error": parse_error,
        "analyze_clicked": analyze_clicked,
    }


def render_results(analysis, min_score, show_resume_text):
    render_metric_cards(analysis)

    score_gap = max(min_score - analysis["match_score"], 0)
    if score_gap:
        st.markdown(
            f"""
            <div class="insight">
                The resume is {score_gap:.1f} points below your target score. Start with the missing skills and
                strengthen project bullets with job-description keywords.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="insight">
                This resume meets your selected target score. Review the ATS checks and keep the strongest project
                evidence near the top.
            </div>
            """,
            unsafe_allow_html=True,
        )

    overview, skills, action_plan, ats = st.tabs(
        ["Dashboard", "Skill Gap", "Action Plan", "ATS Checks"]
    )

    with overview:
        chart_left, chart_right = st.columns(2, gap="large")
        with chart_left:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.plotly_chart(gauge_chart(analysis["match_score"]), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with chart_right:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.plotly_chart(breakdown_chart(analysis), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with skills:
        matched_col, missing_col = st.columns(2, gap="large")
        with matched_col:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            render_pills("Matched Skills", analysis["matched_skills"], "good")
            st.markdown("</div>", unsafe_allow_html=True)
        with missing_col:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            render_pills("Missing Skills", analysis["missing_skills"], "warn")
            st.markdown("</div>", unsafe_allow_html=True)

    with action_plan:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        render_action_plan(analysis["suggestions"])
        st.markdown("</div>", unsafe_allow_html=True)

    with ats:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        render_ats_checks(analysis)
        st.markdown("</div>", unsafe_allow_html=True)

    if show_resume_text:
        with st.expander("Extracted resume text"):
            st.text_area("Resume text", analysis["resume_text"], height=260)


def main():
    inject_styles()
    render_header()
    inputs = load_inputs()

    if inputs["parse_error"]:
        st.error(inputs["parse_error"])

    can_analyze = bool(inputs["resume_text"].strip()) and bool(inputs["job_description"].strip())

    if inputs["analyze_clicked"] and not can_analyze:
        st.warning("Upload or paste a resume and paste a job description before analyzing.")

    if can_analyze:
        analysis = analyze_resume(
            inputs["resume_text"],
            inputs["job_description"],
            inputs["role"],
        )
        render_results(analysis, inputs["min_score"], inputs["show_resume_text"])
    else:
        st.markdown(
            """
            <div class="empty-state">
                Your analysis dashboard will appear here after you add resume text and a job description.
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
