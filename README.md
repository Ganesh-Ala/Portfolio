# Ala Ganesh – Python Full Stack Developer Portfolio

A calm, simple portfolio built with **Flask**. It has light and dark modes, a responsive homepage, project pages, an online resume viewer, a GitHub overview, a simple chat assistant and a secure contact form.

## Technologies
Python · Flask · Gunicorn · HTML · CSS · JavaScript (no frameworks, no CDN) · Resend / SMTP for email

## Project structure
```
app.py             Flask app: routes, security headers, contact form logic
ai_brain.py        Rule-based chat assistant (no external AI service)
mailer.py          Sends contact messages by email (Resend or SMTP)
projects_data.py   The ONE place where project information lives
templates/         HTML pages (base.html + pages + _macros.html)
static/            css/style.css, js/ (main.js, theme-init.js...), img/, fonts/, resume.pdf, favicons
static/img/projects/  project screenshots shown on the homepage cards
requirements.txt   Python dependencies (pinned)
Procfile           Start command (gunicorn app:app)
render.yaml        Optional Render Blueprint
.env.example       List of environment variables (copy to .env)
docs/              Change summary, testing report, your to-do list
```

## Run on your computer (beginner steps)
1. Install Python 3.11 or newer.
2. Open the project folder in VS Code, then open a terminal.
3. Create a virtual environment:
   - Windows: `python -m venv .venv` then `.venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy the settings file: `copy .env.example .env` (Windows) or `cp .env.example .env`
6. Start the site: `python app.py`
7. Open http://127.0.0.1:5000

With `APP_ENV=development` (set in `.env.example`) the contact form works without email setup; messages are only logged.

## Environment variables
| Name | Needed? | Purpose |
|---|---|---|
| `SECRET_KEY` | Yes on Render | Long random text. Render can generate it (render.yaml does). |
| `SITE_URL` | Recommended | Your public URL, used in the sitemap and social previews. |
| `CONTACT_TO_EMAIL` | For contact form | Inbox that receives messages. |
| `RESEND_API_KEY` | For contact form | Free key from resend.com (works on Render free plan). |
| `CONTACT_FROM_EMAIL` | Optional | Sender address verified in Resend. |
| `SMTP_HOST/PORT/USER/PASSWORD` | Alternative | SMTP instead of Resend (blocked on Render free plan). |
| `LINKEDIN_URL`, `PUBLIC_CONTACT_EMAIL` | Optional | Override the links shown on the site. |
| `APP_ENV` | Local only | `development` locally; leave unset on Render. |

If email is **not** configured in production, the contact section shows an "Email me" button instead of a form that cannot work.

## Deploy on Render
1. Push this folder to a GitHub repository (`.env` is ignored by `.gitignore`).
2. On render.com choose **New + → Web Service** and connect the repository (or use **New + → Blueprint** to read `render.yaml`).
3. Settings: Runtime **Python 3**, Build command `pip install -r requirements.txt`, Start command `gunicorn app:app --workers 1 --threads 4 --timeout 60`, Health check path `/healthz`.
4. Add environment variables: `SECRET_KEY`, `SITE_URL`, and for the form `CONTACT_TO_EMAIL`, `RESEND_API_KEY` (optionally `CONTACT_FROM_EMAIL`).
5. Deploy, then open your URL and test the pages and the contact form.

Note: free Render services sleep after inactivity, so the first visit can take about 30 seconds.

## Light / dark mode
The sun/moon button in the navbar switches themes. The choice is saved in the browser (localStorage); on a first visit the visitor's system setting is used. `static/js/theme-init.js` runs before the page paints so there is no flash of the wrong theme. Colours for both themes are CSS variables at the top of `static/css/style.css`.

## Resume page
`/resume` shows `static/resume.pdf` inside the site, with a **Download Resume** button (saved as `Ala_Ganesh_Python_Full_Stack_Developer_Resume.pdf`). To update your resume, replace `static/resume.pdf` with the new file (keep the same name).

## Project screenshots
Cards use `static/img/projects/nutrisnap.webp`, `smarthire.webp` and `billsmart.webp` (1200 x 750 px, 16:10).
- `smarthire.webp` is a real capture of this site.
- `nutrisnap.webp` and `billsmart.webp` are labelled **SAMPLE IMAGE** placeholders. Replace them with real screenshots of your deployed apps (same file names, same size) and they appear automatically. See `docs/YOUR_TO_DO.md`.

## Important notes
- Debug mode is off unless you set `FLASK_DEBUG=1` (never do this on Render).
- Never commit `.env` or API keys.
- To change a project, edit `projects_data.py`; the cards, detail pages and sitemap update automatically.
- `/github` loads public data from the GitHub API in the visitor's browser; GitHub limits unauthenticated requests, so it can occasionally show a fallback message.
