console.log("✅ JS 파일 연결됨");
document.addEventListener('DOMContentLoaded', () => {
  console.log("📦 passwordReset.js 로드됨");

  // ① 이메일 전송 버튼
  const emailBtn = document.querySelector('.passwordCheck-button');
  if (emailBtn) {
    emailBtn.addEventListener('click', async () => {
      const email = document.querySelector('#email').value.trim();
      if (!email) return alert('이메일을 입력해주세요.');

      try {
        const res = await fetch('http://localhost:8000/api/accounts/password-reset/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email })
        });


        const text = await res.text();
        if (res.ok) {
          alert('이메일 전송 성공!');
        } else {
          alert('이메일 전송 실패\n' + text);
        }
      } catch (err) {
        console.error(err);
        alert('네트워크 오류가 발생했습니다.');
      }
    });
  }

  // ② 비밀번호 재설정 버튼
  console.log("✅ DOM loaded");

  const resetBtn = document.querySelector('.password-return-button');
  if (resetBtn) {
    console.log("✅ reset 버튼 찾음");

    resetBtn.addEventListener('click', async () => {
      const password = document.querySelector('#password').value.trim();
      const passwordConfirm = document.querySelector('#confirm_password').value.trim();

      if (!password || !passwordConfirm) return alert("비밀번호를 입력하세요.");
      if (password !== passwordConfirm) return alert("비밀번호가 일치하지 않습니다.");

      const urlParams = new URLSearchParams(window.location.search);
      const uid = urlParams.get('uid');
      const token = urlParams.get('token');

      const payload = {
        new_password: password,
        confirm_password: passwordConfirm
      };

      console.log("📦 보낼 URL:", `http://localhost:8000/api/accounts/password-reset/${uid}/${token}/`);
      console.log("📦 보낼 payload:", payload);

      try {
        const res = await fetch(`http://localhost:8000/api/accounts/password-reset/${uid}/${token}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload)
        });

        const text = await res.text();
        console.log("📦 응답 본문:", text);

        if (res.ok) {
          alert("비밀번호 변경 성공!");
          window.location.href = '/password/result.html';
        } else {
          alert("비밀번호 변경 실패\n" + text);
        }
      } catch (err) {
        console.error("🚨 네트워크 오류:", err);
        alert("네트워크 오류가 발생했습니다.");
      }
    });
  } else {
    console.warn("❌ reset 버튼 못 찾음");
  }

  // ③ 로그인 화면으로 이동
  const backLogin = document.querySelector('.back-login');
  if (backLogin) {
    backLogin.addEventListener('click', () => {
      window.location.href = '/login/login.html';
    });
  }
});
