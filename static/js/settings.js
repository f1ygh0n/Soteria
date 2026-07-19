const modal = document.getElementById("historyModal");

const open = document.getElementById("openDeleteModal");

const cancel = document.getElementById("cancelDelete");

const confirmBtn = document.getElementById("confirmDelete");

const form = document.getElementById("historyForm");

open.onclick = () => {

    modal.classList.remove("hidden");

};

cancel.onclick = () => {

    modal.classList.add("hidden");

};

confirmBtn.onclick = () => {

    form.submit();

};