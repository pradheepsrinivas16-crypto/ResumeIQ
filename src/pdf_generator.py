"""
Candidate Intelligence Brief (PDF Generation)
Generates an executive, single-page PDF brief strictly synchronized with the UI metrics and tiers.
"""

from io import BytesIO
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from src.skill_matcher import format_skill_display

JD_CENTRALITY = [
    "rest api", "react", "sql", "power bi", "javascript", "html", "css",
    "dashboard", "data analysis", "python", "excel", "responsive web design",
    "ui/ux", "git", "figma", "adobe xd", "database", "exploratory data analysis",
    "pandas", "numpy", "kpi", "statistical analysis"
]

def generate_candidate_pdf(candidate_name, screening_result, career_recommendations=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    clean_candidate_title = re.sub(r"\s*\(\d+\)", "", str(candidate_name)).replace(".pdf", "")

    styles = getSampleStyleSheet()
    primary_color = colors.HexColor("#1e293b")
    border_color = colors.HexColor("#cbd5e1")
    text_muted = colors.HexColor("#64748b")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=primary_color
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.0,
        leading=12,
        textColor=text_muted
    )
    h2_style = ParagraphStyle(
        "Heading2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=primary_color,
        spaceAfter=5
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#334155")
    )
    bold_body = ParagraphStyle(
        "BoldBody",
        parent=body_style,
        fontName="Helvetica-Bold"
    )

    story = []

    # 1. Header
    story.append(Paragraph("ResumeIQ • Candidate Intelligence Brief", subtitle_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(f"Screening Evaluation: {clean_candidate_title}", title_style))
    story.append(Paragraph("Augmented decision-support evaluation for target job description", subtitle_style))
    story.append(Spacer(1, 10))

    # 2. Executive Metrics Summary Table
    final_score = float(screening_result.get("final_score", 0))
    semantic_score = float(screening_result.get("semantic_score", 0))
    skill_score = float(screening_result.get("skill_score", 0)) if screening_result.get("skill_score_available", True) else 0.0

    score_data = [
        [
            Paragraph("<b>Overall Compatibility</b>", body_style),
            Paragraph("<b>Semantic Match (60%)</b>", body_style),
            Paragraph("<b>Evidence Skills (40%)</b>", body_style),
            Paragraph("<b>Recommendation</b>", body_style)
        ],
        [
            Paragraph(f"<font size=13 color='#2563eb'><b>{final_score:.1f}%</b></font>", body_style),
            Paragraph(f"<font size=11><b>{semantic_score:.1f}%</b></font>", body_style),
            Paragraph(f"<font size=11><b>{skill_score:.1f}%</b></font>", body_style),
            Paragraph("<b>Strong Fit</b>" if final_score >= 80 else ("<b>Moderate Fit</b>" if final_score >= 50 else "<b>Low Fit</b>"), body_style)
        ]
    ]
    t_score = Table(score_data, colWidths=[130, 130, 130, 150])
    t_score.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_score)
    story.append(Spacer(1, 10))

    # 3. Skills Breakdown
    story.append(Paragraph("Skill Alignment & Evidence Verification", h2_style))
    
    req_skills = screening_result.get("required_skills", [])
    ev_levels = screening_result.get("required_skill_evidence_levels", screening_result.get("skill_evidence_levels", {}))
    
    demonstrated_skills = []
    substitute_skills = []
    supporting_skills = []
    listed_only_skills = []
    missing_skills = []

    for s in req_skills:
        ev = ev_levels.get(s, {})
        status = str(ev.get("status", "missing")).strip().lower()
        disp = format_skill_display(s)

        if status in {"demonstrated", "strong"}:
            demonstrated_skills.append(disp)
        elif status in {"substitute", "equivalent"}:
            sub = format_skill_display(ev.get("substitute_tool", "Equivalent"))
            substitute_skills.append(f"{disp} (Sub: {sub})")
        elif status in {"supporting", "related"}:
            supporting_skills.append(disp)
        elif status in {"listed", "listed_only", "listed only"}:
            listed_only_skills.append(disp)
        else:
            missing_skills.append(s)

    v_str = ", ".join(sorted(demonstrated_skills + substitute_skills)) if (demonstrated_skills or substitute_skills) else "None verified in project/work context."
    supp_str = ", ".join(sorted(supporting_skills)) if supporting_skills else "None (institutional/internship context)."
    l_str = ", ".join(sorted(listed_only_skills)) if listed_only_skills else "None (skills list context)."
    
    sorted_missing = sorted(missing_skills, key=lambda s: JD_CENTRALITY.index(s.lower()) if s.lower() in JD_CENTRALITY else 99)
    m_str = ", ".join(format_skill_display(s) for s in sorted_missing) if sorted_missing else "No unaddressed skill gaps."

    skills_table_data = [
        [Paragraph("<b>Demonstrated / Sub (1.0x / 0.75x):</b>", bold_body), Paragraph(v_str, body_style)],
        [Paragraph("<b>Supporting (0.70x):</b>", bold_body), Paragraph(supp_str, body_style)],
        [Paragraph("<b>Listed Only (0.40x Partial):</b>", bold_body), Paragraph(l_str, body_style)],
        [Paragraph(f"<b>Unmatched Skill Gaps ({len(sorted_missing)}):</b>", bold_body), Paragraph(m_str, body_style)],
    ]
    t_skills = Table(skills_table_data, colWidths=[185, 355])
    t_skills.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
    ]))
    story.append(t_skills)
    story.append(Spacer(1, 10))

    # 4. Gaps & Candidate Priority Follow-up Areas
    story.append(Paragraph("Priority Areas for Technical Follow-up", h2_style))
    if sorted_missing:
        p_areas = [f"• <b>{format_skill_display(s)}</b>: Core job competency not verified on resume. Validate academic coursework or practical labs during technical screening." for s in sorted_missing[:3]]
        p_text = "<br/>".join(p_areas)
    elif listed_only_skills:
        # ACCURATE CLAIM: Candidate has 0 missing, but has listed-only skills
        v_count = len(demonstrated_skills) + len(substitute_skills)
        l_count = len(listed_only_skills)
        p_text = (
            f"Candidate meets all required competencies ({v_count} verified in project/work context, "
            f"{l_count} listed without dedicated project sentences: {', '.join(listed_only_skills)}). "
            f"Focus screening on validating practical depth in listed skills."
        )
    else:
        p_text = "Candidate meets all required technical competencies with active project evidence. Focus interview on architectural and system depth."
    
    story.append(Paragraph(p_text, body_style))
    story.append(Spacer(1, 10))

    # 5. Career & Role Suitability
    story.append(Paragraph("Role Suitability & Market Transferability", h2_style))
    pathways = career_recommendations or []
    if pathways:
        path_strs = [f"<b>{p['role']}</b> ({p['fit']}% market overlap)" for p in pathways[:3]]
        path_text = "<b>Adjacent Career Pathways (JD-Independent):</b> " + " | ".join(path_strs)
    else:
        path_text = "<b>Adjacent Career Pathways (JD-Independent):</b> Technical competencies align with standard software and analytical profiles."
    story.append(Paragraph(path_text, body_style))
    story.append(Spacer(1, 12))

    # 6. Ethical Notice
    notice_text = (
        "<b>Responsible AI & Decision-Support Notice:</b> This briefing document provides heuristic compatibility metrics "
        "calculated from calibrated dense embeddings and evidence-weighted skill parsing. It is designed to assist human recruiters "
        "and should never serve as the sole determinant for employment or interview decisions."
    )
    story.append(Paragraph(notice_text, subtitle_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()