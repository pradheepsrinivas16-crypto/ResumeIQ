def generate_resume_bullets(skill_name):
    """
    Generates industry-proven, action-oriented resume bullet points 
    structured around the XYZ formula: Accomplished [X] as measured by [Y], by doing [Z].
    """
    skill = str(skill_name).strip().lower()
    
    templates = {
        "git": [
            "Managed version control across multi-developer repositories using Git, enforcing clean branching strategies and reducing merge conflicts by 30%.",
            "Coordinated pull requests, code reviews, and release tags using Git workflows, ensuring reliable version tracking across production deployments."
        ],
        "github": [
            "Automated testing and build verification pipelines using GitHub Actions, speeding up continuous integration cycles by 25%.",
            "Maintained open-source and internal repositories on GitHub with thorough documentation, issue tracking, and collaborative branch management."
        ],
        "rest api": [
            "Architected and consumed RESTful APIs with asynchronous client handling, reducing page load latency by 35%.",
            "Integrated secure JSON REST APIs into frontend components, ensuring strict data validation, error handling, and responsive state updates."
        ],
        "typescript": [
            "Refactored mission-critical JavaScript components into TypeScript, cutting runtime type-errors by 40% and improving code maintainability.",
            "Designed strongly-typed interfaces and state models using TypeScript, standardizing data contracts across frontend views."
        ],
        "adobe xd": [
            "Translated Adobe XD wireframes and interactive prototypes into pixel-perfect, responsive web interfaces with semantic HTML and modern CSS.",
            "Collaborated with UI/UX designers to audit component designs in Adobe XD, streamlining the developer handoff process."
        ],
        "seo": [
            "Implemented technical SEO best practices, optimizing Core Web Vitals, metadata, and asset loading to boost organic search visibility by 25%.",
            "Conducted frontend audits to structure semantic HTML tags and OpenGraph protocols, driving search engine crawl efficiency."
        ],
        "tableau": [
            "Built interactive executive Tableau dashboards tracking operational KPIs, empowering leadership with real-time analytics across 50,000+ records.",
            "Engineered automated data extraction pipelines connecting SQL warehouses to Tableau, saving 6+ hours of weekly manual reporting."
        ],
        "docker": [
            "Containerized multi-service applications using Docker, guaranteeing zero environment discrepancies between local testing and production.",
            "Authored multi-stage Dockerfiles to minimize container image sizes by 45%, accelerating deployment pipelines."
        ]
    }

    # Default fallback template for any skill
    default_bullets = [
        f"Leveraged {skill.title()} to engineer scalable solutions, adhering to industry best practices and improving feature delivery turnaround by 20%.",
        f"Integrated {skill.title()} into project workflows, designing robust implementations and collaborating closely with cross-functional stakeholders."
    ]

    return templates.get(skill, default_bullets)