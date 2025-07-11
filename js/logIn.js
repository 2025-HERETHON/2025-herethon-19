document.addEventListener("DOMContentLoaded", () => {
  // 로그인 버튼
  const loginButton = document.querySelector(".login-button");
   // 회원가입 버튼 요소
  const signupButton = document.querySelector(".signup-button");
  const findButton = document.querySelector(".find-password");



      // 요청이 성공한 경우
      if (response.ok) {
        alert("로그인 성공!");


        // 토큰 localStorage에 저장
        localStorage.setItem("accessToken", data.access);
        localStorage.setItem("refreshToken", data.refresh);

        // 로그인 후 이동


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

