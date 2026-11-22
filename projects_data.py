"""Single source of truth for the projects shown on the portfolio.

Every project page, card and sitemap entry is generated from this list, so a
change here is reflected everywhere. Only add URLs that really exist.
"""

PROJECTS = [
    {
        "slug": "nutrisnap",
        "image": "img/projects/nutrisnap.webp",
        "image_alt": "Preview of the NutriSnap-X food recognition and nutrition analysis web application",
        "endpoint": "nutrisnap",
        "title": "NutriSnap-X",
        "tagline": "AI-based food recognition and nutrition estimation",
        "kind": "AI web application",
        "badge": "Mini & Major Project",
        "summary": (
            "A web application that identifies food items in an uploaded photo "
            "and estimates their nutritional values."
        ),
        "overview": (
            "NutriSnap-X is a Flask web application that uses a MobileNetV2 "
            "image-recognition model to identify food items in a photo and "
            "present calorie and nutrition estimates."
        ),
        "problem": (
            "Many people do not know the nutritional value of what they eat "
            "every day, which makes healthy eating harder to maintain."
        ),
        "solution": (
            "Upload a photo of a meal and the application recognises the food "
            "and shows nutritional information straight away."
        ),
        "features": [
            "Food recognition from images using MobileNetV2",
            "Calorie and nutritional analysis",
            "Detection of multiple food items in one image",
        ],
        "flow": ["Upload image", "Process image", "Model predicts food", "Calculate nutrition", "Show result"],
        "tech": ["Python", "Flask", "TensorFlow", "OpenCV", "HTML/CSS/JS"],
        "github": "https://github.com/Ala-Ganesh/NutriSnap-X",
        "live": "https://nutrisnap-x.onrender.com/",
    },
    {
        "slug": "smarthire",
        "image": "img/projects/smarthire.webp",
        "image_alt": "Screenshot of the SmartHire AI interactive portfolio homepage, showing the introduction, profile photo and navigation",
        "endpoint": "smarthire",
        "title": "SmartHire AI",
        "tagline": "Interactive portfolio web application for recruiters",
        "kind": "Flask web application",
        "badge": "This website",
        "summary": (
            "An interactive portfolio that lets recruiters explore projects, "
            "view GitHub activity and ask questions through a chat assistant."
        ),
        "overview": (
            "SmartHire AI is the web application behind this portfolio. It "
            "replaces a static resume with a site where recruiters can browse "
            "projects, open the resume and ask a simple chat assistant about "
            "my background."
        ),
        "problem": (
            "A static resume shows what someone has done but makes it hard to "
            "explore projects and get quick answers."
        ),
        "solution": (
            "A single Flask application that brings projects, live demos, a "
            "GitHub overview and a question-and-answer assistant together."
        ),
        "features": [
            "Project showcase with live demo and source links",
            "Rule-based chat assistant answering questions about my profile",
            "GitHub dashboard using the public GitHub API",
            "Resume download and contact form",
        ],
        "flow": ["Visitor", "Web interface", "Flask backend", "Assistant logic", "Response"],
        "tech": ["Python", "Flask", "HTML/CSS/JS", "Render"],
        "github": "https://github.com/Ala-Ganesh/SmartHire-AI",
        "live": "https://alaganesh-portfolio.onrender.com",
    },
    {
        "slug": "billsmart",
        "image": "img/projects/billsmart.webp",
        "image_alt": "Preview of the BillSmartApp bill and expense management web application",
        "endpoint": "billsmart",
        "title": "BillSmartApp",
        "tagline": "Bill and expense management system",
        "kind": "Full-stack web application",
        "badge": "Personal Project",
        "summary": (
            "A web application to track bills and expenses, with user accounts "
            "and spending insights."
        ),
        "overview": (
            "BillSmartApp is a full-stack Flask application that helps users "
            "keep track of bills and expenses, with user authentication and "
            "data stored in SQLite."
        ),
        "problem": (
            "Many people forget to pay bills on time, which leads to penalties "
            "and makes spending hard to follow."
        ),
        "solution": (
            "Users add their bills and due dates, review their spending and "
            "stay on top of payments."
        ),
        "features": [
            "Add and manage bills with due dates",
            "User authentication",
            "Secure data storage with SQLite",
            "Spending insights and financial reporting",
        ],
        "flow": ["User", "Web interface", "Flask backend", "SQLite database", "Reports"],
        "tech": ["Python", "Flask", "SQLite", "HTML/CSS/JS"],
        "github": "https://github.com/Ala-Ganesh/BillSmart",
        "live": "https://billsmartapp.onrender.com",
    },
]

PROJECTS_BY_SLUG = {p["slug"]: p for p in PROJECTS}
