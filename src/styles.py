import streamlit as st

def render_html(html, **kwargs):
    """Render raw HTML cleanly by stripping extra blank lines."""
    if not html:
        return
    lines = [line.strip() for line in html.strip().splitlines() if line.strip()]
    cleaned = " ".join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

def apply_custom_css():
    """Inject global custom CSS styling for ResumeIQ."""
    render_html(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 15% 10%, rgba(59, 130, 246, 0.10), transparent 28%),
                radial-gradient(circle at 85% 15%, rgba(139, 92, 246, 0.08), transparent 25%),
                #080b12;
            color: #f8fafc;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

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

        .score-hero {
            background: linear-gradient(135deg, rgba(30, 64, 175, 0.20), rgba(15, 23, 42, 0.85));
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

        .bert-card {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.12), rgba(15, 23, 42, 0.9));
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

        .responsible-ai {
            background: rgba(59, 130, 246, 0.06);
            border: 1px solid rgba(59, 130, 246, 0.18);
            border-radius: 14px;
            padding: 17px;
            color: #94a3b8;
            font-size: 12px;
            line-height: 1.6;
        }

        .footer {
            text-align: center;
            color: #475569;
            font-size: 12px;
            margin-top: 55px;
            padding-top: 22px;
            border-top: 1px solid #1e293b;
        }
        /* Ensure Target Job text area has dark background and crisp white readable text */
.stTextArea textarea {
    background-color: #1c2541 !important;
    color: #ffffff !important;
    border: 1px solid #3a506b !important;
    border-radius: 8px !important;
}

/* Ensure radio button labels are bright and readable */
div[data-testid="stRadio"] label p {
    color: #ffffff !important;
    font-size: 14px !important;
}

/* Fix expanders so summary and contents render properly with high contrast */
div[data-testid="stExpander"] {
    background-color: #1c2541 !important;
    border: 1px solid #3a506b !important;
    border-radius: 8px !important;
    margin-bottom: 12px !important;
}

div[data-testid="stExpander"] details summary {
    color: #ffffff !important;
    cursor: pointer !important;
}

div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
    background-color: #0b132b !important;
    color: #e2e8f0 !important;
    padding: 16px !important;
    border-top: 1px solid #3a506b !important;
}
        </style>
        """,
        unsafe_allow_html=True
    )