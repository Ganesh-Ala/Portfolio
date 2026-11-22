# Testing report (version 3 - navbar)

Run in a Linux cloud workspace with Flask 3.1.3, gunicorn and headless Chromium (Playwright). Everything below was actually run.

| Requirement | Test | Result |
|---|---|---|
| Exact link order, toggle at the right end | Read the links in the DOM and their positions at 1280px | pass |
| Every link works on the homepage | Clicked each of Home, About, Technologies, Skills, Projects, My Journey, Contact: URL gets the right `#id`, section lands under the sticky bar, link shows as current | 14/14 pass |
| Resume opens the dedicated page | Clicked Resume: `/resume` loads with the embedded PDF, Resume marked current | pass |
| Section links from other pages | Checked all 7 section hrefs on 9 pages (`/resume`, `/projects`, `/contact`, `/github`, `/chatbot`, three project pages, `/nope`) are `/#id`; actually clicked all 7 from `/resume`, a project page, `/contact` and the 404 page and confirmed each landed on `/#id` at the right section | pass |
| Contact navigation | Contact link from home and from other pages; `/contact` marks Contact current | pass |
| Mobile menu | 375x800, 320x568, 667x375 (landscape): hamburger and theme toggle visible, all 8 links listed, tapping closes the menu and goes to the section, works from `/resume`, Escape closes, menu scrolls when taller than the screen, no horizontal overflow | pass |
| Light/Dark mode | Toggle on desktop and mobile; stays dark after navigating via the navbar (About, Resume, Contact, Projects); saved in localStorage; switching back persists. The earlier 67 theme/contrast checks (no flash, system preference, blocked storage) rerun | pass |
| No broken links | Every navbar target returns 200 | pass |
| Keyboard / accessibility | Tab order: skip link, logo, the 8 links, theme toggle; focus ring visible | pass |
| Nothing else broken | Re-ran all earlier suites: 43 route checks, 16 contact checks, 52 version-2 checks, 25 browser regression, 20 interaction checks; overflow/console/broken-image sweep of 10 pages x 9 widths in light and dark; no server errors | all pass |

Notes:
- The navbar test's console check counted the browser's "404" message from visiting the deliberate `/nope` page; I confirmed no real page has any failed request or script error.
- Overflow sweep: the only flagged page is `/github` (its avatar comes from GitHub, which my workspace cannot reach).
- Not verified: real phones, Safari, Firefox; live deployment (you do this). Items from versions 1 and 2 (live project links, real email, real screenshots for NutriSnap-X and BillSmartApp) are unchanged and still need your action - see YOUR_TO_DO.md.

---

# Testing report (version 2)

Environment: Linux cloud workspace, Flask 3.1.3, gunicorn, headless Chromium via Playwright. Everything below was actually run.

| Area | What was tested | Result |
|---|---|---|
| Routes and content | All routes, 404 page, security headers, one H1, tech order/rows, static files, anchors, chat API, nav order and toggle on every page, timeline text, screenshot alt text, project links, resume page/inline/download headers, PDF byte-identical, sitemap | 43/43 + 52/52 pass |
| Contact form | CSRF, honeypot, timing, rate limit, validation, mocked email send, injection, no-JS fallback | 16/16 pass |
| Theme | First visit follows system (dark and light), no flash before paint, no storage write on visit, toggle in navbar, label update, saved in localStorage, survives refresh, persists across 5 pages, saved choice beats system, live system change followed until user chooses, works with storage blocked, not pure black/white | 32/32 pass |
| Contrast | 35 text/background pairs (light and dark) all at least 4.5:1 (lowest 5.5:1 light) | pass |
| Browser regression | Chat, contact validation/success, skip link, 404, detail pages, card links, no JS errors, in light AND dark; screenshots load and keep 16:10 on mobile | 25/25 pass |
| Navigation/mobile | Hamburger, menu open/close, Escape, smooth scroll, active state, desktop nav, resume download, inner-page links | 20/20 pass |
| Mobile toggle | 375px touch device: toggle visible, 44x44, tap switches theme, persists on reload | pass |
| Layout | 10 pages x 9 widths (320-1440px) x 2 themes: horizontal overflow, broken local images, JS errors, tiny text | 162/180 clean; the 18 flagged are all `/github` (avatar from GitHub unreachable here) |
| Resume viewer | Headless Chrome displays PDF in the page, no fallback needed | pass |
| Server | Runs under gunicorn from a fresh extraction of the ZIP; no errors in server log | pass |

During testing I found and fixed three flaws in my own test scripts (not in the site): a chat check counting avatar images, a form check submitting inside the 3-second anti-bot window, and tests still pointing at removed nav links. A rate-limit "failure" was the limiter working as designed.

## NOT verified
- Real phones, Safari and Firefox. The embedded PDF is known to be unreliable on many phone browsers; that is why the page has a View/Download fallback. Please test on your phone.
- NutriSnap-X and BillSmartApp live sites and all GitHub repo links (blocked from my workspace). No real screenshots of those two could be taken.
- Real email delivery (mock only) and the `/github` page with live data.
- Render deployment (you do this).
