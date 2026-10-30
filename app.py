import os
import sys
import re
import pandas as pd
import streamlit as st
from src.pdf_generator import generate_candidate_pdf
from src.bullet_generator import generate_resume_bullets
from src.interview_generator import generate_interview_questions

SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from src.resume_parser import extract_resume_text
from src.screening_engine import screen_resume
from src.skill_matcher import SKILL_ALIASES, find_equivalent_skill, format_skill_display
from src.role_suitability import recommend_roles
from src.capability_engine import analyze_job_relevant_capabilities
from src.styles import render_html, apply_custom_css
from src.career_paths import get_alternative_pathways

st.set_page_config(
    page_title="ResumeIQ | AI Resume Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()

# Centrality ordering for skills display
JD_CENTRALITY = [
    "rest api", "react", "sql", "power bi", "javascript", "html", "css",
    "dashboard", "data analysis", "python", "excel", "responsive web design",
    "ui/ux", "git", "figma", "adobe xd", "database", "exploratory data analysis",
    "pandas", "numpy", "kpi", "statistical analysis"
]

def clean_snippet_text(raw_text):
    if not raw_text:
        return ""
    text = str(raw_text).replace("|", " ").replace("\n", " ")
    text = re.sub(r"^(Present|Current|Date:?)\s*", "", text, flags=re.I)
    text = re.sub(r"[\u2022\u25cf\u25cb\u25e6\u2023\u25b8●•*#]+\s*", " ", text)
    text = re.sub(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", "", text)
    text = re.sub(r"(?<![a-zA-Z0-9])[-–—]+(?![a-zA-Z0-9])", " ", text)
    text = re.sub(r"[\s–—\-:]+$", "", text).strip()
    text = re.sub(r"\s+", " ", text).strip().lstrip("•-* ")
    return text[:260] + "..." if len(text) > 260 else text

def get_normalized_skill_evidence(skill, evidence_levels, fallback_levels=None):
    if not skill:
        return {}

    levels = evidence_levels if isinstance(evidence_levels, dict) else {}
    fallback = fallback_levels if isinstance(fallback_levels, dict) else {}

    raw_str = str(skill).strip()
    norm_skill = raw_str.lower()

    if raw_str in levels:
        return dict(levels[raw_str])
    if fallback and raw_str in fallback:
        return dict(fallback[raw_str])

    if norm_skill in levels:
        return dict(levels[norm_skill])
    if fallback and norm_skill in fallback:
        return dict(fallback[norm_skill])

    for k, v in levels.items():
        if str(k).strip().lower() == norm_skill:
            return dict(v)
    if fallback:
        for k, v in fallback.items():
            if str(k).strip().lower() == norm_skill:
                return dict(v)

    return {}

with st.sidebar:
    st.markdown('<div class="sidebar-brand">◈ ResumeIQ</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle" style="color:#94a3b8;">Resume Intelligence Platform</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="sidebar-section">AI Models</div>', unsafe_allow_html=True)
    st.write("🧠 BERT Classifier (Supporting)")
    st.write("🔎 Sentence-Transformers (MiniLM Calibrated)")
    st.write("🛠️ Evidence-Weighted Skill Engine")
    st.write("💡 Semantic Capability Engine")
    st.markdown('<div class="sidebar-section">Analysis Suite</div>', unsafe_allow_html=True)
    st.write("✓ Calibrated semantic matching")
    st.write("✓ 4-tier evidence verification")
    st.write("✓ Substitute skill crediting")
    st.write("✓ Cross-functional pathways")
    st.write("✓ Batch candidate ranking")
    st.divider()
    st.caption("Deep Learning • NLP • Explainable Screening")

render_html(
    """
    <div class="hero">
        <div class="hero-badge">EXPLAINABLE RESUME INTELLIGENCE</div>
        <div class="hero-title">Resume<span>IQ</span></div>
        <div class="hero-description" style="color: #cbd5e1;">
            Dual-engine ATS: Dense semantic similarity combined with evidence-weighted skill verification, 
            gap remediation, and batch leaderboard ranking.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

screening_mode = st.radio(
    "Select Screening Mode",
    options=["Single Candidate Deep-Dive", "Multi-Resume Batch Leaderboard"],
    horizontal=True
)

if screening_mode == "Single Candidate Deep-Dive":
    input_col1, input_col2 = st.columns([1, 1], gap="large")

    with input_col1:
        render_html(
            """
            <div class="input-card">
                <div class="input-title">📄 Candidate Resume</div>
                <div class="input-description" style="color:#94a3b8;">Upload candidate resume in PDF or DOCX format.</div>
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
                <div class="input-description" style="color:#94a3b8;">Paste job description or required competencies.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        job_description = st.text_area(
            "Job description",
            height=190,
            label_visibility="collapsed",
            placeholder="Paste target job requirements and qualifications here...",
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
                with st.spinner("🔬 Running AI resume intelligence analysis..."):
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    resume_text = extract_resume_text(temp_path)
                    st.session_state["result"] = screen_resume(resume_text, job_description)
                    st.session_state["resume_name"] = uploaded_file.name
                    st.session_state["active_jd_preview"] = job_description[:120].strip() + "..."
            except Exception as e:
                st.error(f"Analysis failed: {e}")
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

else:
    input_col1, input_col2 = st.columns([1, 1], gap="large")

    with input_col1:
        render_html(
            """
            <div class="input-card">
                <div class="input-title">📑 Candidate Resumes (Batch)</div>
                <div class="input-description" style="color:#94a3b8;">Upload multiple resumes to screen and rank simultaneously.</div>
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
                <div class="input-description" style="color:#94a3b8;">Paste target job description to evaluate all candidates against.</div>
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

            st.session_state["batch_jd_text"] = batch_job_description

            for idx, file in enumerate(batch_files):
                status_text.text(f"Screening candidate ({idx + 1}/{len(batch_files)}): {file.name}")
                temp_path = os.path.join(os.path.dirname(__file__), file.name)
                try:
                    with open(temp_path, "wb") as f:
                        f.write(file.getbuffer())

                    text = extract_resume_text(temp_path)
                    res = screen_resume(text, batch_job_description)

                    clean_name = re.sub(r"\s*\(\d+\)", "", file.name)

                    leaderboard_records.append({
                        "Candidate File": clean_name,
                        "Overall Score (%)": round(float(res.get("final_score", 0)), 1),
                        "Semantic Score (%)": round(float(res.get("semantic_score", 0)), 1),
                        "Skill Coverage (%)": round(float(res.get("skill_score", 0)), 1) if res.get("skill_score_available", True) else 0.0,
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

if screening_mode == "Multi-Resume Batch Leaderboard" and "batch_results" in st.session_state:
    st.divider()

    target_title = st.session_state.get("batch_jd_text", "").splitlines()[0][:80] if st.session_state.get("batch_jd_text") else "Custom Benchmark Job"
    
    render_html(
        f"""
        <div class="section-header" style="margin-bottom: 12px;">
            <div class="section-title">🏆 Candidate Screening Leaderboard</div>
            <div class="section-description" style="color: #94a3b8;">
                Evaluated against: <strong style="color: #60a5fa;">{target_title}</strong>
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

    filtered_df = df_board[df_board["Overall Score (%)"] >= float(min_cutoff)].copy().reset_index(drop=True)
    
    if not filtered_df.empty:
        filtered_df.insert(0, "Rank", [f"#{i+1}" for i in range(len(filtered_df))])

    with ctrl_col2:
        st.write("")
        if not filtered_df.empty:
            csv_data = filtered_df.drop(columns=["Detailed Result"]).to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Export Leaderboard (CSV)",
                data=csv_data,
                file_name="resumeiq_leaderboard_results.csv",
                mime="text/csv",
                use_container_width=True
            )

    if not filtered_df.empty:
        display_df = filtered_df.drop(columns=["Detailed Result"]).copy()
        display_df["Overall Fit"] = display_df["Overall Score (%)"]
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": st.column_config.TextColumn("Rank", width="small"),
                "Candidate File": st.column_config.TextColumn("Candidate", width="medium"),
                "Overall Fit": st.column_config.ProgressColumn(
                    "Overall Fit", format="%.1f%%", min_value=0, max_value=100
                ),
                "Overall Score (%)": st.column_config.NumberColumn(
                    "Overall (%)", format="%.1f%%"
                ),
                "Semantic Score (%)": st.column_config.NumberColumn(
                    "Semantic (%)", format="%.1f%%"
                ),
                "Skill Coverage (%)": st.column_config.NumberColumn(
                    "Skill Coverage (%)", format="%.1f%%"
                )
            }
        )

        st.write("")
        st.markdown("### 🔎 Quick Inspect Candidate")
        selected_candidate_name = st.selectbox(
            "Select candidate to inspect report:",
            options=filtered_df["Candidate File"].tolist()
        )
        if st.button("Load Candidate Full Report", type="secondary"):
            selected_row = next(item for item in batch_list if item["Candidate File"] == selected_candidate_name)
            st.session_state["result"] = selected_row["Detailed Result"]
            st.session_state["resume_name"] = selected_candidate_name
            st.success(f"Loaded {selected_candidate_name}. Explore report below.")
    else:
        st.warning(f"No candidates meet the minimum score threshold of {min_cutoff}%.")

if "result" in st.session_state:
    result = st.session_state["result"]
    st.divider()

    req_skills_list = result.get("required_skills", [])
    skill_evidence_levels = result.get("skill_evidence_levels", {})
    required_skill_evidence_levels = result.get("required_skill_evidence_levels", {})

    # Reconciled SSOT Tier Counting
    c_dem, c_sub, c_supp, c_list, c_miss = 0, 0, 0, 0, 0
    for sk in req_skills_list:
        ev = required_skill_evidence_levels.get(sk, skill_evidence_levels.get(sk, {}))
        st_code = str(ev.get("status", "missing")).strip().lower()

        if st_code in {"demonstrated", "strong"}:
            c_dem += 1
        elif st_code in {"substitute", "equivalent"}:
            c_sub += 1
        elif st_code in {"supporting", "related"}:
            c_supp += 1
        elif st_code in {"listed", "listed_only", "listed only"}:
            c_list += 1
        else:
            c_miss += 1

    if req_skills_list:
        total_earned = (c_dem * 1.0) + (c_sub * 0.75) + (c_supp * 0.70) + (c_list * 0.40)
        skill_score = (total_earned / len(req_skills_list)) * 100.0
    else:
        skill_score = 0.0

    semantic_score = float(result["semantic_score"])
    skill_score_available = bool(req_skills_list)
    final_score = (semantic_score * 0.60 + skill_score * 0.40) if skill_score_available else semantic_score

    result["final_score"] = final_score
    result["skill_score"] = skill_score
    result["semantic_score"] = semantic_score

    candidate_label = st.session_state.get("resume_name", "Candidate")
    career_recs_pdf = get_alternative_pathways(result.get("resume_skills", []))
    pdf_bytes = generate_candidate_pdf(candidate_label, result, career_recs_pdf)

    top_c1, top_c2 = st.columns([3, 1])
    with top_c1:
        render_html(
            f"""
            <div class="section-header" style="margin-bottom:0px;">
                <div class="section-title">Screening Report: {candidate_label}</div>
                <div class="section-description" style="color:#94a3b8;">
                    Evidence-based compatibility analysis for uploaded resume and target job.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with top_c2:
        st.download_button(
            label="📄 Download Evaluation PDF",
            data=pdf_bytes,
            file_name=f"{candidate_label}_Screening_Brief.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.write("")

    tab_summary, tab_skills, tab_resp_caps, tab_career = st.tabs([
        "📊 Executive Summary", 
        "🛠️ Skills & Evidence", 
        "🎯 Responsibilities & Capabilities", 
        "🧭 Career & Role Fit"
    ])

    # --------------------------------------------------------
    # TAB 1: EXECUTIVE SUMMARY
    # --------------------------------------------------------
    with tab_summary:
        score_col, metrics_col = st.columns([1.25, 1.75], gap="large")
        with score_col:
            render_html(
                f"""
                <div class="score-hero">
                    <div class="score-label">Overall Compatibility</div>
                    <div class="score-number">{final_score:.1f}%</div>
                    <div class="score-caption" style="color:#94a3b8;">
                        Calculated from dense semantic alignment (60%) and evidence-weighted skill coverage (40%).
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.progress(min(final_score / 100, 1.0))

        with metrics_col:
            metric1, metric2 = st.columns(2)
            with metric1:
                render_html(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Semantic Compatibility</div>
                        <div class="metric-value">{semantic_score:.1f}%</div>
                        <div class="metric-subtitle" style="color:#94a3b8;">Calibrated MiniLM concept alignment</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with metric2:
                skill_value = f"{skill_score:.1f}%" if skill_score_available else "Not available"
                skill_subtitle = "Evidence-weighted skill coverage" if skill_score_available else "No recognized job skills detected"

                render_html(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Skill Coverage</div>
                        <div class="metric-value">{skill_value}</div>
                        <div class="metric-subtitle" style="color:#94a3b8;">{skill_subtitle}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.write("")
            # Clean 4-Card Summary Grid
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                render_html(
                    f"""<div class="metric-card" style="border-left: 3px solid #10b981;">
                        <div class="metric-label">Demonstrated (1.0x)</div>
                        <div class="metric-value" style="color:#34d399;">{c_dem}</div>
                        <div class="metric-subtitle" style="color:#94a3b8;">Verified in work / projects</div>
                    </div>""",
                    unsafe_allow_html=True
                )
            with m2:
                render_html(
                    f"""<div class="metric-card" style="border-left: 3px solid #f59e0b;">
                        <div class="metric-label">Sub / Supp (0.75/0.70x)</div>
                        <div class="metric-value" style="color:#fbbf24;">{c_sub + c_supp}</div>
                        <div class="metric-subtitle" style="color:#94a3b8;">{c_sub} sub • {c_supp} supp</div>
                    </div>""",
                    unsafe_allow_html=True
                )
            with m3:
                render_html(
                    f"""<div class="metric-card" style="border-left: 3px solid #3b82f6;">
                        <div class="metric-label">Listed Only (0.40x)</div>
                        <div class="metric-value" style="color:#60a5fa;">{c_list}</div>
                        <div class="metric-subtitle" style="color:#94a3b8;">Technical skills list</div>
                    </div>""",
                    unsafe_allow_html=True
                )
            with m4:
                render_html(
                    f"""<div class="metric-card" style="border-left: 3px solid #ef4444;">
                        <div class="metric-label">Missing (0.0x)</div>
                        <div class="metric-value" style="color:#f87171;">{c_miss}</div>
                        <div class="metric-subtitle" style="color:#94a3b8;">No evidence found</div>
                    </div>""",
                    unsafe_allow_html=True
                )

        st.write("")
        semantic_contribution = semantic_score * 0.60
        skill_contribution = skill_score * 0.40

        render_html(
            f"""
            <div class="explanation-card">
                <div class="explanation-title">🔍 Explainable Scoring Breakdown</div>
                <div class="explanation-text" style="color: #cbd5e1;">
                    <strong>Formula:</strong> (Semantic Score × 60%) + (Skill Coverage × 40%)<br><br>
                    • <strong>Semantic Alignment:</strong> {semantic_score:.1f}% × 60% = {semantic_contribution:.1f} points<br>
                    • <strong>Evidence-Weighted Skills:</strong> {skill_score:.1f}% × 40% = {skill_contribution:.1f} points<br><br>
                    <strong>Final Compatibility = {final_score:.1f}%</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # TAB 2: SKILLS & EVIDENCE
    # --------------------------------------------------------
    with tab_skills:
        demonstrated = []
        substitutes = []
        supporting = []
        listed = []
        missing = []

        for skill in req_skills_list:
            evidence = get_normalized_skill_evidence(skill, skill_evidence_levels, required_skill_evidence_levels)
            raw_status = str(evidence.get("status", "missing")).strip().lower()

            if raw_status in {"demonstrated", "strong"}:
                demonstrated.append((skill, evidence))
            elif raw_status in {"substitute", "equivalent"}:
                substitutes.append((skill, evidence))
            elif raw_status in {"supporting", "related"}:
                supporting.append((skill, evidence))
            elif raw_status in {"listed", "listed_only", "listed only"}:
                listed.append((skill, evidence))
            else:
                missing.append((skill, evidence))

        # Sort missing skills by JD centrality (core skills first)
        missing.sort(key=lambda item: JD_CENTRALITY.index(item[0].lower()) if item[0].lower() in JD_CENTRALITY else 99)

        skill_col1, skill_col2 = st.columns(2, gap="large")
        with skill_col1:
            st.markdown("### ✅ Matched Competencies")
            
            if demonstrated or substitutes:
                st.caption("Verified in Projects / Work (1.0x / 0.75x)")
                v_chips = ""
                for skill, ev in (demonstrated + substitutes):
                    disp = format_skill_display(skill)
                    if ev.get("status") == "substitute":
                        sub_t = format_skill_display(ev.get("substitute_tool", "Eq"))
                        v_chips += f'<span class="chip chip-match" style="border: 1px dashed #34d399;">✓ {disp} (Sub: {sub_t})</span> '
                    else:
                        v_chips += f'<span class="chip chip-match">✓ {disp}</span> '
                st.markdown(v_chips, unsafe_allow_html=True)

            if supporting:
                st.caption("Supporting Context (0.70x)")
                supp_chips = "".join(f'<span class="chip chip-match" style="border-color: #fbbf24; color: #fef3c7;">△ {format_skill_display(s)}</span> ' for s, ev in supporting)
                st.markdown(supp_chips, unsafe_allow_html=True)

            if listed:
                st.caption("Listed Only without active project sentence (0.40x)")
                list_chips = "".join(f'<span class="chip chip-match" style="border-color: #60a5fa; color: #dbeafe;">• {format_skill_display(s)}</span> ' for s, ev in listed)
                st.markdown(list_chips, unsafe_allow_html=True)

            if not (demonstrated or substitutes or supporting or listed):
                st.info("No required skills were matched.")

        with skill_col2:
            st.markdown("### ❌ Unmatched Skill Gaps")
            if missing:
                chips = "".join(f'<span class="chip chip-missing">! {format_skill_display(s)}</span> ' for s, ev in missing)
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.success("No unaddressed skill gaps.")

        st.write("")
        with st.expander("🔎 Detailed Skill Evidence Drill-Down", expanded=True):
            if req_skills_list:
                evidence_col1, evidence_col2 = st.columns(2, gap="large")
                with evidence_col1:
                    if demonstrated:
                        st.markdown("#### 🟢 Demonstrated in Work / Projects (1.0x)")
                        for skill, evidence in demonstrated:
                            disp_name = format_skill_display(skill)
                            sections = evidence.get("sections", [])
                            section_text = ", ".join(str(s).replace("_", " ").title() for s in sections if str(s).strip()) or "Projects / Experience"
                            snippet = clean_snippet_text(evidence.get("snippet", ""))
                            
                            snippet_html = f"""
                            <div style="margin-top:8px; padding:8px 12px; background:rgba(56, 189, 248, 0.08); border-left:3px solid #38bdf8; border-radius:4px; font-style:italic; font-size:12.5px; color:#cbd5e1;">
                                "{snippet}"
                            </div>
                            """ if snippet else "<div style='font-size:12px; color:#94a3b8; margin-top:4px;'>Verified delivery in active project/work sentences.</div>"

                            render_html(
                                f"""
                                <div class="explanation-card" style="margin-bottom:10px;">
                                    <div class="explanation-title">✓ {disp_name}</div>
                                    <div class="explanation-text" style="color:#cbd5e1;">
                                        <strong>Status: Demonstrated (1.0x)</strong> • Verified in: <strong>{section_text}</strong>
                                        {snippet_html}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    if substitutes or supporting:
                        st.markdown("#### 🟡 Supporting / Industry Substitute (0.75x / 0.70x)")
                        for skill, evidence in substitutes:
                            disp_name = format_skill_display(skill)
                            sub_name = format_skill_display(evidence.get("substitute_tool", "Equivalent tool"))
                            render_html(
                                f"""
                                <div class="explanation-card" style="margin-bottom:10px; border-left: 3px solid #f59e0b;">
                                    <div class="explanation-title" style="color:#fbbf24;">△ {disp_name} (Sub: {sub_name})</div>
                                    <div class="explanation-text" style="color:#cbd5e1;">
                                        <strong>Status: Substitute Tool (0.75x)</strong><br>
                                        Candidate demonstrates <strong>{sub_name}</strong>, satisfying this requirement via industry tooling equivalence.
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        for skill, evidence in supporting:
                            disp_name = format_skill_display(skill)
                            sections = evidence.get("sections", [])
                            section_text = ", ".join(str(s).replace("_", " ").title() for s in sections if str(s).strip()) or "Internship / Education"
                            snippet = clean_snippet_text(evidence.get("snippet", ""))
                            snippet_html = f"""
                            <div style="margin-top:8px; padding:8px 12px; background:rgba(251, 191, 36, 0.08); border-left:3px solid #fbbf24; border-radius:4px; font-style:italic; font-size:12.5px; color:#cbd5e1;">
                                "{snippet}"
                            </div>
                            """ if snippet else f"<div style='font-size:12.5px; color:#cbd5e1; margin-top:4px;'>Verified in {section_text} records.</div>"

                            render_html(
                                f"""
                                <div class="explanation-card" style="margin-bottom:10px; border-left: 3px solid #f59e0b;">
                                    <div class="explanation-title" style="color:#fbbf24;">△ {disp_name}</div>
                                    <div class="explanation-text" style="color:#cbd5e1;">
                                        <strong>Status: Supporting (0.70x)</strong> • Section: <strong>{section_text}</strong>
                                        {snippet_html}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                with evidence_col2:
                    if listed:
                        st.markdown("#### 🔵 Listed Only (0.40x Partial Credit)")
                        for skill, evidence in listed:
                            disp_name = format_skill_display(skill)
                            render_html(
                                f"""
                                <div class="explanation-card" style="margin-bottom:10px;">
                                    <div class="explanation-title">• {disp_name}</div>
                                    <div class="explanation-text" style="color:#cbd5e1;">
                                        <strong>Status: Listed Only (0.4x)</strong><br>
                                        Found only in Skills section without active project sentence context.
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    if missing:
                        st.markdown("#### 🔴 Missing Requirements (0.0x)")
                        for skill, evidence in missing:
                            disp_name = format_skill_display(skill)
                            render_html(
                                f"""
                                <div class="improvement-card" style="margin-bottom:10px;">
                                    <div class="improvement-title">! {disp_name}</div>
                                    <div class="improvement-text" style="color:#cbd5e1;">
                                        <strong>Status: Missing (0.0x)</strong><br>
                                        No meaningful evidence detected across resume sections.
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
            else:
                st.info("No required skill evidence is available.")

        # ATS BULLET OPTIMIZER
        bullet_gap_options = [s for s, ev in missing]
        if bullet_gap_options:
            st.write("")
            with st.expander("✨ Resume Bullet-Point Optimizer (ATS Formatted)", expanded=True):
                st.markdown(
                    "<div style='font-size:13px; color:#cbd5e1; margin-bottom:12px;'>"
                    "Action-driven bullet templates customized to address candidate skill gaps. "
                    "<strong>Note:</strong> Candidates should only include bullets for competencies they legitimately practiced."
                    "</div>",
                    unsafe_allow_html=True
                )
                
                selected_gap = st.selectbox(
                    "Choose a gap to generate bullet points for:",
                    options=bullet_gap_options,
                    format_func=format_skill_display,
                    key="bullet_skill_selector"
                )
                
                if selected_gap:
                    bullets = generate_resume_bullets(selected_gap)
                    for b in bullets:
                        st.code(b, language="text")

        # SMART RECRUITER INTERVIEW QUESTIONS
        subs_map = {s: ev.get("substitute_tool", "Eq") for s, ev in substitutes}
        interview_questions = generate_interview_questions(
            missing_skills=[s for s, ev in missing],
            substituted_skills=subs_map,
            supporting_skills=[s for s, ev in supporting],
            listed_skills=[s for s, ev in listed],
            demonstrated_skills=[s for s, ev in demonstrated],
            final_score=final_score
        )

        if interview_questions:
            st.write("")
            with st.expander("💼 Smart Technical Interview Question Generator", expanded=True):
                st.markdown(
                    "<div style='font-size:13px; color:#cbd5e1; margin-bottom:14px;'>"
                    "Tailored interview questions automatically generated to evaluate detected skill gaps, "
                    "tool substitutions, and unverified competencies during screening calls."
                    "</div>",
                    unsafe_allow_html=True
                )
                for q_idx, q_item in enumerate(interview_questions):
                    badge_color = "#ef4444" if "Missing" in q_item["type"] or "Gap" in q_item["type"] else ("#f59e0b" if "Tool" in q_item["type"] or "Supporting" in q_item["type"] else ("#10b981" if "Project" in q_item["type"] else "#3b82f6"))
                    render_html(
                        f"""
                        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-left: 3px solid {badge_color}; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <strong style="color: #f8fafc; font-size: 0.95rem;">{q_item['category']}</strong>
                                <span style="background: rgba(255, 255, 255, 0.07); color: {badge_color}; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 700;">
                                    {q_item['type']}
                                </span>
                            </div>
                            <div style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.45;">
                                "{q_item['question']}"
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    # --------------------------------------------------------
    # TAB 3: RESPONSIBILITIES & CAPABILITIES
    # --------------------------------------------------------
    with tab_resp_caps:
        with st.expander("🎯 Job Responsibility Analysis", expanded=True):
            responsibility_analysis = result.get("responsibility_analysis", {})
            responsibility_items = responsibility_analysis.get("responsibilities", [])

            if responsibility_items:
                for item in responsibility_items:
                    st_val = item.get("status")
                    title = item.get("responsibility", "Responsibility")
                    if st_val == "strong":
                        raw_evs = [str(e.get("evidence", "")).strip() for e in item.get("evidence", []) if str(e.get("evidence", "")).strip()]
                        ev_txt = ", ".join(sorted(list(set(raw_evs)), key=len, reverse=True)) or "Explicitly demonstrated in resume text."
                        render_html(
                            f"""<div class="explanation-card" style="margin-bottom:10px; border-left:3px solid #10b981;">
                                <div class="explanation-title">✓ {title}</div>
                                <div class="explanation-text" style="color:#cbd5e1;"><strong>Resume Evidence:</strong> {ev_txt}</div>
                            </div>""",
                            unsafe_allow_html=True
                        )
                    elif st_val == "related":
                        ev_txt = ", ".join(set(format_skill_display(ev.get("skill", "")) for ev in item.get("related_evidence", []))) or "Related skill context"
                        render_html(
                            f"""<div class="explanation-card" style="margin-bottom:10px; border-left:3px solid #f59e0b;">
                                <div class="explanation-title">△ {title}</div>
                                <div class="explanation-text" style="color:#cbd5e1;"><strong>Related Context:</strong> {ev_txt} (Partial Context)</div>
                            </div>""",
                            unsafe_allow_html=True
                        )
                    else:
                        render_html(
                            f"""<div class="improvement-card" style="margin-bottom:10px;">
                                <div class="improvement-title">! {title}</div>
                                <div class="improvement-text" style="color:#cbd5e1;">{item.get('reason', 'No meaningful evidence detected.')}</div>
                            </div>""",
                            unsafe_allow_html=True
                        )
            else:
                st.info("Paste full responsibility sentences into the JD to trigger deep responsibility matching.")

        st.write("")
        st.markdown("### 🎯 High-Level Capability Analysis")
        
        job_capabilities = analyze_job_relevant_capabilities(
            result.get("resume_skills", []),
            req_skills_list,
            skill_evidence_levels=required_skill_evidence_levels
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
                    missing_caps = capability.get("missing_skills", [])

                    status = "✓ Strong Alignment" if alignment == "Strong Alignment" else ("△ Partial Alignment" if alignment == "Partial Alignment" else "! Low Alignment")
                    type_icon = "🎯" if requirement_type == "Required" else "↳"

                    render_html(
                        f"""
                        <div class="capability-card">
                            <div class="capability-name">{name}</div>
                            <div class="capability-status">
                                {type_icon} {requirement_type} • {status} • {coverage:.1f}% evidence coverage
                            </div>
                            <div class="capability-description" style="color:#cbd5e1;">{description}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if matched:
                        st.caption("Matched job evidence")
                        st.markdown("".join(f'<span class="chip chip-match">✓ {format_skill_display(s)}</span> ' for s in matched), unsafe_allow_html=True)
                    if missing_caps:
                        st.caption("Capability gaps")
                        st.markdown("".join(f'<span class="chip chip-missing">! {format_skill_display(s)}</span> ' for s in missing_caps), unsafe_allow_html=True)

    # --------------------------------------------------------
    # TAB 4: CAREER & ROLE FIT
    # --------------------------------------------------------
    with tab_career:
        career_recs = get_alternative_pathways(result.get("resume_skills", []))
        if career_recs:
            pathways_html = "".join([
                f"""
                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 14px 18px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <strong style="color: #60a5fa; font-size: 1.05rem;">{p['role']}</strong>
                        <span style="background: rgba(59, 130, 246, 0.18); color: #93c5fd; padding: 3px 10px; border-radius: 999px; font-size: 0.85rem; font-weight: 700;">
                            {p['fit']}% Market Skill Overlap
                        </span>
                    </div>
                    <div style="font-size: 0.85rem; color: #cbd5e1;">
                        <strong>Transferable Competencies:</strong> {', '.join(format_skill_display(s) for s in p['skills']) if p['skills'] else 'Foundational tech competencies'}
                    </div>
                </div>
                """ for p in career_recs
            ])

            render_html(
                f"""
                <div style="margin-top: 10px; margin-bottom: 24px; padding: 20px; border-radius: 18px; background: rgba(15, 23, 42, 0.7); border: 1px solid #1e293b;">
                    <div style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; margin-bottom: 4px; display: flex; align-items: center; gap: 8px;">
                        <span>🧭</span> Cross-Functional Career Pathways (Broad Market Transferability)
                    </div>
                    <div style="font-size: 0.82rem; color: #94a3b8; margin-bottom: 16px;">
                        Measures JD-independent market skill transferability against global engineering and data families.
                    </div>
                    {pathways_html}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### 🎯 Recommended Roles (Targeted Profile Alignment)")
        st.caption("Evidence-weighted candidate fit evaluated against structured role competency definitions.")
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
                    gap_label = "gap" if missing_cnt == 1 else "gaps"

                    render_html(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">RANK {index + 1}</div>
                            <div class="metric-value" style="font-size:20px;">{role_result["role"]}</div>
                            <div style="color:#93c5fd;font-size:24px;font-weight:800;margin-top:8px;">{coverage:.1f}%</div>
                            <div class="metric-subtitle" style="color:#94a3b8;">{status_icon} {status} • {matched_cnt} matched • {missing_cnt} {gap_label}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        st.write("")
        with st.expander("🧠 Supporting Module: BERT Resume Classification", expanded=False):
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
                                <div style="font-size:11px; color:#94a3b8; text-align:center; margin-top:2px;">Segment Vote Share</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                st.caption(
                    "Note: Fine-tuned BERT sequence classification acts as an auxiliary domain predictor via segmented resume voting. "
                    "It does not penalize or alter the deterministic MiniLM + evidence scoring formula."
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
            <strong style="color: #f1f5f9;">Responsible AI & Ethical Hiring Notice</strong><br><br>
            <span style="color: #cbd5e1;">
            This system provides augmented decision-support information for talent evaluation.
            Compatibility scores, BERT domain classifications, and detected capabilities are heuristic indicators 
            and should never serve as the sole or automated determinant for employment decisions.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

render_html(
    """
    <div class="footer" style="color: #94a3b8;">
        ResumeIQ • Explainable Deep Learning & NLP Resume Intelligence
    </div>
    """,
    unsafe_allow_html=True
)