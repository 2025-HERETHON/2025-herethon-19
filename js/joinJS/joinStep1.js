document.addEventListener("DOMContentLoaded", () => {
  const nextButton = document.querySelector(".next-button");

  nextButton.addEventListener("click", () => {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const nickname = document.getElementById("nickname").value.trim();
    const phone = document.querySelector(".phone-field").value.trim();
    const userType = localStorage.getItem("user_type"); // 이미 저장돼 있음

    if (!email || !password || !confirmPassword || !nickname || !phone) {
      alert("모든 정보를 입력해주세요.");
      return;
    }

    if (password !== confirmPassword) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }

    if (!userType) {
      alert("회원 유형 정보가 없습니다. 처음으로 돌아갑니다.");
      window.location.href = "/join/joinMain.html";
      return;
    }

    // 저장
    localStorage.setItem("join_email", email);
    localStorage.setItem("join_password", password);
    localStorage.setItem("join_password2", confirmPassword);
    localStorage.setItem("join_nickname", nickname);
    localStorage.setItem("join_phone", phone);

   // 5. 다음 페이지로 분기
    if (userType === "mentor") {
      window.location.href = "/join/joinStep2Mento.html";
    } else if (userType === "mentee") {
      window.location.href = "/join/joinStep2Mentee.html";
    } else {
      alert("알 수 없는 회원 유형입니다.");
      window.location.href = "/join/joinMain.html";
    }
  });
});
