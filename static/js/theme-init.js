/* Runs in <head> before the page is painted, so visitors never see a flash of the
   wrong theme. Order of choice: saved choice (localStorage) -> system preference -> light. */
(function () {
    "use strict";
    var theme = null;
    try {
        theme = localStorage.getItem("theme");
    } catch (e) { /* storage blocked: fall back to the system setting */ }
    if (theme !== "light" && theme !== "dark") {
        theme = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }
    document.documentElement.setAttribute("data-theme", theme);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", theme === "dark" ? "#161C19" : "#F8FAF8");
})();
