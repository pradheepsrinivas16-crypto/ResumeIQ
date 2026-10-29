import re

CURATED_BULLETS = {
    "rest api": [
        "Architected and consumed RESTful APIs with asynchronous client handling, reducing page load latency by 35%.",
        "Integrated secure JSON REST APIs into frontend components, ensuring strict data validation, error handling, and responsive state updates."
    ],
    "react": [
        "Built responsive, accessible web interfaces using React functional components, Hooks (useEffect, useMemo), and modern state management.",
        "Refactored legacy UI components into reusable React component hierarchies, improving codebase maintainability and team velocity by 25%."
    ],
    "git": [
        "Managed version control across multi-developer repositories using Git, enforcing clean branching strategies and reducing merge conflicts by 30%.",
        "Coordinated pull requests, code reviews, and release tags using Git workflows, ensuring reliable version tracking across production deployments."
    ],
    "figma": [
        "Designed high-fidelity interactive wireframes and design systems in Figma, translating complex user workflows into intuitive experiences.",
        "Created scalable component libraries and responsive prototypes in Figma, conducting usability reviews with frontend developers."
    ],
    "adobe xd": [
        "Developed interactive UI/UX wireframes and click-through prototypes in Adobe XD, facilitating seamless design-to-development handoffs.",
        "Standardized visual style guides, typography systems, and responsive layout grids utilizing Adobe XD prototype workflows."
    ],
    "ui/ux": [
        "Conducted end-to-end user experience research and created low-to-high fidelity wireframes to streamline user conversion funnels.",
        "Collaborated with product teams to translate wireframes into intuitive user experiences adhering to WCAG accessibility standards."
    ],
    "responsive web design": [
        "Designed and implemented responsive web layouts using modern CSS Flexbox and Grid, achieving seamless cross-browser and mobile parity.",
        "Optimized mobile-first layouts and touch targets, reducing mobile bounce rate by 20% across varying viewport sizes."
    ],
    "statistical analysis": [
        "Conducted rigorous statistical hypothesis testing, A/B experiment evaluation, and regression modeling to validate feature impact.",
        "Applied statistical analysis techniques across large-scale datasets, uncovering underlying correlation patterns and variance distributions."
    ],
    "kpi": [
        "Defined, tracked, and synthesized core business KPI metrics into automated executive reporting pipelines, cutting manual reporting time by 40%.",
        "Formulated data-driven KPI dashboards monitoring retention and engagement, enabling leadership to make proactive strategic decisions."
    ],
    "sql": [
        "Constructed complex SQL queries incorporating window functions, recursive CTEs, and multi-table joins to extract multi-million row datasets.",
        "Optimized relational database queries and indexed foreign keys, reducing analytics extraction execution time by 45%."
    ],
    "python": [
        "Automated end-to-end data processing pipelines using Python, integrating Pandas and NumPy for efficient tabular data transformation.",
        "Engineered modular Python scripts with comprehensive unit testing and structured logging to ingest and clean raw data streams."
    ],
    "power bi": [
        "Engineered interactive, multi-page Power BI dashboards utilizing advanced DAX measures and dimensional star-schema data models.",
        "Automated scheduled data refreshes and row-level security policies in Power BI service, delivering real-time operational reporting."
    ],
    "excel": [
        "Developed dynamic financial and operational models in Excel using advanced lookup formulas, Power Query transformations, and Pivot tables.",
        "Automated repetitive reporting workflows via Excel macros and structured data cleansing formulas, saving 5+ hours weekly."
    ]
}

def generate_resume_bullets(skill_name):
    if not skill_name:
        return []

    norm_skill = str(skill_name).strip().lower()
    
    # Check direct match
    if norm_skill in CURATED_BULLETS:
        return CURATED_BULLETS[norm_skill]

    # Check alias matches
    for key, bullets in CURATED_BULLETS.items():
        if key in norm_skill or norm_skill in key:
            return bullets

    # Context-aware fallback based on skill domain
    formatted_name = str(skill_name).strip().title()
    
    if any(tech in norm_skill for tech in ["design", "ui", "ux", "wireframe", "prototype"]):
        return [
            f"Designed and prototyped user-centric workflows utilizing {formatted_name}, collaborating closely with developers to ensure pixel-perfect delivery.",
            f"Integrated {formatted_name} into design iteration cycles, conducting stakeholder reviews and improving user experience consistency."
        ]
    elif any(tech in norm_skill for tech in ["data", "analytics", "analysis", "model", "query"]):
        return [
            f"Utilized {formatted_name} to extract, transform, and analyze multi-source datasets, delivering actionable findings to stakeholders.",
            f"Implemented structured data pipelines and analytics solutions leveraging {formatted_name}, improving reporting reliability."
        ]
    else:
        return [
            f"Integrated {formatted_name} into project architecture, adhering to engineering best practices and reducing feature turnaround time by 20%.",
            f"Engineered robust solutions utilizing {formatted_name}, collaborating with cross-functional team members to maintain high code quality."
        ]