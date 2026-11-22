"""Ala Ganesh - Python Full Stack Developer portfolio (Flask application).

Run locally:      python app.py
Run in production: gunicorn app:app   (see Procfile / render.yaml)

All secrets and settings come from environment variables - see .env.example.
"""

import hmac
import logging
import os
import re
import secrets
import time
from datetime import date

from flask import Flask, Response, jsonify, render_template, request, send_from_directory, session
from werkzeug.middleware.proxy_fix import ProxyFix

try:  # optional: loads a local .env file during development
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv is not required in production
    pass

import mailer
from ai_brain import get_ai_response
from projects_data import PROJECTS, PROJECTS_BY_SLUG

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("portfolio")

app = Flask(__name__)

# Render (and most hosts) sit behind a proxy: trust one hop so the visitor's
# real IP and https scheme are used.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# --------------------------------------------------------------------------
# Configuration (environment variables, never hard-coded secrets)
# --------------------------------------------------------------------------
_secret = os.environ.get("SECRET_KEY", "").strip()
if not _secret:
    # A random key is fine for local development. In production set SECRET_KEY,
    # otherwise visitors' contact-form sessions reset whenever the app restarts.
    _secret = secrets.token_hex(32)
    log.warning("SECRET_KEY is not set - using a temporary random key.")

app.config.update(
    SECRET_KEY=_secret,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    # Secure cookies only when served over https (Render sets RENDER=true).
    SESSION_COOKIE_SECURE=(
        os.environ.get("SESSION_COOKIE_SECURE", "").lower() == "true"
        or bool(os.environ.get("RENDER"))
    ),
    MAX_CONTENT_LENGTH=32 * 1024,  # no uploads; reject large request bodies
    JSON_SORT_KEYS=False,
)

DEV_MODE = os.environ.get("APP_ENV", "production").lower() == "development"
SITE_URL = (os.environ.get("SITE_URL") or "https://alaganesh-portfolio.onrender.com").rstrip("/")

SITE = {
    "name": "Ala Ganesh",
    "role": "Python Full Stack Developer",
    "email": os.environ.get("PUBLIC_CONTACT_EMAIL", "alaganeshnadendla@gmail.com"),
    "github": "https://github.com/Ala-Ganesh",
    "github_user": "Ala-Ganesh",
    "linkedin": os.environ.get("LINKEDIN_URL", "https://www.linkedin.com/in/ala-ganesh"),
    "url": SITE_URL,
}


@app.context_processor
def inject_site():
    return {
        "site": SITE,
        "year": date.today().year,
        "projects": PROJECTS,
        "contact_enabled": mailer.is_configured() or DEV_MODE,
    }


# --------------------------------------------------------------------------
# Security headers
# --------------------------------------------------------------------------
@app.after_request
def add_security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    # SAMEORIGIN (not DENY) so the resume PDF can be shown inside our own /resume page.
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; "
        "img-src 'self' data: https://avatars.githubusercontent.com; "
        "connect-src 'self' https://api.github.com; "
        "base-uri 'self'; form-action 'self'; frame-ancestors 'self'; object-src 'self'",
    )
    if request.path.startswith("/static/"):
        response.headers.setdefault("Cache-Control", "public, max-age=604800")
    return response


# --------------------------------------------------------------------------
# Simple in-memory rate limiter (per visitor IP). Good enough for a single
# small instance; it protects the contact form and the chat endpoint.
# --------------------------------------------------------------------------
_hits: dict[str, list[float]] = {}


def too_many_requests(bucket: str, limit: int, window_seconds: int) -> bool:
    now = time.time()
    key = f"{bucket}:{request.remote_addr}"
    recent = [t for t in _hits.get(key, []) if now - t < window_seconds]
    if len(recent) >= limit:
        _hits[key] = recent
        return True
    recent.append(now)
    _hits[key] = recent
    return False


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html", csrf_token=get_csrf_token())


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return handle_contact()
    return render_template("contact.html", csrf_token=get_csrf_token())


RESUME_FILENAME = "Ala_Ganesh_Python_Full_Stack_Developer_Resume.pdf"


def _send_resume(as_attachment: bool):
    # Same PDF both ways: "inline" is displayed in the page/tab, "attachment" downloads it
    # under a clean, professional file name.
    return send_from_directory(
        app.static_folder, "resume.pdf",
        mimetype="application/pdf", as_attachment=as_attachment, download_name=RESUME_FILENAME,
    )


@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/resume/file")
def resume_file():
    return _send_resume(as_attachment=False)


@app.route("/resume/download")
def resume_download():
    return _send_resume(as_attachment=True)


@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


@app.route("/github")
def github():
    return render_template("github.html")


def _project_page(slug):
    return render_template("project_detail.html", project=PROJECTS_BY_SLUG[slug])


# Keep the original three URLs and endpoint names working.
@app.route("/project/nutrisnap")
def nutrisnap():
    return _project_page("nutrisnap")


@app.route("/project/smarthire")
def smarthire():
    return _project_page("smarthire")


@app.route("/project/billsmart")
def billsmart():
    return _project_page("billsmart")


# --------------------------------------------------------------------------
# Chat assistant API
# --------------------------------------------------------------------------
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)
    message = data.get("message") if isinstance(data, dict) else None
    if not isinstance(message, str) or not message.strip():
        return jsonify({"reply": "Please type a question."}), 400
    if too_many_requests("ask", limit=30, window_seconds=60):
        return jsonify({"reply": "You are sending messages quickly - please wait a moment."}), 429
    return jsonify({"reply": get_ai_response(message[:300])})


# --------------------------------------------------------------------------
# Contact form
# --------------------------------------------------------------------------
EMAIL_PATTERN = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,255}\.[^@\s]{2,}$")


def get_csrf_token() -> str:
    """Create (once per visitor) the token that proves a form came from our page."""
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
        session["csrf_issued"] = time.time()
    return session["csrf"]


def wants_json() -> bool:
    return request.headers.get("X-Requested-With") == "fetch" or request.is_json


def contact_response(ok: bool, message: str, status: int, errors: dict | None = None):
    if wants_json():
        return jsonify({"ok": ok, "message": message, "errors": errors or {}}), status
    return (
        render_template(
            "contact.html",
            csrf_token=get_csrf_token(),
            form_ok=ok,
            form_message=message,
            form_errors=errors or {},
            form_values=request.form if not ok else {},
        ),
        status,
    )


def handle_contact():
    form = request.form

    # 1. CSRF + timing (bots usually submit instantly or without a session).
    token = form.get("csrf_token", "")
    if not token or not hmac.compare_digest(token, session.get("csrf", "")):
        return contact_response(False, "Your session expired. Please reload the page and try again.", 400)
    if time.time() - session.get("csrf_issued", 0) < 3:
        return contact_response(False, "That was very quick - please try again.", 400)

    # 2. Honeypot: real visitors never see or fill this field.
    if form.get("website", "").strip():
        return contact_response(True, "Thank you! Your message has been sent.", 200)

    if too_many_requests("contact", limit=5, window_seconds=900):
        return contact_response(False, "Too many messages. Please try again in a few minutes.", 429)

    # 3. Validation.
    name = " ".join(form.get("name", "").split())
    email = form.get("email", "").strip()
    message = form.get("message", "").replace("\r\n", "\n").strip()
    errors = {}
    if not 2 <= len(name) <= 80:
        errors["name"] = "Please enter your name (2-80 characters)."
    if not EMAIL_PATTERN.match(email) or len(email) > 254:
        errors["email"] = "Please enter a valid email address."
    if not 10 <= len(message) <= 2000:
        errors["message"] = "Please write a message between 10 and 2000 characters."
    if errors:
        return contact_response(False, "Please fix the highlighted fields.", 422, errors)

    # 4. Deliver.
    if mailer.is_configured():
        if mailer.send_contact_email(name, email, message):
            return contact_response(True, "Thank you! Your message has been sent.", 200)
        return contact_response(
            False,
            f"Sorry, the message could not be sent. Please email me directly at {SITE['email']}.",
            502,
        )

    if DEV_MODE:
        log.info("DEV MODE - contact message from %s <%s> (%d characters)", name, email, len(message))
        return contact_response(True, "Development mode: message received (email is not configured).", 200)

    return contact_response(
        False,
        f"The contact form is not available right now. Please email me at {SITE['email']}.",
        503,
    )


# --------------------------------------------------------------------------
# SEO helpers and health check
# --------------------------------------------------------------------------
@app.route("/robots.txt")
def robots():
    body = f"User-agent: *\nAllow: /\nDisallow: /ask\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    return Response(body, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    paths = ["/", "/projects", "/resume", "/contact", "/chatbot", "/github"] + [
        f"/project/{p['slug']}" for p in PROJECTS
    ]
    urls = "".join(f"<url><loc>{SITE_URL}{path}</loc></url>" for path in paths)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>"
    )
    return Response(xml, mimetype="application/xml")


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"})


# --------------------------------------------------------------------------
# Error pages
# --------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html", code=404, title="Page not found",
                           message="The page you are looking for does not exist."), 404


@app.errorhandler(413)
def too_large(_error):
    return render_template("error.html", code=413, title="Request too large",
                           message="That request was too large."), 413


@app.errorhandler(500)
def server_error(_error):
    return render_template("error.html", code=500, title="Something went wrong",
                           message="An unexpected error occurred. Please try again."), 500


if __name__ == "__main__":
    # Local development only. Production uses gunicorn (see Procfile).
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
    )
