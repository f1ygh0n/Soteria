const form = document.querySelector("form");

const fileInput = document.getElementById("imageUpload");

const uploadBox = document.querySelector(".upload-box");

const uploadTitle = uploadBox.querySelector("h3");

const uploadText = uploadBox.querySelector("p");

const uploadTypes = uploadBox.querySelector("span");

const previewContainer = document.querySelector(".image-preview");

const previewImage = previewContainer
    ? previewContainer.querySelector("img")
    : null;

const submitButton = document.querySelector(".scan-submit");

const spinner = document.querySelector(".button-spinner");

const scanIcon = document.querySelector(".scan-icon");

const scanText = document.querySelector(".scan-text");


function updatePreview(file) {

    if (!file)
        return;

    uploadTitle.textContent = "Image Selected";

    uploadText.textContent = file.name;

    uploadTypes.textContent = "Click Analyze to begin";

    const reader = new FileReader();

    reader.onload = function (event) {

        if (previewImage) {

            previewImage.src = event.target.result;

        }

    };

    reader.readAsDataURL(file);

}


fileInput.addEventListener("change", () => {

    if (fileInput.files.length) {

        updatePreview(fileInput.files[0]);

    }

});


uploadBox.addEventListener("dragover", (event) => {

    event.preventDefault();

    uploadBox.classList.add("dragover");

});


uploadBox.addEventListener("dragleave", () => {

    uploadBox.classList.remove("dragover");

});


uploadBox.addEventListener("drop", (event) => {

    event.preventDefault();

    uploadBox.classList.remove("dragover");

    if (event.dataTransfer.files.length) {

        fileInput.files = event.dataTransfer.files;

        updatePreview(event.dataTransfer.files[0]);

    }

});


form.addEventListener("submit", () => {

    submitButton.disabled = true;

    spinner.classList.remove("hidden");

    scanIcon.classList.add("hidden");

    scanText.textContent = "Analyzing...";

});