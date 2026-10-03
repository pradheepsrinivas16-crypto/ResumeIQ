from pathlib import Path
import sys


# ============================================================
# PATH SETUP
# ============================================================

SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent

sys.path.append(str(SRC_DIR))


# ============================================================
# IMPORTS
# ============================================================

from resume_parser import extract_resume_text
from skill_matcher import extract_skills


# ============================================================
# CAPABILITY DEFINITIONS
# ============================================================

CAPABILITIES = {

    # --------------------------------------------------------
    # DATA SCIENCE
    # --------------------------------------------------------

    "data science": {

        "description":
            "Ability to work with data using programming, "
            "data analysis, statistics and machine learning.",

        "core_skills": {
            "python",
            "data analysis",
            "machine learning"
        },

        "supporting_skills": {
            "pandas",
            "numpy",
            "scikit-learn",
            "statistical analysis",
            "predictive modeling"
        },

        "minimum_core": 2,
        "minimum_supporting": 1
    },


    # --------------------------------------------------------
    # DATA ANALYTICS
    # --------------------------------------------------------

    "data analytics": {

        "description":
            "Ability to analyze data, identify trends "
            "and communicate insights using analytical "
            "and visualization tools.",

        "core_skills": {
            "data analysis",
            "sql",
            "data visualization"
        },

        "supporting_skills": {
            "excel",
            "power bi",
            "tableau",
            "dashboard",
            "statistical analysis",
            "data cleaning",
            "exploratory data analysis"
        },

        "minimum_core": 2,
        "minimum_supporting": 1
    },


    # --------------------------------------------------------
    # MACHINE LEARNING
    # --------------------------------------------------------

    "machine learning": {

        "description":
            "Ability to develop predictive models using "
            "machine learning algorithms and data.",

        "core_skills": {
            "machine learning",
            "python"
        },

        "supporting_skills": {
            "scikit-learn",
            "pandas",
            "numpy",
            "predictive modeling",
            "data analysis"
        },

        "minimum_core": 2,
        "minimum_supporting": 1
    },


    # --------------------------------------------------------
    # BUSINESS INTELLIGENCE
    # --------------------------------------------------------

    "business intelligence": {

        "description":
            "Ability to transform business data into "
            "dashboards, reports and actionable insights.",

        "core_skills": {
            "power bi",
            "dashboard"
        },

        "supporting_skills": {
            "sql",
            "excel",
            "tableau",
            "data visualization",
            "kpi",
            "data analysis"
        },

        "minimum_core": 1,
        "minimum_supporting": 2
    },


    # --------------------------------------------------------
    # DATA VISUALIZATION
    # --------------------------------------------------------

    "data visualization": {

        "description":
            "Ability to communicate information through "
            "charts, dashboards and visual representations "
            "of data.",

        "core_skills": {
            "data visualization"
        },

        "supporting_skills": {
            "power bi",
            "tableau",
            "matplotlib",
            "seaborn",
            "dashboard",
            "excel"
        },

        "minimum_core": 1,
        "minimum_supporting": 1
    }
}


# ============================================================
# NORMALIZE SKILLS
# ============================================================

def normalize_skills(skills):

    return {
        skill.lower().strip()
        for skill in skills
    }


# ============================================================
# ANALYZE SINGLE CAPABILITY
# ============================================================

def analyze_capability(
    resume_skills,
    capability_name
):

    resume_skills = normalize_skills(
        resume_skills
    )

    capability = CAPABILITIES.get(
        capability_name
    )

    # --------------------------------------------------------
    # Invalid capability
    # --------------------------------------------------------

    if capability is None:

        return {
            "capability": capability_name,
            "supported": False,
            "core_matches": [],
            "supporting_matches": [],
            "missing_core": [],
            "missing_supporting": [],
            "evidence_count": 0
        }

    # --------------------------------------------------------
    # Get capability requirements
    # --------------------------------------------------------

    core_skills = capability[
        "core_skills"
    ]

    supporting_skills = capability[
        "supporting_skills"
    ]

    # --------------------------------------------------------
    # Find matching evidence
    # --------------------------------------------------------

    core_matches = sorted(
        resume_skills.intersection(
            core_skills
        )
    )

    supporting_matches = sorted(
        resume_skills.intersection(
            supporting_skills
        )
    )

    # --------------------------------------------------------
    # Find missing evidence
    # --------------------------------------------------------

    missing_core = sorted(
        core_skills - resume_skills
    )

    missing_supporting = sorted(
        supporting_skills - resume_skills
    )

    # --------------------------------------------------------
    # Check requirements
    # --------------------------------------------------------

    core_requirement_met = (
        len(core_matches)
        >= capability["minimum_core"]
    )

    supporting_requirement_met = (
        len(supporting_matches)
        >= capability["minimum_supporting"]
    )

    # --------------------------------------------------------
    # Final capability status
    # --------------------------------------------------------

    supported = (
        core_requirement_met
        and supporting_requirement_met
    )

    # --------------------------------------------------------
    # Evidence count
    # --------------------------------------------------------

    evidence_count = (
        len(core_matches)
        +
        len(supporting_matches)
    )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {

        "capability":
            capability_name,

        "description":
            capability["description"],

        "supported":
            supported,

        "core_matches":
            core_matches,

        "supporting_matches":
            supporting_matches,

        "missing_core":
            missing_core,

        "missing_supporting":
            missing_supporting,

        "evidence_count":
            evidence_count
    }


# ============================================================
# ANALYZE ALL CAPABILITIES
# ============================================================

def analyze_capabilities(
    resume_skills
):

    results = []

    for capability_name in CAPABILITIES:

        result = analyze_capability(
            resume_skills,
            capability_name
        )

        results.append(
            result
        )

    return results


# ============================================================
# PRINT CAPABILITY REPORT
# ============================================================

def print_capability_report(
    results
):

    print("\n" + "=" * 75)
    print("REAL RESUME CAPABILITY INTELLIGENCE")
    print("=" * 75)

    for result in results:

        print(
            f"\n{result['capability'].upper()}"
        )

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        if result["supported"]:

            print(
                "Status: SUPPORTED"
            )

        else:

            print(
                "Status: INSUFFICIENT EVIDENCE"
            )

        # ----------------------------------------------------
        # Evidence count
        # ----------------------------------------------------

        print(
            f"Evidence Count: "
            f"{result['evidence_count']}"
        )

        # ----------------------------------------------------
        # Core evidence
        # ----------------------------------------------------

        print(
            f"Core Evidence: "
            f"{result['core_matches']}"
        )

        # ----------------------------------------------------
        # Supporting evidence
        # ----------------------------------------------------

        print(
            f"Supporting Evidence: "
            f"{result['supporting_matches']}"
        )

        # ----------------------------------------------------
        # Missing core skills
        # ----------------------------------------------------

        if result["missing_core"]:

            print(
                f"Missing Core: "
                f"{result['missing_core']}"
            )

        # ----------------------------------------------------
        # Missing supporting skills
        # ----------------------------------------------------

        if result["missing_supporting"]:

            print(
                f"Missing Supporting: "
                f"{result['missing_supporting']}"
            )

    print("\n" + "=" * 75)


# ============================================================
# FIND RESUME PDF AUTOMATICALLY
# ============================================================

def find_resume_pdf():

    # Search project root
    pdf_files = list(
        PROJECT_DIR.glob("*.pdf")
    )

    if pdf_files:
        return pdf_files[0]

    # Search one level deeper
    pdf_files = list(
        PROJECT_DIR.glob("*/*.pdf")
    )

    if pdf_files:
        return pdf_files[0]

    return None


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Find resume
    # --------------------------------------------------------

    print("\nSearching for resume PDF...")

    resume_path = find_resume_pdf()

    if resume_path is None:

        print(
            "\nERROR: No PDF resume found."
        )

        print(
            "\nPut your resume PDF inside:"
        )

        print(
            PROJECT_DIR
        )

        print(
            "\nThen run:"
        )

        print(
            "python src/capability_engine.py"
        )

        sys.exit(1)

    print(
        f"\nUsing resume:"
    )

    print(
        f"  {resume_path}"
    )


    # --------------------------------------------------------
    # Extract resume
    # --------------------------------------------------------

    print(
        "\nExtracting resume..."
    )

    try:

        resume_text = extract_resume_text(
            resume_path
        )

    except Exception as e:

        print(
            "\nERROR while extracting resume:"
        )

        print(e)

        sys.exit(1)


    if not resume_text.strip():

        print(
            "\nERROR: Resume text is empty."
        )

        print(
            "The PDF may be scanned/image-based."
        )

        sys.exit(1)


    print(
        "Resume extracted successfully."
    )

    print(
        f"Characters extracted: "
        f"{len(resume_text)}"
    )


    # --------------------------------------------------------
    # Extract skills
    # --------------------------------------------------------

    print(
        "\nExtracting skills..."
    )

    resume_skills = extract_skills(
        resume_text
    )


    # --------------------------------------------------------
    # Display detected skills
    # --------------------------------------------------------

    print(
        "\nDetected Resume Skills:"
    )

    if resume_skills:

        for skill in resume_skills:

            print(
                f"  ✓ {skill}"
            )

    else:

        print(
            "  No skills detected."
        )


    # --------------------------------------------------------
    # Capability analysis
    # --------------------------------------------------------

    print(
        "\nAnalyzing candidate capabilities..."
    )

    results = analyze_capabilities(
        resume_skills
    )


    # --------------------------------------------------------
    # Print detailed report
    # --------------------------------------------------------

    print_capability_report(
        results
    )


    # --------------------------------------------------------
    # Supported capabilities
    # --------------------------------------------------------

    supported = [

        result

        for result in results

        if result["supported"]

    ]


    print(
        "\nSUPPORTED CAPABILITIES"
    )

    if supported:

        for result in supported:

            print(
                f"  ✓ "
                f"{result['capability']}"
            )

    else:

        print(
            "  None"
        )


    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    print(
        "\n" + "=" * 75
    )

    print(
        "REAL RESUME CAPABILITY TEST COMPLETE"
    )

    print(
        "=" * 75
    )