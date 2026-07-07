document.querySelectorAll(".scan-form").forEach(form => {

    form.addEventListener("submit", () => {

        const button = form.querySelector(".scan-submit");

        if (!button)
            return;

        const spinner = button.querySelector(".button-spinner");
        const icon = button.querySelector(".scan-icon");
        const text = button.querySelector(".scan-text");

        spinner.classList.remove("hidden");

        icon.classList.add("hidden");

        text.textContent = "Analyzing...";

        button.disabled = true;

    });

});