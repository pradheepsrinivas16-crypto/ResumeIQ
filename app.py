import streamlit as st

import sys

import os

import textwrap





# ============================================================

# PROJECT PATH

# ============================================================



SRC_PATH = os.path.join(

    os.path.dirname(__file__),

    "src"

)



if SRC_PATH not in sys.path:

    sys.path.append(SRC_PATH)





from resume_parser import extract_resume_text

from screening_engine import screen_resume





# ============================================================

# PAGE CONFIG

# ============================================================



st.set_page_config(

    page_title="ResumeIQ | AI Resume Intelligence",

    page_icon="◈",

    layout="wide",

    initial_sidebar_state="expanded"

)





# ============================================================

# HTML RENDER HELPER

# ============================================================



def render_html(html, **kwargs):

    """Render raw HTML directly so Streamlit never treats it as Markdown code."""

    st.html(textwrap.dedent(html))





# ============================================================

# PROFESSIONAL UI CSS

# ============================================================



render_html(

    """

    <style>



    /* ======================================================

       GLOBAL

       ====================================================== */



    .stApp {

        background:

            radial-gradient(

                circle at 15% 10%,

                rgba(59, 130, 246, 0.10),

                transparent 28%

            ),

            radial-gradient(

                circle at 85% 15%,

                rgba(139, 92, 246, 0.08),

                transparent 25%

            ),

            #080b12;

        color: #f8fafc;

    }



    .block-container {

        max-width: 1400px;

        padding-top: 2rem;

        padding-bottom: 5rem;

    }



    /* ======================================================

       SIDEBAR

       ====================================================== */



    section[data-testid="stSidebar"] {

        background: #0b0f17;

        border-right: 1px solid #1e293b;

    }



    section[data-testid="stSidebar"] * {

        color: #e2e8f0;

    }



    .sidebar-brand {

        font-size: 25px;

        font-weight: 800;

        letter-spacing: -0.5px;

        margin-bottom: 3px;

    }



    .sidebar-subtitle {

        color: #94a3b8;

        font-size: 13px;

        margin-bottom: 20px;

    }



    .sidebar-section {

        color: #64748b;

        font-size: 11px;

        font-weight: 800;

        text-transform: uppercase;

        letter-spacing: 1.2px;

        margin-top: 22px;

        margin-bottom: 10px;

    }



    /* ======================================================

       HERO

       ====================================================== */



    .hero {

        padding: 10px 0 24px 0;

    }



    .hero-badge {

        display: inline-block;

        padding: 6px 12px;

        border-radius: 999px;

        background: rgba(59, 130, 246, 0.10);

        border: 1px solid rgba(59, 130, 246, 0.25);

        color: #93c5fd;

        font-size: 12px;

        font-weight: 700;

        margin-bottom: 13px;

    }



    .hero-title {

        font-size: 48px;

        line-height: 1.05;

        font-weight: 850;

        letter-spacing: -1.8px;

        margin: 0;

        color: #f8fafc;

    }



    .hero-title span {

        color: #60a5fa;

    }



    .hero-description {

        margin-top: 12px;

        color: #94a3b8;

        font-size: 16px;

        max-width: 760px;

        line-height: 1.6;

    }



    /* ======================================================

       INPUT CARDS

       ====================================================== */



    .input-card {

        background: rgba(15, 23, 42, 0.80);

        border: 1px solid #1e293b;

        border-radius: 18px;

        padding: 22px;

        min-height: 260px;

    }



    .input-title {

        font-size: 18px;

        font-weight: 750;

        color: #f8fafc;

        margin-bottom: 4px;

    }



    .input-description {

        color: #64748b;

        font-size: 13px;

        margin-bottom: 15px;

    }



    /* ======================================================

       BUTTON

       ====================================================== */



    .stButton > button {

        border-radius: 12px;

        min-height: 48px;

        font-weight: 750;

        border: 1px solid rgba(96, 165, 250, 0.35);

        transition: 0.2s ease;

    }



    .stButton > button:hover {

        border-color: #60a5fa;

        transform: translateY(-1px);

    }



    /* ======================================================

       SECTION HEADERS

       ====================================================== */



    .section-header {

        margin-top: 32px;

        margin-bottom: 16px;

    }



    .section-title {

        font-size: 24px;

        font-weight: 800;

        color: #f8fafc;

        margin-bottom: 3px;

    }



    .section-description {

        color: #64748b;

        font-size: 13px;

    }



    /* ======================================================

       SCORE HERO

       ====================================================== */



    .score-hero {

        background:

            linear-gradient(

                135deg,

                rgba(30, 64, 175, 0.20),

                rgba(15, 23, 42, 0.85)

            );

        border: 1px solid #263a67;

        border-radius: 22px;

        padding: 28px;

        min-height: 245px;

    }



    .score-label {

        color: #93c5fd;

        font-size: 12px;

        text-transform: uppercase;

        letter-spacing: 1.4px;

        font-weight: 800;

    }



    .score-number {

        font-size: 72px;

        font-weight: 900;

        line-height: 1;

        letter-spacing: -3px;

        margin-top: 8px;

        color: #f8fafc;

    }



    .score-caption {

        color: #94a3b8;

        margin-top: 9px;

        font-size: 14px;

    }



    /* ======================================================

       METRIC CARDS

       ====================================================== */



    .metric-card {

        background: #0f172a;

        border: 1px solid #1e293b;

        border-radius: 18px;

        padding: 22px;

        min-height: 118px;

    }



    .metric-label {

        color: #64748b;

        font-size: 12px;

        font-weight: 750;

        text-transform: uppercase;

        letter-spacing: 0.8px;

    }



    .metric-value {

        color: #f8fafc;

        font-size: 32px;

        font-weight: 850;

        margin-top: 7px;

    }



    .metric-subtitle {

        color: #64748b;

        font-size: 12px;

        margin-top: 3px;

    }



    /* ======================================================

       EXPLANATION CARD

       ====================================================== */



    .explanation-card {

        background: #0f172a;

        border: 1px solid #1e293b;

        border-radius: 18px;

        padding: 24px;

    }



    .explanation-title {

        color: #f8fafc;

        font-size: 18px;

        font-weight: 800;

        margin-bottom: 10px;

    }



    .explanation-text {

        color: #94a3b8;

        line-height: 1.65;

        font-size: 14px;

    }



    /* ======================================================

       SKILL CHIPS

       ====================================================== */



    .chip {

        display: inline-block;

        padding: 7px 11px;

        margin: 4px 5px 4px 0;

        border-radius: 999px;

        font-size: 12px;

        font-weight: 650;

    }



    .chip-match {

        color: #86efac;

        background: rgba(34, 197, 94, 0.09);

        border: 1px solid rgba(34, 197, 94, 0.22);

    }



    .chip-missing {

        color: #fca5a5;

        background: rgba(239, 68, 68, 0.09);

        border: 1px solid rgba(239, 68, 68, 0.22);

    }



    .chip-neutral {

        color: #cbd5e1;

        background: rgba(148, 163, 184, 0.08);

        border: 1px solid #334155;

    }



    /* ======================================================

       IMPROVEMENT CARDS

       ====================================================== */



    .improvement-card {

        background: #0f172a;

        border: 1px solid #1e293b;

        border-left: 3px solid #f59e0b;

        border-radius: 14px;

        padding: 16px 18px;

        margin-bottom: 10px;

    }



    .improvement-title {

        color: #fbbf24;

        font-size: 14px;

        font-weight: 750;

    }



    .improvement-text {

        color: #94a3b8;

        font-size: 13px;

        margin-top: 5px;

        line-height: 1.55;

    }



    /* ======================================================

       BERT

       ====================================================== */



    .bert-card {

        background:

            linear-gradient(

                135deg,

                rgba(139, 92, 246, 0.12),

                rgba(15, 23, 42, 0.9)

            );

        border: 1px solid rgba(139, 92, 246, 0.25);

        border-radius: 18px;

        padding: 22px;

        margin-bottom: 10px;

    }



    .bert-rank {

        color: #a78bfa;

        font-weight: 800;

        font-size: 12px;

    }



    .bert-category {

        color: #f8fafc;

        font-size: 17px;

        font-weight: 750;

        margin-top: 4px;

    }



    .bert-confidence {

        color: #c4b5fd;

        font-size: 14px;

        font-weight: 700;

    }



    /* ======================================================

       CAPABILITY

       ====================================================== */



    .capability-card {

        background: #0f172a;

        border: 1px solid #1e293b;

        border-radius: 16px;

        padding: 20px;

        margin-bottom: 12px;

    }



    .capability-name {

        font-size: 17px;

        font-weight: 800;

        color: #f8fafc;

    }



    .capability-status {

        color: #86efac;

        font-size: 12px;

        font-weight: 750;

    }



    .capability-description {

        color: #64748b;

        font-size: 13px;

        margin-top: 7px;

        line-height: 1.5;

    }



    /* ======================================================

       INFO / RESPONSIBLE AI

       ====================================================== */



    .responsible-ai {

        background: rgba(59, 130, 246, 0.06);

        border: 1px solid rgba(59, 130, 246, 0.18);

        border-radius: 14px;

        padding: 17px;

        color: #94a3b8;

        font-size: 12px;

        line-height: 1.6;

    }



    /* ======================================================

       FOOTER

       ====================================================== */



    .footer {

        text-align: center;

        color: #475569;

        font-size: 12px;

        margin-top: 55px;

        padding-top: 22px;

        border-top: 1px solid #1e293b;

    }



    </style>

    """,

    unsafe_allow_html=True

)





# ============================================================

# SIDEBAR

# ============================================================



with st.sidebar:



    st.markdown(

        '<div class="sidebar-brand">◈ ResumeIQ</div>',

        unsafe_allow_html=True

    )



    st.markdown(

        '<div class="sidebar-subtitle">'

        'Resume Intelligence Platform'

        '</div>',

        unsafe_allow_html=True

    )



    st.divider()



    st.markdown(

        '<div class="sidebar-section">AI Models</div>',

        unsafe_allow_html=True

    )



    st.write("🧠 BERT")

    st.write("🔎 Sentence Transformer")

    st.write("🛠️ Skill Intelligence")

    st.write("💡 Capability Engine")



    st.markdown(

        '<div class="sidebar-section">Analysis</div>',

        unsafe_allow_html=True

    )



    st.write("✓ Semantic compatibility")

    st.write("✓ Skill coverage")

    st.write("✓ Missing-skill detection")

    st.write("✓ Role classification")

    st.write("✓ Capability analysis")

    st.write("✓ Improvement recommendations")



    st.divider()



    st.caption(

        "Deep Learning • NLP • Explainable Screening"

    )





# ============================================================

# HERO

# ============================================================



render_html(

    """

    <div class="hero">



        <div class="hero-badge">

            DEEP LEARNING RESUME INTELLIGENCE

        </div>



        <div class="hero-title">

            Resume<span>IQ</span>

        </div>



        <div class="hero-description">

            Analyze how closely a resume aligns with a job description,

            understand the reasons behind the compatibility score,

            identify skill gaps, and generate evidence-based improvement

            recommendations.

        </div>



    </div>

    """,

    unsafe_allow_html=True

)





# ============================================================

# INPUT AREA

# ============================================================



input_col1, input_col2 = st.columns(

    [1, 1],

    gap="large"

)





with input_col1:



    render_html(

        """

        <div class="input-card">



            <div class="input-title">

                📄 Candidate Resume

            </div>



            <div class="input-description">

                Upload the candidate's resume in PDF or DOCX format.

            </div>



        </div>

        """,

        unsafe_allow_html=True

    )



    uploaded_file = st.file_uploader(

        "Upload resume",

        type=["pdf", "docx"],

        label_visibility="collapsed"

    )





with input_col2:



    render_html(

        """

        <div class="input-card">



            <div class="input-title">

                💼 Target Job

            </div>



            <div class="input-description">

                Paste the job description or required skills.

            </div>



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

        )

    )





st.write("")





analyze_button = st.button(

    "🚀  Analyze Resume Compatibility",

    use_container_width=True,

    type="primary"

)





# ============================================================

# ANALYSIS

# ============================================================



if analyze_button:



    if uploaded_file is None:



        st.error(

            "Please upload a resume before starting the analysis."

        )



    elif not job_description.strip():



        st.error(

            "Please enter a job description before starting the analysis."

        )



    else:



        temp_path = os.path.join(

            os.path.dirname(__file__),

            uploaded_file.name

        )



        try:



            with st.spinner(

                "Running resume intelligence analysis..."

            ):



                # Save uploaded file

                with open(

                    temp_path,

                    "wb"

                ) as f:



                    f.write(

                        uploaded_file.getbuffer()

                    )



                # Extract text

                resume_text = extract_resume_text(

                    temp_path

                )



                # Run complete screening engine

                result = screen_resume(

                    resume_text,

                    job_description

                )



                st.session_state["result"] = result



                st.session_state["resume_name"] = (

                    uploaded_file.name

                )



        except Exception as e:



            st.error(

                f"Analysis failed: {e}"

            )



        finally:



            if os.path.exists(temp_path):



                os.remove(temp_path)





# ============================================================

# RESULTS

# ============================================================



if "result" in st.session_state:



    result = st.session_state["result"]



    st.divider()



    # ========================================================

    # REPORT HEADER

    # ========================================================



    render_html(

        """

        <div class="section-header">



            <div class="section-title">

                Screening Report

            </div>



            <div class="section-description">

                Evidence-based compatibility analysis for the

                uploaded resume and target job.

            </div>



        </div>

        """,

        unsafe_allow_html=True

    )





    # ========================================================

    # SCORE HERO

    # ========================================================



    score_col, metrics_col = st.columns(

        [1.25, 1.75],

        gap="large"

    )





    with score_col:



        score = float(

            result["final_score"]

        )



        render_html(

            f"""

            <div class="score-hero">



                <div class="score-label">

                    Overall Compatibility

                </div>



                <div class="score-number">

                    {score:.1f}%

                </div>



                <div class="score-caption">

                    Compatibility score based on semantic

                    alignment and detected skill coverage.

                </div>



            </div>

            """,

            unsafe_allow_html=True

        )



        st.progress(

            min(score / 100, 1.0)

        )





    with metrics_col:



        metric1, metric2 = st.columns(2)



        with metric1:



            render_html(

                f"""

                <div class="metric-card">



                    <div class="metric-label">

                        Semantic Compatibility

                    </div>



                    <div class="metric-value">

                        {result["semantic_score"]:.1f}%

                    </div>



                    <div class="metric-subtitle">

                        Resume ↔ job description meaning

                    </div>



                </div>

                """,

                unsafe_allow_html=True

            )



        with metric2:



            render_html(

                f"""

                <div class="metric-card">



                    <div class="metric-label">

                        Skill Coverage

                    </div>



                    <div class="metric-value">

                        {result["skill_score"]:.1f}%

                    </div>



                    <div class="metric-subtitle">

                        Required skills detected in resume

                    </div>



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



                    <div class="metric-label">

                        Skills Matched

                    </div>



                    <div class="metric-value">

                        {len(result["matched_skills"])}

                    </div>



                    <div class="metric-subtitle">

                        Required skills found

                    </div>



                </div>

                """,

                unsafe_allow_html=True

            )



        with metric4:



            render_html(

                f"""

                <div class="metric-card">



                    <div class="metric-label">

                        Skill Gaps

                    </div>



                    <div class="metric-value">

                        {len(result["missing_skills"])}

                    </div>



                    <div class="metric-subtitle">

                        Required skills not detected

                    </div>



                </div>

                """,

                unsafe_allow_html=True

            )





    # ========================================================

    # WHY THIS SCORE?

    # ========================================================



    render_html(

        """

        <div class="section-header">



            <div class="section-title">

                🔍 Why did you get this score?

            </div>



            <div class="section-description">

                Transparent breakdown of how the compatibility

                score was calculated.

            </div>



        </div>

        """,

        unsafe_allow_html=True

    )





    semantic_score = float(

        result["semantic_score"]

    )



    skill_score = float(

        result["skill_score"]

    )



    semantic_contribution = (

        semantic_score * 0.60

    )



    skill_contribution = (

        skill_score * 0.40

    )





    render_html(

        f"""

        <div class="explanation-card">



            <div class="explanation-title">

                Compatibility Score Calculation

            </div>



            <div class="explanation-text">



                Your final compatibility score combines two

                components:



                <br><br>



                <strong>Semantic Compatibility:</strong>

                {semantic_score:.1f}% × 60%

                = {semantic_contribution:.1f} points



                <br>



                <strong>Skill Coverage:</strong>

                {skill_score:.1f}% × 40%

                = {skill_contribution:.1f} points



                <br><br>



                <strong>

                Final Score = {semantic_contribution:.1f}

                + {skill_contribution:.1f}

                = {result["final_score"]:.1f}%

                </strong>



            </div>



        </div>

        """,

        unsafe_allow_html=True

    )





    # ========================================================

    # SMART SCORE EXPLANATION

    # ========================================================



    matched_count = len(

        result.get("matched_skills", [])

    )

    required_count = len(

        result.get("required_skills", [])

    )

    missing_count = len(

        result.get("missing_skills", [])

    )



    score_explanation = result.get(

        "score_explanation",

        []

    )



    # Backward-compatible fallback if the screening engine

    # was not updated yet.

    if not score_explanation:

        score_explanation = [

            f"{matched_count} of {required_count} detected required skills were matched.",

            (
                f"{missing_count} detected job requirements were not found in the resume."

                if missing_count

                else "All detected required skills were found in the resume."

            )

        ]



    explanation_items = ""

    for item in score_explanation:

        explanation_items += (

            f'<div style="margin-bottom:10px;">• {item}</div>'

        )



    render_html(

        f"""

        <div class="explanation-card">

            <div class="explanation-title">

                What influenced the result?

            </div>

            <div class="explanation-text">

                {explanation_items}

            </div>

        </div>

        """,

        unsafe_allow_html=True

    )



    # ========================================================

    # SKILLS

    # ========================================================



    render_html(

        """

        <div class="section-header">



            <div class="section-title">

                🛠️ Skill Analysis

            </div>



            <div class="section-description">

                Skills detected from the job description and

                evidence found in the resume.

            </div>



        </div>

        """,

        unsafe_allow_html=True

    )





    skill_col1, skill_col2 = st.columns(

        2,

        gap="large"

    )





    with skill_col1:



        st.markdown(

            "### ✅ Matched Skills"

        )



        if result["matched_skills"]:



            chips = ""



            for skill in result["matched_skills"]:



                chips += (

                    f'<span class="chip chip-match">'

                    f'✓ {skill}'

                    f'</span>'

                )



            st.markdown(

                chips,

                unsafe_allow_html=True

            )



        else:



            st.info(

                "No required skills were matched."

            )





    with skill_col2:



        st.markdown(

            "### ❌ Missing Skills"

        )



        if result["missing_skills"]:



            chips = ""



            for skill in result["missing_skills"]:



                chips += (

                    f'<span class="chip chip-missing">'

                    f'! {skill}'

                    f'</span>'

                )



            st.markdown(

                chips,

                unsafe_allow_html=True

            )



        else:



            st.success(

                "No detected skill gaps."

            )





    # ========================================================

    # IMPROVEMENT PLAN

    # ========================================================



    render_html(

        """

        <div class="section-header">



            <div class="section-title">

                🚀 How can you improve?

            </div>



            <div class="section-description">

                Actionable recommendations based on the

                requirements detected in the job description.

            </div>



        </div>

        """,

        unsafe_allow_html=True

    )





    if result["missing_skills"]:



        for index, skill in enumerate(

            result["missing_skills"],

            start=1

        ):



            render_html(

                f"""

                <div class="improvement-card">



                    <div class="improvement-title">

                        {index}. {skill}

                    </div>



                    <div class="improvement-text">

                        This requirement appears in the job

                        description but was not detected in

                        the resume. If you genuinely have this

                        experience, consider clearly documenting

                        the relevant project, coursework,

                        certification, or work experience.

                    </div>



                </div>

                """,

                unsafe_allow_html=True

            )



    else:



        st.success(

            "No detected skill gaps. The resume covers all "

            "recognized requirements from the job description."

        )





    # ========================================================

    # CANDIDATE STRENGTHS

    # ========================================================



    render_html(

        """

        <div class="section-header">



            <div class="section-title">

                💪 Candidate Strengths

            </div>



            <div class="section-description">

                Evidence detected from skills that overlap

                with the target job requirements.

            </div>



        </div>

        """,

        unsafe_allow_html=True

    )





    if result["matched_skills"]:



        strengths = ""



        for skill in result["matched_skills"]:



            strengths += (

                f'<span class="chip chip-match">'

                f'✓ {skill}'

                f'</span>'

            )



        st.markdown(

            strengths,

            unsafe_allow_html=True

        )



    else:



        st.info(

            "No matching strengths were detected."

        )





    # ========================================================

    # BERT ROLE ANALYSIS

    # ========================================================



    render_html(

        """

        <div class="section-header">



            <div class="section-title">

                🧠 BERT Resume Classification

            </div>



            <div class="section-description">

                Top categories predicted by the fine-tuned

                BERT resume classification model.

            </div>



        </div>

        """,

        unsafe_allow_html=True

    )





    bert_categories = result.get(

        "bert_categories",

        []

    )





    if bert_categories:



        bert_cols = st.columns(

            len(bert_categories)

        )



        for index, prediction in enumerate(

            bert_categories

        ):



            with bert_cols[index]:



                render_html(

                    f"""

                    <div class="bert-card">



                        <div class="bert-rank">

                            RANK {index + 1}

                        </div>



                        <div class="bert-category">

                            {prediction["category"].title()}

                        </div>



                        <div class="bert-confidence">

                            {prediction["confidence"]:.2f}%

                        </div>



                    </div>

                    """,

                    unsafe_allow_html=True

                )





        st.caption(

            "BERT confidence represents classification probability "

            "across the resume categories. It is not a hiring "

            "probability and is separate from the compatibility score."

        )





    # ========================================================

    # CAPABILITY INTELLIGENCE

    # ========================================================



    render_html(

        """

        <div class="section-header">



            <div class="section-title">

                💡 Capability Intelligence

            </div>



            <div class="section-description">

                Higher-level capabilities inferred from

                detected skill evidence.

            </div>



        </div>

        """,

        unsafe_allow_html=True

    )





    capabilities = result.get(

        "capabilities",

        []

    )





    supported_capabilities = [

        capability

        for capability in capabilities

        if capability.get(

            "supported",

            False

        )

    ]





    if supported_capabilities:



        capability_columns = st.columns(

            2

        )



        for index, capability in enumerate(

            supported_capabilities

        ):



            with capability_columns[

                index % 2

            ]:



                name = capability.get(

                    "capability",

                    "Unknown"

                )



                evidence_count = capability.get(

                    "evidence_count",

                    0

                )



                description = capability.get(

                    "description",

                    ""

                )



                core_matches = capability.get(

                    "core_matches",

                    []

                )



                supporting_matches = capability.get(

                    "supporting_matches",

                    []

                )



                render_html(

                    f"""

                    <div class="capability-card">



                        <div class="capability-name">

                            {name.title()}

                        </div>



                        <div class="capability-status">

                            ✓ Supported •

                            {evidence_count} evidence items

                        </div>



                        <div class="capability-description">

                            {description}

                        </div>



                    </div>

                    """,

                    unsafe_allow_html=True

                )



                if core_matches:



                    st.caption(

                        "Core evidence"

                    )



                    core_chips = ""



                    for skill in core_matches:



                        core_chips += (

                            f'<span class="chip chip-match">'

                            f'{skill}'

                            f'</span>'

                        )



                    st.markdown(

                        core_chips,

                        unsafe_allow_html=True

                    )



                if supporting_matches:



                    st.caption(

                        "Supporting evidence"

                    )



                    supporting_chips = ""



                    for skill in supporting_matches:



                        supporting_chips += (

                            f'<span class="chip chip-neutral">'

                            f'{skill}'

                            f'</span>'

                        )



                    st.markdown(

                        supporting_chips,

                        unsafe_allow_html=True

                    )



    else:



        st.info(

            "No higher-level capabilities had enough "

            "evidence to satisfy the current capability rules."

        )





    # ========================================================

    # COMPLETE CAPABILITY ANALYSIS

    # ========================================================



    with st.expander(

        "🔍 View complete capability analysis"

    ):



        for capability in capabilities:



            name = capability.get(

                "capability",

                "Unknown"

            )



            supported = capability.get(

                "supported",

                False

            )



            evidence_count = capability.get(

                "evidence_count",

                0

            )



            st.markdown(

                f"### {name.title()}"

            )



            if supported:



                st.success(

                    f"Supported • Evidence: {evidence_count}"

                )



            else:



                st.warning(

                    f"Insufficient evidence • "

                    f"Evidence: {evidence_count}"

                )



            st.write(

                "Core evidence:",

                capability.get(

                    "core_matches",

                    []

                )

            )



            st.write(

                "Supporting evidence:",

                capability.get(

                    "supporting_matches",

                    []

                )

            )



            if capability.get(

                "missing_core",

                []

            ):



                st.write(

                    "Missing core:",

                    capability["missing_core"]

                )



            if capability.get(

                "missing_supporting",

                []

            ):



                st.write(

                    "Missing supporting:",

                    capability["missing_supporting"]

                )



            st.divider()





    # ========================================================

    # RESUME SKILLS

    # ========================================================



    render_html(

        """

        <div class="section-header">



            <div class="section-title">

                📄 Skills Detected in Resume

            </div>



            <div class="section-description">

                Skills automatically identified from the

                uploaded resume.

            </div>



        </div>

        """,

        unsafe_allow_html=True

    )





    resume_skills = result.get(

        "resume_skills",

        []

    )





    if resume_skills:



        chips = ""



        for skill in resume_skills:



            chips += (

                f'<span class="chip chip-neutral">'

                f'{skill}'

                f'</span>'

            )



        st.markdown(

            chips,

            unsafe_allow_html=True

        )



    else:



        st.info(

            "No recognized skills were detected."

        )





    # ========================================================

    # JOB REQUIREMENTS

    # ========================================================



    render_html(

        """

        <div class="section-header">



            <div class="section-title">

                📋 Detected Job Requirements

            </div>



            <div class="section-description">

                Recognized skills extracted from the job description.

            </div>



        </div>

        """,

        unsafe_allow_html=True

    )





    required_skills = result.get(

        "required_skills",

        []

    )





    if required_skills:



        chips = ""



        for skill in required_skills:



            if skill in result["matched_skills"]:



                chips += (

                    f'<span class="chip chip-match">'

                    f'✓ {skill}'

                    f'</span>'

                )



            else:



                chips += (

                    f'<span class="chip chip-missing">'

                    f'! {skill}'

                    f'</span>'

                )



        st.markdown(

            chips,

            unsafe_allow_html=True

        )



    else:



        st.info(

            "No recognized skills were detected in the job description."

        )





    # ========================================================

    # RESPONSIBLE AI

    # ========================================================



    st.markdown(

        "<br>",

        unsafe_allow_html=True

    )



    render_html(

        """

        <div class="responsible-ai">



            <strong>Responsible AI Notice</strong><br><br>



            This system provides decision-support information

            based on the uploaded resume and job description.

            Compatibility scores, BERT classifications and

            detected capabilities should not be treated as

            hiring probabilities or used as the sole basis

            for employment decisions. Recommendations should

            reflect genuine candidate experience.



        </div>

        """,

        unsafe_allow_html=True

    )





    # ========================================================

    # FOOTER

    # ========================================================



    render_html(

        """

        <div class="footer">

            ResumeIQ • Deep Learning • NLP • Explainable

            Resume Intelligence

        </div>

        """,

        unsafe_allow_html=True

    )