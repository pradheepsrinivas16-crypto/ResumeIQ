"""
Resume Bullet-Point Optimizer (ATS Formatted)
Provides honest, metric-bracketed bullet templates customized for foundational coursework and projects.
"""

from src.skill_matcher import format_skill_display

BULLET_TEMPLATES = {
    "dashboard": [
        "Designed and published an academic Power BI dashboard tracking [specific KPI or metric], organizing raw tabular inputs into visual reports.",
        "Built interactive report views in Power BI/Excel to visualize project trends, presenting findings to stakeholders with clean chart layouts."
    ],
    "sql": [
        "Authored SQL queries utilizing SELECT, WHERE filters, and basic table JOINs to extract structured subsets of data for class projects.",
        "Created relational database tables and executed aggregation queries in MySQL/PostgreSQL to analyze [dataset domain]."
    ],
    "excel": [
        "Organized and analyzed tabular datasets in Microsoft Excel utilizing VLOOKUP/XLOOKUP, pivot tables, and summary charts.",
        "Applied Excel formulas and conditional formatting to clean raw survey/project records, eliminating manual calculation errors."
    ],
    "python": [
        "Developed modular Python scripts to parse, clean, and structure raw data inputs into clean tabular formats.",
        "Implemented data transformation routines in Python using standard libraries to automate recurring project analysis tasks."
    ],
    "pandas": [
        "Loaded and inspected tabular datasets using Pandas DataFrames, handling missing values and basic summary statistics.",
        "Applied Pandas functions (.groupby(), .merge()) to transform and clean multi-table records for exploratory analysis."
    ],
    "power bi": [
        "Built foundational Power BI dashboards connecting to Excel/CSV data sources, implementing bar charts and KPI summary cards.",
        "Modeled basic two-table relationships in Power BI to produce interactive visual reports for coursework presentations."
    ],
    "rest api": [
        "Integrated RESTful API endpoints for client-server communication, implementing error handling and status-code validation (e.g., 200 vs 404).",
        "Consumed external REST APIs and parsed JSON response payloads into frontend component state."
    ]
}

DEFAULT_TEMPLATES = [
    "Applied foundational concepts of {skill} within coursework and project labs to implement [specific feature or analysis].",
    "Practiced {skill} adhering to standard coding conventions and technical guidelines during project assignments."
]

def generate_resume_bullets(skill_name):
    if not skill_name:
        return []
    skill_clean = str(skill_name).strip().lower()
    disp_name = format_skill_display(skill_clean)

    if skill_clean in BULLET_TEMPLATES:
        return BULLET_TEMPLATES[skill_clean]
    
    return [template.format(skill=disp_name) for template in DEFAULT_TEMPLATES]