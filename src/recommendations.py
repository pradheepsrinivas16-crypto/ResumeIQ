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


def generate_improvement_suggestions(missing_skills):
    """
    Generate resume improvement suggestions
    based on missing job requirements.
    """

    suggestions = []

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
    required_skills
):
    """
    Generate an explanation for the compatibility score.
    """

    explanation = []

    # ------------------------------------------
    # Skill coverage
    # ------------------------------------------

    matched_count = len(matched_skills)
    required_count = len(required_skills)

    if required_count > 0:

        explanation.append(
            f"{matched_count}/{required_count} required skills "
            f"were detected in the resume."
        )

    # ------------------------------------------
    # Skill interpretation
    # ------------------------------------------

    if skill_score >= 90:

        explanation.append(
            "Strong technical skill coverage."
        )

    elif skill_score >= 70:

        explanation.append(
            "Good technical skill coverage with some gaps."
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
    required_skills=None
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
        missing_skills
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
            required_skills
        )

    else:

        result["score_explanation"] = []

    return result