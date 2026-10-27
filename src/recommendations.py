# ==========================================
# RESUME RECOMMENDATIONS
# ==========================================


def generate_strengths(matched_skills):
    """
    Generate candidate strengths from matched skills.
    """

    strengths = []

    if not matched_skills:
        return strengths

    # Overall strength
    strengths.append(
        f"Demonstrates strong coverage of "
        f"{len(matched_skills)} required job skills."
    )

    # Individual skills
    for skill in matched_skills:
        strengths.append(
            f"Demonstrates experience with {skill}."
        )

    return strengths


def generate_skill_gaps(missing_skills):
    """
    Identify skills that are missing from the resume.
    """

    return missing_skills


def generate_improvement_suggestions(
    missing_skills,
    skill_evidence_levels=None,
    matched_skills=None
):
    """
    Generate resume improvement suggestions
    based on missing job requirements and evidence quality.

    When there are no missing skills, suggest upgrading
    Listed Only skills to Demonstrated evidence.
    """

    suggestions = []
    skill_evidence_levels = skill_evidence_levels or {}
    matched_skills = matched_skills or []

    if missing_skills:

        suggestions.append(
            f"Consider strengthening the resume by adding "
            f"relevant experience, projects, or certifications "
            f"related to {len(missing_skills)} missing skill(s), "
            f"if applicable."
        )

        for skill in missing_skills:

            suggestions.append(
                f"Consider adding relevant {skill} "
                f"experience, projects, or certifications "
                f"if applicable."
            )

    else:

        suggestions.append(
            "The resume covers all detected required skills."
        )

        # Find skills that are only Listed (not Demonstrated/Supporting)
        # and suggest upgrading them.
        listed_only_skills = []
        for skill in matched_skills:
            ev = None
            # Try direct lookup and case-insensitive fallback
            ev = skill_evidence_levels.get(skill)
            if ev is None:
                for k, v in skill_evidence_levels.items():
                    if str(k).strip().lower() == str(skill).strip().lower():
                        ev = v
                        break

            if ev is not None:
                status = str(ev.get("status", "")).strip().lower()
                if status in ("listed", "listed_only"):
                    listed_only_skills.append(skill)

        if listed_only_skills:
            suggestions.append(
                f"You matched all required skills, but "
                f"{len(listed_only_skills)} skill(s) appear only "
                f"in your Skills section without demonstrated evidence. "
                f"Upgrading these to Demonstrated (e.g., add a project or "
                f"work-experience bullet) would strengthen your profile:"
            )
            for skill in listed_only_skills:
                suggestions.append(
                    f"Upgrade '{skill}' from Listed Only to Demonstrated: "
                    f"add a project, coursework, or work-experience bullet "
                    f"that explicitly uses {skill}."
                )
        else:
            suggestions.append(
                "Consider strengthening the evidence for these skills "
                "with measurable project results, achievements, or "
                "work experience where applicable."
            )

    return suggestions


def generate_score_explanation(
    semantic_score,
    skill_score,
    matched_skills,
    required_skills,
    missing_skills=None,
    skill_evidence_levels=None
):
    """
    Generate an explanation for the compatibility score,
    including evidence-weight breakdown.
    """

    explanation = []
    missing_skills = missing_skills or []
    skill_evidence_levels = skill_evidence_levels or {}

    # ------------------------------------------
    # Skill coverage count
    # ------------------------------------------

    matched_count = len(matched_skills)
    required_count = len(required_skills)
    missing_count = len(missing_skills)

    if required_count > 0:

        explanation.append(
            f"{matched_count}/{required_count} required skills "
            f"were detected in the resume."
        )

    # ------------------------------------------
    # Evidence-weight breakdown
    # Explain WHY skill_score != 100% even when all matched
    # ------------------------------------------

    if required_count > 0 and skill_evidence_levels:
        evidence_weights = {
            "demonstrated": 1.00,
            "supporting": 0.70,
            "listed": 0.40,
            "listed_only": 0.40,
            "missing": 0.00,
        }

        demonstrated_skills = []
        supporting_skills_list = []
        listed_only_skills = []

        for skill in required_skills:
            ev = skill_evidence_levels.get(skill)
            if ev is None:
                for k, v in skill_evidence_levels.items():
                    if str(k).strip().lower() == str(skill).strip().lower():
                        ev = v
                        break
            if ev is None:
                continue
            status = str(ev.get("status", "missing")).strip().lower()
            if status == "demonstrated":
                demonstrated_skills.append(skill)
            elif status == "supporting":
                supporting_skills_list.append(skill)
            elif status in ("listed", "listed_only"):
                listed_only_skills.append(skill)

        if demonstrated_skills or supporting_skills_list or listed_only_skills:
            breakdown_parts = []
            if demonstrated_skills:
                breakdown_parts.append(
                    f"{len(demonstrated_skills)} Demonstrated (weight 1.0)"
                )
            if supporting_skills_list:
                breakdown_parts.append(
                    f"{len(supporting_skills_list)} Supporting (weight 0.7)"
                )
            if listed_only_skills:
                breakdown_parts.append(
                    f"{len(listed_only_skills)} Listed Only (weight 0.4)"
                )
            if breakdown_parts:
                explanation.append(
                    "Evidence quality breakdown: "
                    + ", ".join(breakdown_parts)
                    + ". Listed Only skills receive partial credit (0.4×) "
                    "because they appear only in the Skills section without "
                    "demonstrated project or work evidence."
                )

    # ------------------------------------------
    # Skill interpretation — never say "some gaps" when gaps = 0
    # ------------------------------------------

    if missing_count == 0 and required_count > 0:
        if skill_score >= 90:
            explanation.append(
                "Strong technical skill coverage with no gaps detected."
            )
        elif skill_score >= 70:
            explanation.append(
                "Good technical skill coverage. All required skills matched, "
                "but some are Listed Only (partial credit). "
                "Add project/experience evidence to reach full weight."
            )
        elif skill_score >= 40:
            explanation.append(
                "Moderate skill coverage score. All required skills were "
                "detected, but most appear as Listed Only (0.4× weight). "
                "Demonstrating them in projects or work experience "
                "would significantly improve this score."
            )
        else:
            explanation.append(
                "Low skill coverage score despite all skills being matched. "
                "Skills appear only in the Skills section (Listed Only). "
                "Add concrete project or work experience bullets."
            )
    else:
        if skill_score >= 90:
            explanation.append(
                "Strong technical skill coverage."
            )
        elif skill_score >= 70:
            explanation.append(
                "Good technical skill coverage."
            )
        elif skill_score >= 40:
            explanation.append(
                "Moderate technical skill coverage."
            )
        else:
            explanation.append(
                "Limited technical skill coverage."
            )

    # ------------------------------------------
    # Semantic interpretation
    # ------------------------------------------

    if semantic_score >= 80:

        explanation.append(
            "Strong semantic alignment between the resume "
            "and job description."
        )

    elif semantic_score >= 60:

        explanation.append(
            "Moderate semantic alignment between the resume "
            "and job description."
        )

    elif semantic_score >= 40:

        explanation.append(
            "Limited semantic alignment between the resume "
            "and job description."
        )

    else:

        explanation.append(
            "Low semantic alignment between the resume "
            "and job description."
        )

    # ------------------------------------------
    # Overall interpretation
    # ------------------------------------------

    if skill_score >= 80 and semantic_score >= 80:

        explanation.append(
            "Overall: Strong alignment across both skills "
            "and resume-job context."
        )

    elif skill_score >= 80 and semantic_score < 80:

        explanation.append(
            "Overall: Strong skill coverage with moderate "
            "semantic alignment."
        )

    elif skill_score < 80 and semantic_score >= 80:

        if missing_count == 0:
            explanation.append(
                "Overall: Strong semantic alignment. All required skills "
                "matched, but evidence quality could be improved "
                "(some skills are Listed Only)."
            )
        else:
            explanation.append(
                "Overall: Strong semantic alignment, but some "
                "required skills are missing."
            )

    else:

        explanation.append(
            "Overall: The resume has partial alignment with "
            "the job requirements."
        )

    return explanation


def generate_recommendations(
    matched_skills,
    missing_skills,
    semantic_score=None,
    skill_score=None,
    required_skills=None,
    skill_evidence_levels=None
):
    """
    Generate complete recommendation report.

    The additional parameters are optional so existing
    code remains compatible.
    """

    strengths = generate_strengths(
        matched_skills
    )

    skill_gaps = generate_skill_gaps(
        missing_skills
    )

    suggestions = generate_improvement_suggestions(
        missing_skills,
        skill_evidence_levels=skill_evidence_levels,
        matched_skills=matched_skills
    )

    result = {
        "strengths": strengths,
        "skill_gaps": skill_gaps,
        "suggestions": suggestions
    }

    # Generate score explanation when score information
    # is available.
    if (
        semantic_score is not None
        and skill_score is not None
        and required_skills is not None
    ):

        result["score_explanation"] = generate_score_explanation(
            semantic_score,
            skill_score,
            matched_skills,
            required_skills,
            missing_skills=missing_skills,
            skill_evidence_levels=skill_evidence_levels
        )

    else:

        result["score_explanation"] = []

    return result