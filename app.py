import os
import sys
import pandas as pd
import streamlit as st
from src.pdf_generator import generate_candidate_pdf
from src.bullet_generator import generate_resume_bullets

# ============================================================
# PROJECT PATH SETUP
# ============================================================
SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from src.resume_parser import extract_resume_text
from src.screening_engine import screen_resume
from src.skill_matcher import SKILL_ALIASES, find_equivalent_skill
from src.role_suitability import recommend_roles
from src.capability_engine import analyze_job_relevant_capabilities
from src.styles import render_html, apply_custom_css
from src.career_paths import get_alternative_pathways

# ============================================================
# PAGE CONFIG & STYLES
# ============================================================
st.set_page_config(
    page_title="ResumeIQ | AI Resume Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()

def get_normalized_skill_evidence(skill, evidence_levels, fallback_levels=None):
    if not skill:
        return {}

    levels = evidence_levels if isinstance(evidence_levels, dict) else {}
    fallback = fallback_levels if isinstance(fallback_levels, dict) else {}

    raw_str = str(skill).strip()
    norm_skill = raw_str.lower()

    if raw_str in levels:
        return levels[raw_str]
    if fallback and raw_str in fallback:
        return fallback[raw_str]

    if norm_skill in levels:
        return levels[norm_skill]
    if fallback and norm_skill in fallback:
        return fallback[norm_skill]

    for k, v in levels.items():
        if str(k).strip().lower() == norm_skill:
            return v
    if fallback:
        for k, v in fallback.items():
            if str(k).strip().lower() == norm_skill:
                return v

    for canonical, aliases in SKILL_ALIASES.items():
        all_forms = [canonical.strip().lower()] + [a.strip().lower() for a in aliases]
        if norm_skill in all_forms:
            for form in all_forms:
                if form in levels:
                    return levels[form]
                if fallback and form in fallback:
                    return fallback[form]
            for k, v in levels.items():
                if str(k).strip().lower() in all_forms:
                    return v
            if fallback:
                for k, v in fallback.items():
                    if str(k).strip().lower() in all_forms:
                        return v

    return {}

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">◈ ResumeIQ</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Resume Intelligence Platform</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="sidebar-section">AI Models</div>', unsafe_allow_html=True)
    st.write("🧠 BERT")
    st.write("🔎 Sentence Transformer")
    st.write("🛠️ Skill Intelligence")
    st.write("💡 Capability Engine")
    st.markdown('<div class="sidebar-section">Analysis</div>', unsafe_allow_html=True)
    st.write("✓ Semantic compatibility")
    st.write("✓ Skill coverage")
    st.write("✓ Missing-skill detection")
    st.write("✓ Role classification")
    st.write("✓ Capability analysis")
    st.write("✓ Improvement recommendations")
    st.write("✓ Batch candidate ranking")
    st.write("✓ Alternative career pathways")
    st.divider()
    st.caption("Deep Learning • NLP • Explainable Screening")

# ============================================================
# HERO
# ============================================================
render_html(
    """
    <div class="hero">
        <div class="hero-badge">DEEP LEARNING RESUME INTELLIGENCE</div>
        <div class="hero-title">Resume<span>IQ</span></div>
        <div class="hero-description">
            Analyze candidate compatibility against job requirements, uncover skill gaps, 
            explore cross-functional career paths, and rank multiple applicants in batch.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SCREENING MODE SELECTION
# ============================================================
screening_mode = st.radio(
    "Select Screening Mode",
    options=["Single Candidate Deep-Dive", "Multi-Resume Batch Leaderboard"],
    horizontal=True
)

# ============================================================
# INPUT AREA
# ============================================================
if screening_mode == "Single Candidate Deep-Dive":
    input_col1, input_col2 = st.columns([1, 1], gap="large")

    with input_col1:
        render_html(
            """
            <div class="input-card">
                <div class="input-title">📄 Candidate Resume</div>
                <div class="input-description">Upload the candidate's resume in PDF or DOCX format.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader(
            "Upload resume",
            type=["pdf", "docx"],
            label_visibility="collapsed",
            key="single_resume_uploader"
        )

    with input_col2:
        render_html(
            """
            <div class="input-card">
                <div class="input-title">💼 Target Job</div>
                <div class="input-description">Paste the job description or required skills.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        job_description = st.text_area(
            "Job description",
            height=190,
            label_visibility="collapsed",
            placeholder=(
                "Example:\n\n"
                "We are looking for a Data Analyst with strong "
                "Python, SQL, Excel, Power BI, Tableau and "
                "statistical analysis skills..."
            ),
            key="single_job_desc"
        )

    st.write("")
    if st.button("🚀 Analyze Resume Compatibility", use_container_width=True, type="primary"):
        if not uploaded_file:
            st.error("Please upload a resume before starting the analysis.")
        elif not job_description.strip():
            st.error("Please enter a job description before starting the analysis.")
        else:
            temp_path = os.path.join(os.path.dirname(__file__), uploaded_file.name)
            try:
                with st.spinner("🔬 Running AI resume intelligence analysis — this may take 10–30 seconds..."):
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    resume_text = extract_resume_text(temp_path)
                    st.session_state["result"] = screen_resume(resume_text, job_description)
                    st.session_state["resume_name"] = uploaded_file.name
            except Exception as e:
                st.error(f"Analysis failed: {e}")
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

else:
    # MULTI-RESUME BATCH MODE
    input_col1, input_col2 = st.columns([1, 1], gap="large")

    with input_col1:
        render_html(
            """
            <div class="input-card">
                <div class="input-title">📑 Candidate Resumes (Batch)</div>
                <div class="input-description">Upload multiple resumes (PDF or DOCX) to screen and rank simultaneously.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        batch_files = st.file_uploader(
            "Upload multiple resumes",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="batch_resume_uploader"
        )

    with input_col2:
        render_html(
            """
            <div class="input-card">
                <div class="input-title">💼 Benchmark Target Job</div>
                <div class="input-description">Paste the target job description to evaluate all candidates against.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        batch_job_description = st.text_area(
            "Batch Job description",
            height=190,
            label_visibility="collapsed",
            placeholder="Paste target job requirements and qualifications here...",
            key="batch_job_desc"
        )

    st.write("")
    if st.button("📊 Run Batch Screening & Rank Candidates", use_container_width=True, type="primary"):
        if not batch_files:
            st.error("Please upload at least one resume.")
        elif not batch_job_description.strip():
            st.error("Please provide a target job description.")
        else:
            leaderboard_records = []
            progress_bar = st.progress(0)
            status_text = st.empty()

            for idx, file in enumerate(batch_files):
                status_text.text(f"Processing candidate ({idx + 1}/{len(batch_files)}): {file.name}")
                temp_path = os.path.join(os.path.dirname(__file__), file.name)
                try:
                    with open(temp_path, "wb") as f:
                        f.write(file.getbuffer())

                    text = extract_resume_text(temp_path)
                    res = screen_resume(text, batch_job_description)

                    leaderboard_records.append({
                        "Candidate File": file.name,
                        "Overall Score (%)": round(float(res.get("final_score", 0)), 1),
                        "Semantic Score (%)": round(float(res.get("semantic_score", 0)), 1),
                        "Skill Coverage (%)": round(float(res.get("skill_score", 0)), 1) if res.get("skill_score_available", True) else "N/A",
                        "Matched Skills": len(res.get("matched_skills", [])),
                        "Skill Gaps": len(res.get("missing_skills", [])),
                        "Detailed Result": res
                    })
                except Exception as ex:
                    st.warning(f"Failed parsing {file.name}: {ex}")
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

                progress_bar.progress((idx + 1) / len(batch_files))

            status_text.empty()
            if leaderboard_records:
                st.session_state["batch_results"] = leaderboard_records

# ============================================================
# BATCH LEADERBOARD DISPLAY
# ============================================================
if screening_mode == "Multi-Resume Batch Leaderboard" and "batch_results" in st.session_state:
    st.divider()
    render_html(
        """
        <div class="section-header">
            <div class="section-title">🏆 Candidate Screening Leaderboard</div>
            <div class="section-description">
                Comparative ranking and qualification analysis across all uploaded applicants.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    batch_list = st.session_state["batch_results"]
    df_board = pd.DataFrame(batch_list).sort_values(by="Overall Score (%)", ascending=False).reset_index(drop=True)

    ctrl_col1, ctrl_col2 = st.columns([2, 1])
    with ctrl_col1:
        min_cutoff = st.slider(
            "Filter Candidates by Minimum Score (%)",
            min_value=0, max_value=100, value=0, step=5,
            help="Show only candidates who meet or exceed this score threshold."
        )

    filtered_df = df_board[df_board["Overall Score (%)"] >= min_cutoff].copy().reset_index(drop=True)
    filtered_df.insert(0, "Rank", [f"#{i+1}" for i in range(len(filtered_df))])

    with ctrl_col2:
        st.write("")
        csv_data = filtered_df.drop(columns=["Detailed Result"]).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Leaderboard (CSV)",
            data=csv_data,
            file_name="resumeiq_leaderboard_results.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.dataframe(
        filtered_df.drop(columns=["Detailed Result"]),
        use_container_width=True,
        column_config={
            "Overall Score (%)": st.column_config.ProgressColumn(
                "Overall Fit", format="%.1f%%", min_value=0, max_value=100
            ),
            "Semantic Score (%)": st.column_config.NumberColumn(
                "Semantic Fit", format="%.1f%%"
            )
        }
    )

    st.write("")
    st.markdown("### 🔎 Quick Inspect Candidate")
    if not filtered_df.empty:
        selected_candidate_name = st.selectbox(
            "Select candidate to inspect report:",
            options=filtered_df["Candidate File"].tolist()
        )
        if st.button("Load Candidate Full Report", type="secondary"):
            selected_row = next(item for item in batch_list if item["Candidate File"] == selected_candidate_name)
            st.session_state["result"] = selected_row["Detailed Result"]
            st.session_state["resume_name"] = selected_candidate_name
            st.success(f"Loaded {selected_candidate_name}. Scroll below to view complete insights.")
    else:
        st.warning("No candidates meet the current minimum score threshold.")

# ============================================================
# RESULTS (DEEP DIVE REPORT)
# ============================================================
if "result" in st.session_state:
    result = st.session_state["result"]
    st.divider()

    # Report Header
    render_html(
        """
        <div class="section-header">
            <div class="section-title">Screening Report</div>
            <div class="section-description">
                Evidence-based compatibility analysis for the uploaded resume and target job.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Top Action Bar: PDF Brief Export
    top_c1, top_c2 = st.columns([3, 1])
    with top_c2:
        career_recs_pdf = get_alternative_pathways(result.get("resume_skills", []))
        candidate_label = st.session_state.get("resume_name", "Candidate")
        pdf_bytes = generate_candidate_pdf(candidate_label, result, career_recs_pdf)
        
        st.download_button(
            label="📄 Download Evaluation PDF",
            data=pdf_bytes,
            file_name=f"{candidate_label}_Screening_Brief.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    # Score Hero
    score_col, metrics_col = st.columns([1.25, 1.75], gap="large")
    with score_col:
        score = float(result["final_score"])
        render_html(
            f"""
            <div class="score-hero">
                <div class="score-label">Overall Compatibility</div>
                <div class="score-number">{score:.1f}%</div>
                <div class="score-caption">
                    Compatibility score based on semantic alignment and detected skill coverage.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.progress(min(score / 100, 1.0))

    with metrics_col:
        metric1, metric2 = st.columns(2)
        with metric1:
            render_html(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Semantic Compatibility</div>
                    <div class="metric-value">{result["semantic_score"]:.1f}%</div>
                    <div class="metric-subtitle">Resume ↔ job description meaning</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with metric2:
            if result.get("skill_score_available", True):
                skill_value = f'{result["skill_score"]:.1f}%'
                skill_subtitle = "Evidence-weighted skill score (Demonstrated=1.0, Listed Only=0.4)"
            else:
                skill_value = "Not available"
                skill_subtitle = "No recognized job skills detected"

            render_html(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Skill Coverage</div>
                    <div class="metric-value">{skill_value}</div>
                    <div class="metric-subtitle">{skill_subtitle}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")
        metric3, metric4 = st.columns(2)
        with metric3:
            render_html(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Skills Matched</div>
                    <div class="metric-value">{len(result["matched_skills"])}</div>
                    <div class="metric-subtitle">Required skills found</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with metric4:
            render_html(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Skill Gaps</div>
                    <div class="metric-value">{len(result["missing_skills"])}</div>
                    <div class="metric-subtitle">Required skills not detected</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Alternative Career Pathways
    career_recs = get_alternative_pathways(result.get("resume_skills", []))
    if career_recs:
        pathways_html = "".join([
            f"""
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 14px 18px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <strong style="color: #60a5fa; font-size: 1.05rem;">{p['role']}</strong>
                    <span style="background: rgba(59, 130, 246, 0.18); color: #93c5fd; padding: 3px 10px; border-radius: 999px; font-size: 0.85rem; font-weight: 700;">
                        {p['fit']}% Transferable Fit
                    </span>
                </div>
                <div style="font-size: 0.85rem; color: #94a3b8;">
                    <strong>Transferable Strengths:</strong> {', '.join(p['skills']).title() if p['skills'] else 'Foundational tech competencies'}
                </div>
            </div>
            """ for p in career_recs
        ])

        render_html(
            f"""
            <div style="margin-top: 24px; margin-bottom: 24px; padding: 20px; border-radius: 18px; background: rgba(15, 23, 42, 0.7); border: 1px solid #1e293b;">
                <div style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; margin-bottom: 6px; display: flex; align-items: center; gap: 8px;">
                    <span>🧭</span> Alternative Career Pathways
                </div>
                <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 16px;">
                    Based on verified competencies found in this candidate's profile, here are adjacent specializations with strong cross-functional overlap:
                </div>
                {pathways_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    # Why did you get this score?
    render_html(
        """
        <div class="section-header">
            <div class="section-title">🔍 Why did you get this score?</div>
            <div class="section-description">Transparent breakdown of how the compatibility score was calculated.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    semantic_score = float(result["semantic_score"])
    skill_score = float(result["skill_score"])
    skill_score_available = result.get("skill_score_available", bool(result.get("required_skills")))
    semantic_contribution = semantic_score * 0.60
    skill_contribution = skill_score * 0.40

    render_html(
        f"""
        <div class="explanation-card">
            <div class="explanation-title">Compatibility Score Calculation</div>
            <div class="explanation-text">
                Your final compatibility score combines two components:
                <br><br>
                <strong>Semantic Compatibility:</strong> {semantic_score:.1f}% × 60% = {semantic_contribution:.1f} points
                <br>
                <strong>Skill Coverage:</strong> {f"{skill_score:.1f}% × 40% = {skill_contribution:.1f} points" if skill_score_available else "Not available for this job description"}
                <br><br>
                <strong>
                {
                    f"Final Score = {semantic_contribution:.1f} + {skill_contribution:.1f} = {result['final_score']:.1f}%"
                    if skill_score_available
                    else f"Final Score = Semantic Compatibility = {result['final_score']:.1f}%"
                }
                </strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Smart score explanation
    matched_count = len(result.get("matched_skills", []))
    required_count = len(result.get("required_skills", []))
    missing_count = len(result.get("missing_skills", []))
    score_explanation = result.get("score_explanation", [])

    if not score_explanation:
        if required_count == 0:
            score_explanation = [
                "No recognized skills were detected in the job description.",
                "Skill coverage was excluded from the final score.",
                f"Semantic compatibility contributed {result['final_score']:.1f}% to the final score."
            ]
        else:
            score_explanation = [
                f"{matched_count} of {required_count} detected required skills were matched.",
                (
                    f"{missing_count} detected job requirements were not found in the resume."
                    if missing_count
                    else "All detected required skills were found in the resume."
                )
            ]

    explanation_items = "".join(f'<div style="margin-bottom:10px;">• {item}</div>' for item in score_explanation)
    render_html(
        f"""
        <div class="explanation-card">
            <div class="explanation-title">What influenced the result?</div>
            <div class="explanation-text">{explanation_items}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Skill Analysis Chips
    render_html(
        """
        <div class="section-header">
            <div class="section-title">🛠️ Skill Analysis</div>
            <div class="section-description">Skills detected from the job description and evidence found in the resume.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    skill_col1, skill_col2 = st.columns(2, gap="large")
    with skill_col1:
        st.markdown("### ✅ Matched Skills")
        if result["matched_skills"]:
            chips = "".join(f'<span class="chip chip-match">✓ {skill}</span>' for skill in result["matched_skills"])
            st.markdown(chips, unsafe_allow_html=True)
        else:
            st.info("No required skills were matched.")

    with skill_col2:
        st.markdown("### ❌ Missing Skills")
        if result["missing_skills"]:
            chips = ""
            for skill in result["missing_skills"]:
                equiv = find_equivalent_skill(skill, result.get("resume_skills", []))
                if equiv:
                    chips += f'<span class="chip chip-neutral" style="border: 1px dashed #f59e0b; color: #fbbf24;">△ {skill} (Sub: {equiv})</span>'
                else:
                    chips += f'<span class="chip chip-missing">! {skill}</span>'
            st.markdown(chips, unsafe_allow_html=True)
        else:
            if result.get("skill_score_available", True):
                st.success("No detected skill gaps.")
            else:
                st.info("Skill gap analysis is not available because no recognized job skills were detected.")

    # Required Skill Evidence (Collapsible)
    render_html(
        """
        <details style="margin-top:28px; margin-bottom:12px;">
        <summary style="
            cursor:pointer;
            font-size:18px;
            font-weight:700;
            color:#f8fafc;
            padding:14px 18px;
            background:rgba(15,23,42,0.85);
            border:1px solid #1e293b;
            border-radius:12px;
            list-style:none;
            display:flex;
            align-items:center;
            gap:8px;
        ">
            🔎 Required Skill Evidence
            <span style="font-size:12px;color:#64748b;margin-left:8px;">(click to expand)</span>
        </summary>
        """,
        unsafe_allow_html=True
    )

    skill_evidence_levels = result.get("skill_evidence_levels", result.get("required_skill_evidence_levels", {}))
    required_skill_evidence_levels = result.get("required_skill_evidence_levels", {})
    required_skills = result.get("required_skills", [])

    if required_skills:
        demonstrated = []
        listed = []
        supporting = []
        missing = []

        for skill in required_skills:
            evidence = get_normalized_skill_evidence(skill, skill_evidence_levels, required_skill_evidence_levels)
            raw_status = str(evidence.get("status", "missing")).strip().lower()

            if raw_status in {"demonstrated", "strong", "direct"}:
                demonstrated.append((skill, evidence))
            elif raw_status in {"listed", "listed_only", "listed only"}:
                listed.append((skill, evidence))
            elif raw_status in {"supporting", "supporting_evidence", "supporting evidence", "related"}:
                supporting.append((skill, evidence))
            else:
                missing.append((skill, evidence))

        evidence_col1, evidence_col2 = st.columns(2, gap="large")
        with evidence_col1:
            if demonstrated:
                st.markdown("### 🟢 Demonstrated")
                for skill, evidence in demonstrated:
                    sections = evidence.get("sections", [])
                    section_text = ", ".join(str(s).replace("_", " ").title() for s in sections if str(s).strip()) or "Projects / Experience"
                    render_html(
                        f"""
                        <div class="explanation-card" style="margin-bottom:10px;">
                            <div class="explanation-title">✓ {skill}</div>
                            <div class="explanation-text">
                                <strong>Status: Demonstrated</strong> • Direct evidence detected.<br><br>
                                Evidence source: {section_text}<br><br>
                                Direct evidence found in projects, internships, or work experience.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            if supporting:
                st.markdown("### 🟡 Supporting Evidence")
                for skill, evidence in supporting:
                    sections = evidence.get("sections", [])
                    section_text = ", ".join(str(s).replace("_", " ").title() for s in sections if str(s).strip()) or "Education / Certifications"
                    render_html(
                        f"""
                        <div class="explanation-card" style="margin-bottom:10px;">
                            <div class="explanation-title">△ {skill}</div>
                            <div class="explanation-text">
                                <strong>Status: Supporting Evidence</strong> • Supported by background qualifications.<br><br>
                                Evidence source: {section_text}<br><br>
                                Supported by relevant education or certifications without direct project experience.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        with evidence_col2:
            if listed:
                st.markdown("### 🔵 Listed Only")
                for skill, evidence in listed:
                    sections = evidence.get("sections", ["skills"])
                    section_text = ", ".join(str(s).replace("_", " ").title() for s in sections if str(s).strip()) or "Skills"
                    render_html(
                        f"""
                        <div class="explanation-card" style="margin-bottom:10px;">
                            <div class="explanation-title">• {skill}</div>
                            <div class="explanation-text">
                                <strong>Status: Listed Only</strong> • Mentioned in skills section.<br><br>
                                Evidence source: {section_text}<br><br>
                                Mentioned in the skills section without direct project or experience evidence.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            if missing:
                st.markdown("### 🔴 Missing")
                for skill, evidence in missing:
                    render_html(
                        f"""
                        <div class="improvement-card" style="margin-bottom:10px;">
                            <div class="improvement-title">! {skill}</div>
                            <div class="improvement-text">
                                <strong>Status: Missing</strong> • No meaningful evidence detected.<br><br>
                                Evidence source: None detected<br><br>
                                No meaningful evidence for this required skill was detected in the resume.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    else:
        st.info("No required skill evidence is available.")

    render_html("<p></details>", unsafe_allow_html=True)

    # Job Responsibility Analysis (Collapsible)
    render_html(
        """
        <details style="margin-top:28px; margin-bottom:12px;">
        <summary style="
            cursor:pointer;
            font-size:18px;
            font-weight:700;
            color:#f8fafc;
            padding:14px 18px;
            background:rgba(15,23,42,0.85);
            border:1px solid #1e293b;
            border-radius:12px;
            list-style:none;
            display:flex;
            align-items:center;
            gap:8px;
        ">
            🎯 Job Responsibility Analysis
            <span style="font-size:12px;color:#64748b;margin-left:8px;">(click to expand)</span>
        </summary>
        """,
        unsafe_allow_html=True
    )

    responsibility_analysis = result.get("responsibility_analysis", {})
    responsibility_items = responsibility_analysis.get("responsibilities", [])

    if responsibility_items:
        strong_items = [i for i in responsibility_items if i.get("status") == "strong"]
        related_items = [i for i in responsibility_items if i.get("status") == "related"]
        missing_items = [i for i in responsibility_items if i.get("status") == "missing"]

        if strong_items:
            st.markdown("### 🟢 Strong Evidence")
            for item in strong_items:
                evidence = item.get("evidence", [])
                evidence_text = ", ".join(str(e.get("evidence", "")) for e in evidence if e.get("evidence")) or "Explicitly supported by resume content."
                render_html(
                    f"""
                    <div class="explanation-card" style="margin-bottom:10px;">
                        <div class="explanation-title">✓ {item.get('responsibility', 'Responsibility')}</div>
                        <div class="explanation-text"><strong>Resume evidence:</strong> {evidence_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if related_items:
            st.markdown("### 🟡 Related Evidence")
            for item in related_items:
                related_names = [ev.get("skill", "") for ev in item.get("related_evidence", []) if ev.get("skill")]
                related_text = ", ".join(related_names) or "Related resume evidence detected."
                render_html(
                    f"""
                    <div class="explanation-card" style="margin-bottom:10px;">
                        <div class="explanation-title">△ {item.get('responsibility', 'Responsibility')}</div>
                        <div class="explanation-text">
                            <strong>Related evidence:</strong> {related_text}<br><br>
                            Related evidence supports the responsibility but does not prove direct performance.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if missing_items:
            st.markdown("### 🔴 Not Demonstrated")
            for item in missing_items:
                render_html(
                    f"""
                    <div class="improvement-card">
                        <div class="improvement-title">! {item.get('responsibility', 'Responsibility')}</div>
                        <div class="improvement-text">{item.get('reason', 'No meaningful evidence was detected.')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        summary = responsibility_analysis.get("summary", {})
        st.caption(
            f"Responsibility evidence: {summary.get('strong', len(strong_items))} strong • "
            f"{summary.get('related', len(related_items))} related • "
            f"{summary.get('missing', len(missing_items))} not demonstrated"
        )
    else:
        render_html(
            """
            <div class="explanation-card" style="border-left:3px solid #f59e0b;">
                <div class="explanation-title" style="color:#f59e0b;">📋 No Responsibilities Detected</div>
                <div class="explanation-text">
                    Add responsibilities to the JD for deeper analysis.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    render_html("<p></details>", unsafe_allow_html=True)

    # Improvement Plan
    render_html(
        """
        <div class="section-header">
            <div class="section-title">🚀 How can you improve?</div>
            <div class="section-description">Actionable recommendations based on the requirements detected in the job description.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if result["missing_skills"]:
        for index, skill in enumerate(result["missing_skills"], start=1):
            render_html(
                f"""
                <div class="improvement-card">
                    <div class="improvement-title">{index}. {skill}</div>
                    <div class="improvement-text">
                        This requirement appears in the job description but was not detected in
                        the resume. If you genuinely have this experience, consider clearly documenting
                        the relevant project, coursework, certification, or work experience.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        if result.get("skill_score_available", True):
            st.success("No detected skill gaps. The resume covers all recognized requirements from the job description.")
            suggestions_list = result.get("suggestions", [])
            upgrade_suggestions = [s for s in suggestions_list if "listed only" in s.lower() or "upgrade" in s.lower()]
            for sug in upgrade_suggestions:
                render_html(
                    f'''<div class="improvement-card" style="border-left:3px solid #f59e0b;">
                        <div class="improvement-title" style="color:#f59e0b;">⬆ Strengthen Evidence</div>
                        <div class="improvement-text">{sug}</div>
                    </div>''',
                    unsafe_allow_html=True
                )
        else:
            st.info("No recognized job skills were detected, so skill-specific improvement recommendations cannot be generated.")
        # ========================================================
    # RESUME BULLET-POINT OPTIMIZER
    # ========================================================
    if result.get("missing_skills"):
        with st.expander("✨ Resume Bullet-Point Optimizer (ATS Formatted)"):
            st.markdown(
                "<div style='font-size:13px; color:#94a3b8; margin-bottom:12px;'>"
                "Select any identified skill gap to generate high-impact, action-driven bullet points "
                "ready to paste into your resume."
                "</div>",
                unsafe_allow_html=True
            )
            
            selected_gap = st.selectbox(
                "Choose a skill to generate bullet points for:",
                options=result["missing_skills"],
                key="bullet_skill_selector"
            )
            
            if selected_gap:
                bullets = generate_resume_bullets(selected_gap)
                for b in bullets:
                    st.code(b, language="text")
                    st.caption("Click the copy icon on the top right to paste directly into your resume.")    

    # Candidate Strengths
    render_html(
        """
        <div class="section-header">
            <div class="section-title">💪 Candidate Strengths</div>
            <div class="section-description">Evidence detected from skills that overlap with the target job requirements.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if result["matched_skills"]:
        chips = "".join(f'<span class="chip chip-match">✓ {skill}</span>' for skill in result["matched_skills"])
        st.markdown(chips, unsafe_allow_html=True)
    else:
        if result.get("skill_score_available", True):
            st.info("No matching strengths were detected.")
        else:
            st.info("Skill-based strengths could not be compared because no recognized job skills were detected.")

    # BERT Resume Classification (Collapsible)
    render_html(
        """
        <details style="margin-top:28px; margin-bottom:12px;">
        <summary style="
            cursor:pointer;
            font-size:18px;
            font-weight:700;
            color:#f8fafc;
            padding:14px 18px;
            background:rgba(15,23,42,0.85);
            border:1px solid #1e293b;
            border-radius:12px;
            list-style:none;
            display:flex;
            align-items:center;
            gap:8px;
        ">
            🧠 BERT Resume Classification
            <span style="font-size:12px;color:#64748b;margin-left:8px;">(click to expand)</span>
        </summary>
        """,
        unsafe_allow_html=True
    )

    bert_categories = result.get("bert_categories", [])
    if bert_categories:
        bert_cols = st.columns(len(bert_categories))
        for index, prediction in enumerate(bert_categories):
            with bert_cols[index]:
                render_html(
                    f"""
                    <div class="bert-card">
                        <div class="bert-rank">RANK {index + 1}</div>
                        <div class="bert-category">{prediction["category"].title()}</div>
                        <div class="bert-confidence">{prediction["confidence"]:.2f}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.caption(
            "BERT confidence represents classification probability across resume categories. "
            "⚠️ Low confidence (< 50%) indicates ambiguous resume text; it does not degrade overall compatibility score."
        )

    render_html("<p></details>", unsafe_allow_html=True)

    # Job-Relevant Capabilities
    render_html(
        """
        <div class="section-header">
            <div class="section-title">🎯 Job-Relevant Capability Analysis</div>
            <div class="section-description">Higher-level capabilities relevant to the target job, based on recognized job-skill evidence.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    job_capabilities = analyze_job_relevant_capabilities(
        result.get("resume_skills", []),
        result.get("required_skills", [])
    )

    if job_capabilities:
        capability_columns = st.columns(2)
        for index, capability in enumerate(job_capabilities):
            with capability_columns[index % 2]:
                name = capability.get("capability", "Unknown")
                description = capability.get("description", "")
                coverage = capability.get("coverage", 0.0)
                alignment = capability.get("alignment", "Low Alignment")
                requirement_type = capability.get("requirement_type", "Supporting")
                matched = capability.get("matched_skills", [])
                missing = capability.get("missing_skills", [])

                status = "✓ Strong Alignment" if alignment == "Strong Alignment" else ("△ Partial Alignment" if alignment == "Partial Alignment" else "! Low Alignment")
                type_icon = "🎯" if requirement_type == "Required" else "↳"

                render_html(
                    f"""
                    <div class="capability-card">
                        <div class="capability-name">{name.title()}</div>
                        <div class="capability-status">
                            {type_icon} {requirement_type} • {status} • {coverage:.1f}% evidence coverage
                        </div>
                        <div class="capability-description">{description}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if matched:
                    st.caption("Matched job evidence")
                    st.markdown("".join(f'<span class="chip chip-match">✓ {s}</span>' for s in matched), unsafe_allow_html=True)

                if missing:
                    st.caption("Capability gaps")
                    st.markdown("".join(f'<span class="chip chip-missing">! {s}</span>' for s in missing), unsafe_allow_html=True)
    else:
        st.info("No higher-level capabilities were directly linked to the recognized required skills for this job.")

    # Role Suitability & Recommendations
    render_html(
        """
        <div class="section-header">
            <div class="section-title">🎯 Role Suitability & Recommended Roles</div>
            <div class="section-description">Roles ranked using skills detected from the candidate's resume.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    role_recommendations = recommend_roles(
        result.get("resume_skills", []),
        skill_evidence_levels=result.get("skill_evidence_levels", {})
    )

    if role_recommendations:
        top_roles = role_recommendations[:3]
        role_columns = st.columns(len(top_roles))

        for index, role_result in enumerate(top_roles):
            with role_columns[index]:
                coverage = role_result["coverage"]
                status = role_result["status"]
                status_icon = "🟢" if status == "Strong Fit" else ("🟡" if status == "Moderate Fit" else "🔴")
                matched_cnt = len(role_result["matched_skills"])
                missing_cnt = len(role_result["missing_skills"])

                render_html(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">RANK {index + 1}</div>
                        <div class="metric-value" style="font-size:22px;">{role_result["role"]}</div>
                        <div style="color:#93c5fd;font-size:24px;font-weight:800;margin-top:8px;">{coverage:.1f}%</div>
                        <div class="metric-subtitle">{status_icon} {status} • {matched_cnt} matched • {missing_cnt} gaps</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.write("")
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        if st.button("🔄 Analyze Another Resume", use_container_width=True, key="analyze_another_btn"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    render_html(
        """
        <div class="responsible-ai" style="margin-top: 25px;">
            <strong>Responsible AI Notice</strong><br><br>
            This system provides decision-support information based on the uploaded resume and job description.
            Compatibility scores, BERT classifications, and detected capabilities should not be treated as hiring
            probabilities or used as the sole basis for employment decisions.
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# FOOTER
# ============================================================
render_html(
    """
    <div class="footer">
        ResumeIQ • Deep Learning • NLP • Explainable Resume Intelligence
    </div>
    """,
    unsafe_allow_html=True
)