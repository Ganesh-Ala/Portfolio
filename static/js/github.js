/* GitHub activity page: reads public data from the GitHub API.
   All API values are inserted with textContent (never innerHTML). */
(function () {
    "use strict";

    var profileBox = document.getElementById("gh-profile");
    var repoBox = document.getElementById("gh-repos");
    if (!profileBox || !repoBox) return;

    var username = profileBox.getAttribute("data-user");
    var api = "https://api.github.com/users/" + encodeURIComponent(username);

    function el(tag, className, text) {
        var node = document.createElement(tag);
        if (className) node.className = className;
        if (text !== undefined) node.textContent = text;
        return node;
    }

    function showError(box, message) {
        box.replaceChildren(el("p", "muted", message));
    }

    function request(url) {
        return fetch(url, { headers: { Accept: "application/vnd.github+json" } }).then(function (response) {
            if (!response.ok) throw new Error("GitHub API " + response.status);
            return response.json();
        });
    }

    request(api)
        .then(function (user) {
            var avatar = el("img");
            avatar.src = user.avatar_url;
            avatar.alt = "GitHub avatar of " + (user.name || username);
            avatar.width = 88;
            avatar.height = 88;

            var info = el("div");
            info.appendChild(el("h2", "", user.name || username));
            if (user.bio) info.appendChild(el("p", "", user.bio));

            var stats = el("p", "gh-stats");
            stats.appendChild(el("span", "", user.public_repos + " public repositories"));
            stats.appendChild(el("span", "", user.followers + " followers"));
            info.appendChild(stats);

            profileBox.replaceChildren(avatar, info);
        })
        .catch(function () {
            showError(profileBox, "GitHub data could not be loaded right now. Please use the profile link below.");
        });

    request(api + "/repos?sort=updated&per_page=12&type=owner")
        .then(function (repos) {
            var shown = repos.filter(function (repo) { return !repo.fork; }).slice(0, 6);
            if (!shown.length) {
                showError(repoBox, "No public repositories to show yet.");
                return;
            }
            var cards = shown.map(function (repo) {
                var card = el("article", "gh-card");
                card.appendChild(el("h3", "", repo.name));
                card.appendChild(el("p", "", repo.description || "No description provided."));

                var link = el("a", "text-link", "View repository");
                link.href = repo.html_url;
                link.target = "_blank";
                link.rel = "noopener noreferrer";
                card.appendChild(link);
                return card;
            });
            repoBox.replaceChildren.apply(repoBox, cards);
        })
        .catch(function () {
            showError(repoBox, "Repositories could not be loaded right now.");
        });
})();
