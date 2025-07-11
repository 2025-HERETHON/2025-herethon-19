document.addEventListener("DOMContentLoaded", () => {
  const mentoCard = document.querySelector(".mento-card");
  const menteeCard = document.querySelector(".mentee-card");

  // 멘토 선택 시
  mentoCard.addEventListener("click", () => {
    localStorage.setItem("user_type", "mentor"); // 멘토로 저장
    window.location.href = "/join/joinStep1.html"; // 회원 정보 입력 페이지로 이동
  });

  // 멘티 선택 시
  menteeCard.addEventListener("click", () => {
    localStorage.setItem("user_type", "mentee"); // 멘티로 저장
    window.location.href = "/join/joinStep1.html"; // 회원 정보 입력 페이지로 이동
  });
});
