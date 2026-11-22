/* Site-wide behaviour: mobile menu, active section highlight, contact form. */
(function () {
    "use strict";

    document.documentElement.classList.replace("no-js", "js");

    /* ---- Light / dark theme ------------------------------------------ */
    var root = document.documentElement;
    var themeButton = document.querySelector("[data-theme-toggle]");
    var themeMeta = document.querySelector('meta[name="theme-color"]');
    var darkQuery = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

    function storedTheme() {
        try {
            var value = localStorage.getItem("theme");
            return value === "light" || value === "dark" ? value : null;
        } catch (e) {
            return null;
        }
    }

    function applyTheme(theme, animate) {
        if (animate) {
            root.classList.add("theme-transition");
            window.setTimeout(function () { root.classList.remove("theme-transition"); }, 400);
        }
        if (root.getAttribute("data-theme") !== theme) root.setAttribute("data-theme", theme);
        if (themeMeta) themeMeta.setAttribute("content", theme === "dark" ? "#161C19" : "#F8FAF8");
        if (themeButton) {
            themeButton.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
        }
    }

    applyTheme(root.getAttribute("data-theme") === "dark" ? "dark" : "light", false);

    if (themeButton) {
        themeButton.addEventListener("click", function () {
            var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
            applyTheme(next, true);
            try { localStorage.setItem("theme", next); } catch (e) { /* choice just won't be remembered */ }
        });
    }

    /* Follow the system setting live, but only until the visitor picks a theme. */
    if (darkQuery && darkQuery.addEventListener) {
        darkQuery.addEventListener("change", function (event) {
            if (!storedTheme()) applyTheme(event.matches ? "dark" : "light", true);
        });
    }
    /* Keep other open tabs in step with the choice. */
    window.addEventListener("storage", function (event) {
        if (event.key === "theme" && (event.newValue === "light" || event.newValue === "dark")) {
            applyTheme(event.newValue, true);
        }
    });

    /* ---- Mobile navigation ------------------------------------------ */
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("site-nav");

    function setMenu(open) {
        if (!toggle || !nav) return;
        nav.classList.toggle("is-open", open);
        toggle.setAttribute("aria-expanded", String(open));
        toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }

    if (toggle && nav) {
        toggle.addEventListener("click", function () {
            setMenu(toggle.getAttribute("aria-expanded") !== "true");
        });
        nav.addEventListener("click", function (event) {
            if (event.target.closest("a")) setMenu(false);
        });
        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                setMenu(false);
                toggle.focus();
            }
        });
        document.addEventListener("click", function (event) {
            if (!event.target.closest(".nav-bar")) setMenu(false);
        });
        window.matchMedia("(min-width: 1081px)").addEventListener("change", function () {
            setMenu(false);
        });
    }

    /* ---- Active section in the navbar (home page only) -------------- */
    var onHome = document.getElementById("home") !== null;
    if (onHome && "IntersectionObserver" in window) {
        var links = Array.prototype.slice.call(document.querySelectorAll(".site-nav a[data-section]"));
        var byId = {};
        links.forEach(function (link) {
            byId[link.getAttribute("data-section")] = link;
        });

        var setActive = function (id) {
            links.forEach(function (link) {
                if (link.getAttribute("data-section") === id) {
                    link.setAttribute("aria-current", "true");
                } else {
                    link.removeAttribute("aria-current");
                }
            });
        };

        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting && byId[entry.target.id]) setActive(entry.target.id);
                });
            },
            { rootMargin: "-45% 0px -50% 0px", threshold: 0 }
        );

        Object.keys(byId).forEach(function (id) {
            var section = document.getElementById(id);
            if (section) observer.observe(section);
        });
    }

    /* ---- Contact form (progressive enhancement) ---------------------- */
    var forms = document.querySelectorAll("[data-contact-form]");
    Array.prototype.forEach.call(forms, function (form) {
        var status = form.querySelector("[data-form-status]");
        var button = form.querySelector("button[type=submit]");
        var label = form.querySelector("[data-label]");

        function clearErrors() {
            Array.prototype.forEach.call(form.querySelectorAll("[data-error-for]"), function (p) {
                p.textContent = "";
            });
            Array.prototype.forEach.call(form.querySelectorAll("[aria-invalid]"), function (el) {
                el.removeAttribute("aria-invalid");
            });
        }

        function showErrors(errors) {
            var first = null;
            Object.keys(errors || {}).forEach(function (field) {
                var holder = form.querySelector('[data-error-for="' + field + '"]');
                var input = form.elements[field];
                if (holder) holder.textContent = errors[field];
                if (input) {
                    input.setAttribute("aria-invalid", "true");
                    if (!first) first = input;
                }
            });
            if (first) first.focus();
        }

        function showStatus(message, ok) {
            status.textContent = message;
            status.className = "form-status " + (ok ? "is-success" : "is-error");
        }

        form.addEventListener("submit", function (event) {
            event.preventDefault();
            clearErrors();
            status.textContent = "";
            status.className = "form-status";

            button.disabled = true;
            label.textContent = "Sending…";

            fetch(form.action, {
                method: "POST",
                headers: { "X-Requested-With": "fetch", Accept: "application/json" },
                body: new FormData(form),
                credentials: "same-origin"
            })
                .then(function (response) {
                    return response.json().then(function (data) {
                        return { ok: response.ok && data.ok, data: data };
                    });
                })
                .then(function (result) {
                    showStatus(result.data.message, result.ok);
                    if (result.ok) {
                        form.reset();
                    } else {
                        showErrors(result.data.errors);
                    }
                })
                .catch(function () {
                    showStatus("Network error. Please check your connection and try again.", false);
                })
                .finally(function () {
                    button.disabled = false;
                    label.textContent = "Send message";
                });
        });
    });
})();
