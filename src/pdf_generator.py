import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_candidate_pdf(candidate_name, result, career_recs=None):
    """Generate a clean, professional 1-page PDF candidate evaluation brief."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4,
        fontName='Helvetica-Bold'
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=14,
        fontName='Helvetica'
    )
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1e40af'),
        spaceBefore=10,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155'),
        fontName='Helvetica'
    )

    # 1. Header
    story.append(Paragraph("ResumeIQ • Candidate Intelligence Brief", title_style))
    story.append(Paragraph(f"Candidate Evaluation Report: <b>{candidate_name}</b>", subtitle_style))
    story.append(Spacer(1, 4))

    # 2. Executive Metrics Summary Table
    final_score = float(result.get("final_score", 0))
    semantic_score = float(result.get("semantic_score", 0))
    skill_score = float(result.get("skill_score", 0)) if result.get("skill_score_available", True) else "N/A"
    matched_count = len(result.get("matched_skills", []))
    missing_count = len(result.get("missing_skills", []))

    metrics_data = [
        ["Overall Fit", "Semantic Match", "Skill Coverage", "Matched Skills", "Skill Gaps"],
        [f"{final_score:.1f}%", f"{semantic_score:.1f}%", f"{skill_score if isinstance(skill_score, str) else f'{skill_score:.1f}%'}", str(matched_count), str(missing_count)]
    ]

    metric_table = Table(metrics_data, colWidths=[108, 108, 108, 108, 108])
    metric_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#475569')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 13),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#0f172a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(metric_table)
    story.append(Spacer(1, 10))

    # 3. Verified Skills vs Gaps
    story.append(Paragraph("Skill Alignment Breakdown", section_heading))
    matched_str = ", ".join(result.get("matched_skills", [])) or "None verified"
    missing_str = ", ".join(result.get("missing_skills", [])) or "No detected gaps"

    skills_data = [
        [Paragraph("<b>Verified Matches:</b>", body_style), Paragraph(matched_str, body_style)],
        [Paragraph("<b>Identified Gaps:</b>", body_style), Paragraph(missing_str, body_style)]
    ]
    skills_table = Table(skills_data, colWidths=[120, 420])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 6))

    # 4. Alternative Career Pathways
    if career_recs:
        story.append(Paragraph("Cross-Functional Career Recommendations", section_heading))
        recs_rows = [["Adjacent Role", "Transferable Fit", "Core Overlapping Competencies"]]
        for rec in career_recs:
            recs_rows.append([
                rec['role'],
                f"{rec['fit']}%",
                ", ".join(rec['skills']).title()
            ])
        recs_table = Table(recs_rows, colWidths=[150, 90, 300])
        recs_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(recs_table)
        story.append(Spacer(1, 6))

    # 5. Strategic Recommendations
    story.append(Paragraph("Candidate Development & Next Steps", section_heading))
    missing_skills = result.get("missing_skills", [])
    if missing_skills:
        for idx, skill in enumerate(missing_skills[:3], 1):
            story.append(Paragraph(f"• <b>Priority Area {idx} ({skill.title()}):</b> Candidate should provide verifiable project, certification, or repository links demonstrating production application of {skill}.", body_style))
    else:
        story.append(Paragraph("• Candidate satisfies all key required capabilities detected in the benchmark description.", body_style))

    # 6. Compliance / Audit Footer
    story.append(Spacer(1, 14))
    footer_text = "Generated by ResumeIQ Decision-Support Platform. AI models provide evidence matching and classification; not intended as an automated hiring decision."
    story.append(Paragraph(f"<i><font size='7' color='#94a3b8'>{footer_text}</font></i>", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()