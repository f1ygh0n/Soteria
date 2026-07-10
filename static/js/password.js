const form = document.querySelector("form");

const submitButton = document.querySelector(".scan-submit");

const spinner = document.querySelector(".button-spinner");

const scanText = document.querySelector(".scan-text");

const scanIcon = document.querySelector(".scan-icon");

const toggle = document.getElementById("togglePassword");

const passwordInput = document.getElementById("passwordInput");

const icon = toggle.querySelector("img");

toggle.addEventListener("click", () => {

    if (passwordInput.type === "password") {

        passwordInput.type = "text";

        icon.src = "/static/images/icons/eye-off.svg";

    }

    else {

        passwordInput.type = "password";

        icon.src = "/static/images/icons/eye.svg";

    }

});

form.addEventListener("submit", () => {

    submitButton.disabled = true;

    spinner.classList.remove("hidden");

    scanIcon.classList.add("hidden");

    scanText.textContent = "Analyzing...";

});