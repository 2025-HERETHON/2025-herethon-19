console.log("✅ JS 파일 연결됨");

document.addEventListener("DOMContentLoaded", () => {
  console.log("🎯 DOM 로드 완료됨");

  /* ===== 요소 찾기 ===== */
  const loginBtn = document.querySelector(".login-button");
  const signupBtn = document.querySelector(".signup-button");
  const findBtn = document.querySelector(".find-password");

  /* 찾기 실패 시 콘솔 경고 */
  if (!loginBtn || !signupBtn || !findBtn) {
    console.warn("❌ 버튼 요소를 찾지 못했습니다.");
    return;
  }
  console.log("🔘 로그인 버튼:", loginBtn);

  // 회원가입 버튼 요소
  const signupButton = document.querySelector(".signup-button");
  const findButton = document.querySelector(".find-password");

  // 로그인 버튼 클릭 이벤트 등록
  loginBtn.addEventListener("click", async (event) => {
    event.preventDefault();
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

      // ✅ 원래는 바로 .json() 했지만 지금은 text로 받아서 구조 확인
      const text = await response.text();
      console.log("서버 응답 원본(text):", text);

      // 🔽 여기를 안전하게 JSON 파싱하도록 변경!
      let data;
      try {
        data = JSON.parse(text);
      } catch (parseError) {
        console.error("❌ JSON 파싱 실패:", parseError);
        alert("서버 응답이 올바른 JSON 형식이 아닙니다.");
        return;  // 여기서 종료
      }

      // 요청이 성공한 경우
      if (response.ok) {
        alert("로그인 성공!");
        // ★ 토큰 저장
        localStorage.setItem("accessToken", data.access);
        localStorage.setItem("refreshToken", data.refresh);

        // ★ 페이지 이동 (setTimeout 제거, 상대 경로 사용)
        console.log("✅ 이동 시작");
        window.location.href = "/communityUI/communityMain.html";
        //  ↑ 5500 포트 기준으로 이미 확인된 경로
      } else {
        alert("로그인 실패: " + (data.detail || "아이디/비밀번호를 확인하세요"));
      }
    } catch (error) {
      // 네트워크 오류 또는 서버 문제
      console.error("🔥 에러 발생!", error);
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

