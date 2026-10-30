"""
Resume Bullet-Point Optimizer (ATS Formatted)
Provides metric-bracketed, honest bullet templates customized by technical domain.
"""

from src.skill_matcher import format_skill_display

BULLET_TEMPLATES = {
    "dashboard": [
        "Designed and published interactive Power BI/Tableau dashboards tracking [KPI / operational metric], reducing manual reporting turnaround by [X]%, if measurable.",
        "Consolidated disparate business datasets into a centralized dashboard, enabling stakeholders to monitor [business metric] on a regular cadence."
    ],
    "sql": [
        "Authored optimized SQL queries utilizing joins, aggregations, and window functions to extract and transform [volume / records] for analysis.",
        "Structured relational database queries to clean and aggregate multi-source records, accelerating data extraction time by [X]%."
    ],
    "excel": [
        "Built dynamic Excel reporting workbooks utilizing XLOOKUP, advanced pivot tables, and data models for [specific project or team].",
        "Cleaned and reconciled tabular datasets in Excel using logical formulas and conditional formatting, eliminating manual entry errors."
    ],
    "python": [
        "Developed modular Python scripts to clean, process, and structure raw tabular datasets into analysis-ready formats.",
        "Automated repetitive data extraction and preprocessing workflows using Python, saving approximately [X] hours per project milestone."
    ],
    "pandas": [
        "Leveraged Pandas for large-scale data manipulation, handling missing records and categorical encoding across [X] rows of data.",
        "Vectorized tabular computations using Pandas DataFrames to preprocess experimental data for downstream reporting."
    ],
    "numpy": [
        "Utilized NumPy arrays and mathematical vector operations to accelerate scientific and statistical data calculations.",
        "Implemented numerical data transformations and array slicing in Python to prepare structured inputs for analysis."
    ],
    "power bi": [
        "Constructed end-to-end Power BI data models with star-schema architecture, creating custom DAX measures for [KPI / metric].",
        "Developed and maintained executive Power BI reports, delivering automated data refreshes and actionable visual insights."
    ],
    "rest api": [
        "Architected and integrated RESTful API endpoints for asynchronous client-server communication, handling [payload / request type].",
        "Consumed external REST APIs and implemented client-side error handling, state hydration, and HTTP status-code handling."
    ],
    "statistical analysis": [
        "Conducted descriptive and inferential statistical analysis to evaluate data distributions, variance, and feature correlations.",
        "Applied hypothesis testing and statistical modeling techniques to validate business assumptions across [dataset name]."
    ]
}

DEFAULT_TEMPLATES = [
    "Applied {skill} within academic and project coursework to implement [specific feature or analysis], improving workflow execution.",
    "Integrated {skill} into project workflows adhering to industry standards and modern technical best practices."
]

def generate_resume_bullets(skill_name):
    if not skill_name:
        return []
    skill_clean = str(skill_name).strip().lower()
    disp_name = format_skill_display(skill_clean)

    if skill_clean in BULLET_TEMPLATES:
        return BULLET_TEMPLATES[skill_clean]
    
    return [template.format(skill=disp_name) for template in DEFAULT_TEMPLATES]