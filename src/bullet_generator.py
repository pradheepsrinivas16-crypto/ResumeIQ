"""
Resume Bullet-Point Optimizer (ATS Formatted)
Provides metric-bracketed, honest bullet templates customized by technical domain.
"""

from src.skill_matcher import format_skill_display

BULLET_TEMPLATES = {
    "dashboard": [
        "Designed and published interactive Power BI/Tableau dashboards tracking [KPI / operational metric], reducing reporting turnaround time by [X]%.",
        "Consolidated disparate data sources into a centralized business dashboard, enabling leadership to track [business metric] weekly."
    ],
    "sql": [
        "Authored complex SQL queries utilizing joins, subqueries, and window functions to extract and transform [volume / records] of data for analysis.",
        "Optimized relational database queries and indexed tables, improving data retrieval efficiency by [X]%."
    ],
    "excel": [
        "Built automated Excel reporting workbooks utilizing XLOOKUP, advanced pivot tables, and dynamic charts for [specific project/team].",
        "Cleaned and reconciled messy tabular datasets in Excel using formulas and data validation, eliminating manual entry errors."
    ],
    "python": [
        "Engineered automated Python data extraction scripts to clean, process, and structure raw inputs into analysis-ready formats.",
        "Developed modular Python functions and data pipelines, cutting down repetitive data preparation tasks by [X] hours per week."
    ],
    "pandas": [
        "Leveraged Pandas for large-scale data manipulation, handling missing values and outlier detection across [X] rows of raw records.",
        "Vectorized tabular computations using Pandas DataFrames to preprocess experimental data for reporting."
    ],
    "power bi": [
        "Constructed end-to-end Power BI data models with star-schema architecture, creating custom DAX measures for [KPI/metric].",
        "Developed and maintained executive Power BI reports, delivering automated data refreshes and actionable visual insights."
    ],
    "rest api": [
        "Architected and integrated RESTful API endpoints for asynchronous client-server communication, handling [payload/request type].",
        "Consumed external REST APIs and implemented robust client-side error handling and status code hydration."
    ]
}

DEFAULT_TEMPLATES = [
    "Applied {skill} within academic and project coursework to implement [specific feature or analysis], improving execution efficiency.",
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