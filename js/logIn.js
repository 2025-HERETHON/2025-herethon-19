document.addEventListener("DOMContentLoaded", () => {
  // 로그인 버튼
  const loginButton = document.querySelector(".login-button");
   // 회원가입 버튼 요소
  const signupButton = document.querySelector(".signup-button");
  const findButton = document.querySelector(".find-password");

  // 로그인 버튼 클릭 이벤트 등록
  loginButton.addEventListener("click", async () => {
    // 입력된 이메일/비밀번호 값 가져오기
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
      // 백엔드 로그인 API 요청 보내기
      const response = await fetch("http://127.0.0.1:8000/api/accounts/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })  // 요청 본문
      });

      // 응답 JSON 파싱
      const data = await response.json();

      // 요청이 성공한 경우
      if (response.ok) {
        alert("로그인 성공!");
        console.log("받은 토큰:", data);

        // 토큰 localStorage에 저장
        localStorage.setItem("accessToken", data.access);
        localStorage.setItem("refreshToken", data.refresh);

        // 로그인 후 이동
        console.log("페이지 이동 시도 중...");
        window.location.href = "/community/communityMain.html";

      } else {
        // 요청은 보냈지만 인증 실패한 경우
        alert("로그인 실패: " + (data.detail || "아이디/비밀번호를 확인하세요"));
      }
    } catch (error) {
      // 네트워크 오류 또는 서버 문제
      alert("에러 발생: " + error.message);
    }
  });

  signupButton.addEventListener("click", () => {
    window.location.href = "/join/joinMain.html";
  });

    // 비밀번호 찾기 버튼 클릭 시 find.html로 이동
  findButton.addEventListener("click", () => {
    window.location.href = "/password/find.html"; 
  });

});

