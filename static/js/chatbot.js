/* Chat assistant page. Messages are inserted with textContent, never innerHTML,
   so nothing typed by a visitor can inject HTML into the page. */
(function () {
    "use strict";

    var log = document.getElementById("chat-log");
    var form = document.getElementById("chat-form");
    var input = document.getElementById("chat-input");
    if (!log || !form || !input) return;

    var avatarSrc = log.querySelector(".chat-avatar").getAttribute("src");
    var busy = false;

    function addMessage(text, sender) {
        var wrapper = document.createElement("div");
        wrapper.className = "chat-msg " + (sender === "user" ? "is-user" : "is-bot");

        if (sender !== "user") {
            var avatar = document.createElement("img");
            avatar.className = "chat-avatar";
            avatar.src = avatarSrc;
            avatar.alt = "";
            avatar.width = 32;
            avatar.height = 32;
            wrapper.appendChild(avatar);
        }

        var bubble = document.createElement("p");
        bubble.className = "chat-bubble";
        bubble.textContent = text;
        wrapper.appendChild(bubble);

        log.appendChild(wrapper);
        log.scrollTop = log.scrollHeight;
        return wrapper;
    }

    function ask(question) {
        var text = question.trim();
        if (!text || busy) return;
        busy = true;

        addMessage(text, "user");
        var typing = addMessage("Typing…", "bot");

        fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        })
            .then(function (response) {
                return response.json().catch(function () { return {}; });
            })
            .then(function (data) {
                typing.remove();
                addMessage(data.reply || "Sorry, something went wrong. Please try again.", "bot");
            })
            .catch(function () {
                typing.remove();
                addMessage("Sorry, I could not reach the server. Please try again.", "bot");
            })
            .finally(function () {
                busy = false;
            });
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        var value = input.value;
        input.value = "";
        ask(value);
    });

    Array.prototype.forEach.call(document.querySelectorAll("[data-question]"), function (button) {
        button.addEventListener("click", function () {
            ask(button.getAttribute("data-question"));
        });
    });
})();
