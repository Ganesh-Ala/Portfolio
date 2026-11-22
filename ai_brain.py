"""A small rule-based assistant that answers questions about Ala Ganesh.

It is intentionally simple: it matches keywords in the visitor's question and
returns a prepared answer. It does not call any external AI service, so it
needs no API key and works offline.
"""

import re

# Each rule is (set_of_keywords, answer). Rules are checked in order, so more
# specific topics (individual projects) come before general ones.
_RULES = [
    (
        {"hi", "hello", "hey", "hii"},
        "Hello! I can answer questions about Ala's skills, projects, education, "
        "experience and career goals. What would you like to know?",
    ),
    (
        {"nutrisnap", "nutri", "food", "nutrition"},
        "NutriSnap-X is a Flask web app that identifies food items in a photo "
        "using a MobileNetV2 model and estimates calories and nutritional values. "
        "It can detect multiple foods in one image. Built with Python, Flask, "
        "TensorFlow and OpenCV.",
    ),
    (
        {"billsmart", "bill", "bills", "expense", "expenses"},
        "BillSmartApp is a full-stack Flask application for tracking bills and "
        "expenses. It includes user authentication, SQLite storage and spending "
        "insights.",
    ),
    (
        {"smarthire", "portfolio", "website"},
        "SmartHire AI is the Flask application behind this portfolio. It includes "
        "a project showcase, a GitHub dashboard, resume page, a contact form "
        "and this rule-based assistant.",
    ),
    (
        {"project", "projects", "built", "build", "made"},
        "Ala has built three main projects: NutriSnap-X (AI food recognition), "
        "SmartHire AI (this interactive portfolio) and BillSmartApp (bill and "
        "expense management). Ask about any of them for details.",
    ),
    (
        {"skill", "skills", "technology", "technologies", "stack", "tools", "python", "flask", "fastapi", "django", "sql", "mysql"},
        "Ala works with Python, HTML, CSS, JavaScript, MySQL/SQL, Flask and "
        "FastAPI, plus Git and GitHub. He is currently learning Django as part of "
        "his Python Full Stack Development training.",
    ),
    (
        {"education", "study", "studied", "college", "degree", "university", "btech", "graduate", "graduated"},
        "Ala holds a B.Tech in Computer Science Engineering with a specialization "
        "in Data Science (2022-2026).",
    ),
    (
        {"experience", "internship", "intern", "job", "work", "worked"},
        "Ala completed a remote Data Science internship at CODTECH IT Solutions "
        "(August-September 2025), working on data preprocessing, exploratory "
        "analysis, visualisation and machine learning workflows in Python. He has "
        "also worked part-time alongside his studies, which built his teamwork, "
        "responsibility and communication skills.",
    ),
    (
        {"career", "goal", "goals", "role", "roles", "looking", "hire", "hiring", "opportunity", "opportunities"},
        "Ala is looking for entry-level roles as a Python Developer, Python Full "
        "Stack Developer or Junior Software Developer.",
    ),
    (
        {"family", "background", "home", "from"},
        "Ala comes from a farming family in Andhra Pradesh and is the first "
        "graduate in his family.",
    ),
    (
        {"contact", "email", "reach", "linkedin", "github", "resume", "cv"},
        "You can reach Ala through the Contact section of this site, on LinkedIn "
        "or GitHub, and view or download his resume on the Resume page.",
    ),
    (
        {"who", "about", "yourself", "ala", "ganesh"},
        "Ala Ganesh is a Computer Science graduate (Data Science specialization) "
        "focused on becoming a Python Full Stack Developer. He builds practical "
        "web applications with Python, Flask, FastAPI, MySQL and modern web "
        "technologies.",
    ),
]

_DEFAULT = (
    "I can answer questions about Ala's skills, projects, education, experience "
    "and career goals. Try one of the suggestions above."
)


def get_ai_response(message: str) -> str:
    """Return the prepared answer that best matches the visitor's message."""
    words = set(re.findall(r"[a-z0-9+#.]+", (message or "").lower()))
    for keywords, answer in _RULES:
        if words & keywords:
            return answer
    return _DEFAULT
