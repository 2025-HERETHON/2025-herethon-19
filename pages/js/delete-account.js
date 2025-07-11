const checkbox = document.getElementById("withdraw-confirm");
const button = document.getElementById("withdraw-btn");

checkbox.addEventListener("change", function () {
  button.disabled = !this.checked;
});
