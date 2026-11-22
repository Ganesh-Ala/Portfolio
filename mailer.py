"""Sending contact-form messages by email.

Two delivery methods are supported, chosen by environment variables:

1. Resend HTTPS API   -> RESEND_API_KEY + CONTACT_TO_EMAIL (+ CONTACT_FROM_EMAIL)
2. Classic SMTP       -> SMTP_HOST + SMTP_PORT + SMTP_USER + SMTP_PASSWORD + CONTACT_TO_EMAIL

Render's free web services block outbound SMTP ports, so on the free plan use
the HTTPS API (option 1). No secrets are stored in the code.
"""

import json
import logging
import os
import smtplib
import urllib.error
import urllib.request
from email.message import EmailMessage

log = logging.getLogger(__name__)


def _env(name: str) -> str:
    return (os.environ.get(name) or "").strip()


def method() -> str | None:
    """Return 'resend', 'smtp' or None when email is not configured."""
    if not _env("CONTACT_TO_EMAIL"):
        return None
    if _env("RESEND_API_KEY"):
        return "resend"
    if _env("SMTP_HOST") and _env("SMTP_USER") and _env("SMTP_PASSWORD"):
        return "smtp"
    return None


def is_configured() -> bool:
    return method() is not None


def _clean_header(value: str) -> str:
    """Remove line breaks so user input can never inject email headers."""
    return " ".join(value.replace("\r", " ").replace("\n", " ").split())


def send_contact_email(name: str, email: str, message: str) -> bool:
    """Send the message. Returns True on success, False on any failure."""
    chosen = method()
    if chosen is None:
        return False

    to_address = _env("CONTACT_TO_EMAIL")
    subject = f"Portfolio message from {_clean_header(name)[:60]}"
    body = f"Name: {_clean_header(name)}\nEmail: {_clean_header(email)}\n\n{message}"

    try:
        if chosen == "resend":
            payload = {
                "from": _env("CONTACT_FROM_EMAIL") or "Portfolio <onboarding@resend.dev>",
                "to": [to_address],
                "subject": subject,
                "text": body,
                "reply_to": _clean_header(email),
            }
            request = urllib.request.Request(
                "https://api.resend.com/emails",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {_env('RESEND_API_KEY')}",
                    "Content-Type": "application/json",
                    # An explicit User-Agent avoids being rejected by the API's firewall.
                    "User-Agent": "ala-ganesh-portfolio/1.0",
                },
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=10) as response:
                return 200 <= response.status < 300

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = _env("SMTP_USER")
        msg["To"] = to_address
        msg["Reply-To"] = _clean_header(email)
        msg.set_content(body)
        port = int(_env("SMTP_PORT") or 587)
        with smtplib.SMTP(_env("SMTP_HOST"), port, timeout=10) as server:
            server.starttls()
            server.login(_env("SMTP_USER"), _env("SMTP_PASSWORD"))
            server.send_message(msg)
        return True

    except (urllib.error.URLError, smtplib.SMTPException, OSError, ValueError) as error:
        # Log the type only: never log keys, passwords or message contents.
        log.error("Contact email failed (%s)", type(error).__name__)
        return False
