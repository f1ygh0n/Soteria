const searchInput = document.getElementById("globalSearch");
const dropdown = document.getElementById("searchDropdown");

if (searchInput && dropdown) {

    searchInput.addEventListener("input", () => {

        const query = searchInput.value.trim().toLowerCase();

        dropdown.innerHTML = "";

        if (!query) {

            dropdown.classList.add("hidden");
            return;

        }

        const matches = window.APP_PAGES.filter(page =>

            page.name.toLowerCase().includes(query) ||

            page.keywords.some(keyword =>
                keyword.toLowerCase().includes(query)
            )

        );

        if (matches.length === 0) {

            dropdown.classList.add("hidden");
            return;

        }

        matches.slice(0, 5).forEach(page => {

            const div = document.createElement("div");

            div.className = "search-item";

            div.innerHTML = `
                <h4>${page.name}</h4>
                <p>${page.description}</p>
            `;

            div.addEventListener("click", () => {

                window.location.href = page.url;

            });

            dropdown.appendChild(div);

        });

        dropdown.classList.remove("hidden");

    });

    searchInput.addEventListener("keydown", (event) => {

        if (event.key !== "Enter")
            return;

        event.preventDefault();

        const query = searchInput.value.trim();

        if (!query)
            return;

        window.location.href = `/search?q=${encodeURIComponent(query)}`;

    });

    document.addEventListener("click", (event) => {

        if (!event.target.closest(".search-box")) {

            dropdown.classList.add("hidden");

        }

    });

    searchInput.addEventListener("focus", () => {

        if (dropdown.children.length > 0) {

            dropdown.classList.remove("hidden");

        }

    });

}