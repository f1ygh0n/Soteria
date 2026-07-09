const pasteButton = document.getElementById("pasteButton");
const uploadButton = document.getElementById("uploadButton");

const uploadInput = document.getElementById("chatUpload");

const textarea = document.getElementById("chatInput");

const ocrOverlay = document.getElementById("ocrOverlay");

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

        if (!file)
            return;

        const formData = new FormData();

        formData.append("chat_image", file);

        if (ocrOverlay)
            ocrOverlay.classList.remove("hidden");

        try {

            const response = await fetch("/parse-chat-image", {

                method: "POST",

                body: formData

            });

            if (!response.ok) {

                console.error(await response.text());

                throw new Error("Server error.");

            }

            const data = await response.json();

            if (data.success) {

                textarea.value = data.chat_text;

                textarea.focus();

            }

            else {

                alert(data.message);

            }

        }

        catch (err) {

            console.error(err);

            alert("Failed to process the screenshot.");

        }

        finally {

            if (ocrOverlay)
                ocrOverlay.classList.add("hidden");

            uploadInput.value = "";

        }

    });

}