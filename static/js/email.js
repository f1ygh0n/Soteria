const pasteButton = document.getElementById("pasteButton");
const uploadButton = document.getElementById("uploadButton");
const uploadInput = document.getElementById("emlUpload");
const textarea = document.getElementById("emailInput");

const gmailButton = document.getElementById("gmailButton");
const gmailButtonText = document.getElementById("gmailButtonText");

const gmailModal = document.getElementById("gmailModal");
const gmailList = document.getElementById("gmailList");
const closeModal = document.getElementById("closeModal");

function getRelativeTime(dateString) {

    const now = new Date();
    const then = new Date(dateString);

    const seconds = Math.floor((now - then) / 1000);

    if (seconds < 60)
        return "Just now";

    const minutes = Math.floor(seconds / 60);

    if (minutes < 60)
        return `${minutes}m ago`;

    const hours = Math.floor(minutes / 60);

    if (hours < 24)
        return `${hours}h ago`;

    const days = Math.floor(hours / 24);

    if (days === 1)
        return "Yesterday";

    if (days < 7)
        return `${days} days ago`;

    return then.toLocaleDateString();

}

if (pasteButton && textarea) {

    pasteButton.addEventListener("click", async () => {

        try {

            const text = await navigator.clipboard.readText();

            textarea.value = text;

            textarea.focus();

        }

        catch {

            alert("Clipboard access was denied.");

        }

    });

}

if (uploadButton && uploadInput && textarea) {

    uploadButton.addEventListener("click", () => {

        uploadInput.click();

    });

    uploadInput.addEventListener("change", async () => {

        const file = uploadInput.files[0];

        if (!file) return;

        const formData = new FormData();

        formData.append("email_file", file);

        try {

            const response = await fetch("/parse-eml", {

                method: "POST",

                body: formData

            });

            const data = await response.json();

            if (data.success) {

                textarea.value = data.email_text;

            }

            else {

                alert(data.message);

            }

        }

        catch (err) {

            console.error(err);

            alert("Failed to upload the file.");

        }

    });

}

if (gmailButton) {

    gmailButton.addEventListener("click", async () => {

        if (gmailButtonText.innerText.trim() === "Connect Gmail") {

            window.location.href = "/gmail/login";

            return;

        }

        gmailButton.disabled = true;
        gmailButtonText.innerText = "Loading...";

        gmailModal.classList.remove("hidden");

        gmailList.innerHTML = `

            <div class="gmail-loading">

                <div class="loader"></div>

                <p>Loading your inbox...</p>

            </div>

        `;

        try {

            const response = await fetch("/gmail/list");

            const emails = await response.json();

            gmailList.innerHTML = "";

            emails.forEach(email => {

                const div = document.createElement("div");

                div.className = "gmail-item";

                div.innerHTML = `

                    <div class="gmail-item-left">

                        <h3>${email.subject || "(No Subject)"}</h3>

                        <p>${email.from}</p>

                    </div>

                    <div class="gmail-time">

                        ${getRelativeTime(email.date)}

                    </div>

                `;

                div.addEventListener("click", async () => {

                    gmailList.innerHTML = `

                        <div class="gmail-loading">

                            <div class="loader"></div>

                            <p>Loading email...</p>

                        </div>

                    `;

                    try {

                        const response = await fetch(`/gmail/email/${email.id}`);

                        const data = await response.json();

                        console.log(data);

                        textarea.value =
                            `From: ${data.from}
                            To: ${data.to}
                            Reply-To: ${data.reply_to}
                            Return-Path: ${data.return_path}
                            Subject: ${data.subject}
                            Date: ${data.date}

                            ${data.body}`;

                        gmailModal.classList.add("hidden");

                    }

                    catch (err) {

                        console.error(err);

                        alert("Failed to load email.");

                        gmailModal.classList.add("hidden");

                    }

                });

                gmailList.appendChild(div);

            });

        }

        catch (err) {

            console.error(err);

            gmailModal.classList.add("hidden");

            alert("Failed to load Gmail.");

        }

        finally {

            gmailButton.disabled = false;
            gmailButtonText.innerText = "Choose From Gmail";

        }

    });

}

if (closeModal) {

    closeModal.addEventListener("click", () => {

        gmailModal.classList.add("hidden");

    });

}

window.addEventListener("click", (event) => {

    if (event.target === gmailModal) {

        gmailModal.classList.add("hidden");

    }

});

gmailSearch.addEventListener("input", () => {

    const value = gmailSearch.value.toLowerCase();

    document.querySelectorAll(".gmail-item").forEach(item => {

        item.style.display =
            item.innerText.toLowerCase().includes(value)
                ? "block"
                : "none";

    });

});
