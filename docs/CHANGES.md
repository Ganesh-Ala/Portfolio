# Changes in version 3 (navbar only)

Only the navigation bar was changed. Everything from version 2 (dark mode, resume page, screenshots, timeline, availability badge) is untouched.

- `templates/base.html`: navbar now has, in order: Home, About, Technologies, Skills, Projects, My Journey, Resume, Contact, then the existing light/dark toggle at the right end. Section links point to `#id` on the homepage and to `url_for('home') + #id` from every other page (so `/resume` -> About goes to `/#about`). Resume links to the Resume page. The existing `aria-current` logic is kept (Projects pages mark Projects, Contact page marks Contact, Resume page marks Resume).
- `static/css/style.css`: slightly tighter link spacing and no-wrap so eight links stay on one line; the navbar collapses into the existing menu button below **1080px** (it was 880px: eight links need the room, at 881px the page scrolled sideways by 19px); the open mobile menu scrolls inside the screen on short displays (e.g. phone in landscape).
- `static/js/main.js`: the existing menu-reset breakpoint changed from 881px to 1081px to match. The scroll-highlighting already handled any `data-section` link, so Home, About, Technologies, Skills and My Journey highlight as you scroll with no other change.
- Not touched: `theme-init.js`, the toggle button and icons, dark-mode variables, section IDs, routes, Python files.

---

# Changes in this update (version 2)

Only the six requested changes were made. Routes, backend logic, chatbot, contact form, SEO, project data and Render files are unchanged except where listed.

## 1. Light / Dark mode
- Sun/moon toggle button in the navbar (44px touch target, works on mobile; label updates for screen readers).
- Dark palette: soft charcoal-green background `#161C19`, off-white text `#E6ECE8`; no pure black or pure white. All colours are CSS variables (`:root[data-theme="dark"]` in `static/css/style.css`), so navbar, hero, cards, projects, skills, technologies, timeline, forms, buttons, chips, error/success messages and footer all switch.
- Single-colour logos (GitHub, Flask, Django) are lightened in dark mode so they stay visible.
- Subtle 0.3s colour fade, only while the button is pressed.
- New `static/js/theme-init.js` (loaded in `<head>`) applies the theme before first paint: saved choice, else system preference, else light. Choice saved in localStorage; works if storage is blocked. Browser `theme-color` meta also follows the theme.
- Files: `base.html`, `style.css`, `main.js`, `theme-init.js`.

## 2. Navbar order
Projects -> Resume -> Contact, with the existing logo/home link. Theme toggle sits at the right of the navbar. Footer also links to Resume.

## 3. Project screenshots
- Each homepage/projects card now shows a 16:10 image (`static/img/projects/*.webp`, 1200x750), lazy-loaded, with descriptive alt text. Data lives in `projects_data.py` (`image`, `image_alt`).
- `smarthire.webp`: real screenshot of this site's homepage.
- `nutrisnap.webp`, `billsmart.webp`: clearly labelled **SAMPLE IMAGE** placeholders (see YOUR_TO_DO.md).
- Existing descriptions, technologies, GitHub and live-demo links unchanged.

## 4. Resume page
- New `/resume` page (`templates/resume.html`) embeds the PDF with `<object>`, plus **Download Resume** and **Open in new tab** buttons, and a fallback with the same options if the browser cannot show PDFs in the page.
- New routes: `/resume` (page), `/resume/file` (inline PDF), `/resume/download` (attachment named `Ala_Ganesh_Python_Full_Stack_Developer_Resume.pdf`). Nothing downloads automatically.
- Uses the same `static/resume.pdf` you supplied (byte-identical, content untouched).
- Security header `X-Frame-Options` changed from DENY to SAMEORIGIN and CSP allows same-origin embedding so the viewer works; external sites still cannot frame your site.
- `/resume` added to `sitemap.xml`; the homepage hero button now reads "View Resume" and opens this page; chatbot answer about the resume updated.

## 5. Available for opportunities
Small pill with a green dot above the hero heading, next to the graduate label. Readable in both themes.

## 6. Education timeline
Replaced with exactly: 2019-2020 10th Standard (CBSE), Chilakaluripet, Guntur, Andhra Pradesh; 2020-2022 Intermediate - MPC, Guntur, Andhra Pradesh; 2022-2026 B.Tech, Chennai, Tamil Nadu, CSE - Data Science Specialization. Chronological, responsive, themed. (The previous internship/projects timeline entries were replaced as requested; the internship remains on your resume.)

## Other
- Project repo URLs set to the ones that appear in your original project files (NutriSnap-X, SmartHire-AI, BillSmart) - please verify.
- README updated (themes, resume, screenshots).
