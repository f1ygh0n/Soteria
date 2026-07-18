const fileInput = document.getElementById("fileUpload");
const uploadBox = document.querySelector(".upload-box");
const uploadTitle = uploadBox.querySelector("h3");
const uploadText = uploadBox.querySelector("p");
const form = document.querySelector("form");
const submitButton = document.querySelector(".scan-submit");
const spinner = document.querySelector(".button-spinner");
const scanText = document.querySelector(".scan-text");
const textarea = document.querySelector(".privacy-textarea");
const scanIcon = document.querySelector(".scan-icon");

fileInput.addEventListener("change", () => {

    if (fileInput.files.length === 0) {

        uploadTitle.textContent = "Upload a File";

        uploadText.textContent =
            "Drag & drop a file or click to browse.";

        textarea.disabled = false;

        textarea.placeholder =
            "Paste text, source code, configuration files or documents here...";

        return;

    }

    const file = fileInput.files[0];

    uploadTitle.textContent = file.name;

    uploadText.textContent =
        `${(file.size / 1024).toFixed(1)} KB`;

    textarea.disabled = true;

    textarea.placeholder =
        "File selected. Text input disabled.";

});

uploadBox.addEventListener("dragover", (e) => {

    e.preventDefault();

    uploadBox.classList.add("dragging");

});

uploadBox.addEventListener("dragleave", () => {

    uploadBox.classList.remove("dragging");

});

uploadBox.addEventListener("drop", (e) => {

    e.preventDefault();

    uploadBox.classList.remove("dragging");

    fileInput.files = e.dataTransfer.files;

    fileInput.dispatchEvent(new Event("change"));

});

form.addEventListener("submit", (e) => {

    const hasFile = fileInput.files.length > 0;

    const hasText = textarea.value.trim().length > 0;

    if (!hasFile && !hasText) {

        e.preventDefault();

        alert("Please upload a file or paste some text.");

        return;

    }

    if (hasFile) {

        textarea.value = "";

    }

    submitButton.disabled = true;

    scanIcon.classList.add("hidden");

    spinner.classList.remove("hidden");

    scanText.textContent = "Scanning...";

});