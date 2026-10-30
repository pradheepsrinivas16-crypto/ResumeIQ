"""
Candidate Intelligence Brief (PDF Generation)
Generates an executive, single-page PDF brief strictly synchronized with the UI metrics and tiers.
"""

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from src.skill_matcher import format_skill_display

JD_CENTRALITY = [
    "sql", "power bi", "dashboard", "data analysis", "excel", 
    "python", "data visualization", "kpi", "database", 
    "exploratory data analysis", "pandas", "statistical analysis", "numpy"
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

    styles = getSampleStyleSheet()
    primary_color = colors.HexColor("#1e293b")
    accent_color = colors.HexColor("#2563eb")
    border_color = colors.HexColor("#cbd5e1")
    text_muted = colors.HexColor("#64748b")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=primary_color
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=text_muted
    )
    h2_style = ParagraphStyle(
        "Heading2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=primary_color,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
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
    story.append(Paragraph(f"Screening Evaluation: {candidate_name}", title_style))
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
            Paragraph(f"<font size=14 color='#2563eb'><b>{final_score:.1f}%</b></font>", body_style),
            Paragraph(f"<font size=12><b>{semantic_score:.1f}%</b></font>", body_style),
            Paragraph(f"<font size=12><b>{skill_score:.1f}%</b></font>", body_style),
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
    story.append(Spacer(1, 12))

    # 3. Skills Breakdown: Split Verified (1.0x/0.75x) vs Listed-Only (0.4x)
    story.append(Paragraph("Skill Alignment & Evidence Verification", h2_style))
    
    req_skills = screening_result.get("required_skills", [])
    ev_levels = screening_result.get("required_skill_evidence_levels", screening_result.get("skill_evidence_levels", {}))
    
    verified_skills = []
    listed_only_skills = []
    missing_skills = []

    for s in req_skills:
        ev = ev_levels.get(s, {})
        status = str(ev.get("status", "missing")).strip().lower()
        disp = format_skill_display(s)
        if status in {"demonstrated", "substitute"}:
            if status == "substitute":
                sub = format_skill_display(ev.get("substitute_tool", "Eq"))
                verified_skills.append(f"{disp} (Sub: {sub})")
            else:
                verified_skills.append(disp)
        elif status == "listed":
            listed_only_skills.append(disp)
        else:
            missing_skills.append(s)

    v_str = ", ".join(sorted(verified_skills)) if verified_skills else "None verified in project/work context."
    l_str = ", ".join(sorted(listed_only_skills)) if listed_only_skills else "None (no unverified skills detected)."
    
    # Priority sorting of missing skills by JD importance
    sorted_missing = sorted(missing_skills, key=lambda s: JD_CENTRALITY.index(s) if s in JD_CENTRALITY else 99)
    m_str = ", ".join(format_skill_display(s) for s in sorted_missing) if sorted_missing else "No unaddressed skill gaps."

    skills_table_data = [
        [Paragraph("<b>Verified Matches (1.0x / 0.75x):</b>", bold_body), Paragraph(v_str, body_style)],
        [Paragraph("<b>Listed Only (0.4x Partial):</b>", bold_body), Paragraph(l_str, body_style)],
        [Paragraph(f"<b>Unmatched Skill Gaps ({len(sorted_missing)}):</b>", bold_body), Paragraph(m_str, body_style)],
    ]
    t_skills = Table(skills_table_data, colWidths=[170, 370])
    t_skills.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
    ]))
    story.append(t_skills)
    story.append(Spacer(1, 12))

    # 4. Gaps & Candidate Priority Development Areas
    story.append(Paragraph("Priority Areas for Technical Follow-up", h2_style))
    if sorted_missing:
        # Prioritize top 3 gaps by JD importance
        p_areas = [f"• <b>{format_skill_display(s)}</b>: Assess foundational knowledge or practical coursework exposure during screening." for s in sorted_missing[:3]]
        p_text = "<br/>".join(p_areas)
    else:
        p_text = "Candidate meets all required technical competencies for the target job description. Focus interview on architectural and project depth."
    story.append(Paragraph(p_text, body_style))
    story.append(Spacer(1, 12))

    # 5. Career & Role Suitability
    story.append(Paragraph("Role Suitability & Market Transferability", h2_style))
    pathways = career_recommendations or []
    if pathways:
        path_strs = [f"<b>{p['role']}</b> ({p['fit']}% transferability)" for p in pathways[:3]]
        path_text = "<b>Adjacent Career Pathways:</b> " + " | ".join(path_strs)
    else:
        path_text = "<b>Adjacent Career Pathways:</b> Technical competencies align with standard software and analytical profiles."
    story.append(Paragraph(path_text, body_style))
    story.append(Spacer(1, 14))

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