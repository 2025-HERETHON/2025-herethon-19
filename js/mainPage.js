// mainPage.js 파일
document.addEventListener("DOMContentLoaded", () => {
  const startButton = document.querySelector(".main-button");

  startButton.addEventListener("click", () => {
    window.location.href = "/logIn/logIn.html";
  });
});

