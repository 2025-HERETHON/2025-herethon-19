document.addEventListener("DOMContentLoaded", () => {
  const certifyBtn = document.querySelector(".certify-btn");
  const skipSection = document.querySelector(".skip-section");
  const fileInput = document.getElementById("fileInput");
  const mentoIntro = document.getElementById("mentoIntro");
  const fileList = document.getElementById("fileList");
  const textCount = document.querySelector(".text-count");

  // 업로드 버튼 → 모달 열기
  const uploadBtn = document.getElementById("uploadBtn");
  const uploadModal = document.getElementById("uploadModal");
  const closeUpload = document.getElementById("closeUpload");

  uploadBtn.addEventListener("click", () => {
    uploadModal.style.display = "flex";
  });

  closeUpload.addEventListener("click", () => {
    uploadModal.style.display = "none";
  });

  // 파일 선택 시 화면에 표시
  fileInput.addEventListener("change", () => {
    fileList.innerHTML = ""; // 기존 목록 초기화
    const files = fileInput.files;
    if (files.length === 0) return;

    const file = files[0]; // 하나만
    const fileItem = document.createElement("div");
    fileItem.className = "file-item";
    fileItem.innerHTML = `
      <span class="file-name">${file.name}</span>
      <span class="remove">X</span>
    `;
    fileList.appendChild(fileItem);

    // 삭제 버튼
    fileItem.querySelector(".remove").addEventListener("click", () => {
      fileInput.value = "";
      fileList.innerHTML = "";
    });
  });

  // 글자 수 실시간 표시
  mentoIntro.addEventListener("input", () => {
  if (mentoIntro.value.length > 500) {
    mentoIntro.value = mentoIntro.value.slice(0, 500); // 글자수 강제 자르기
  }
  textCount.textContent = `${mentoIntro.value.length}/500`;
});

  // 멘토 인증 제출
  certifyBtn.addEventListener("click", async (e) => {
    e.preventDefault();

    const files = fileInput.files;
    const email = localStorage.getItem("join_email");
    const password = localStorage.getItem("join_password");
    const password2 = localStorage.getItem("join_password2");
    const nickname = localStorage.getItem("join_nickname");
    const phone = localStorage.getItem("join_phone");
    const userType = localStorage.getItem("user_type");
    const interestIds = JSON.parse(localStorage.getItem("join_interest_ids") || "[]");
    const isOver14 = localStorage.getItem("join_is_over_14") === "true";
    const agreedTerms = localStorage.getItem("join_agreed_terms") === "true";
    const agreedPrivacy = localStorage.getItem("join_agreed_privacy") === "true";
    const agreedMarketing = localStorage.getItem("join_agreed_marketing") === "true";
    const introduction = mentoIntro.value.trim();

    if (!email) {
      alert("이메일 정보가 없습니다. 처음부터 다시 진행해주세요.");
      return;
    }

    if (files.length === 0) {
      alert("증빙 파일을 최소 1개 이상 첨부해주세요.");
      return;
    }

    const formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);
    formData.append("password2", password2);
    formData.append("nickname", nickname);
    formData.append("phone_number", phone);
    formData.append("user_type", userType);
    formData.append("mentor_introduction", introduction);
    formData.append("mentor_document", files[0]);
    formData.append("mentor_skip", false);
    formData.append("is_over_14", isOver14);
    formData.append("agreed_terms", agreedTerms);
    formData.append("agreed_privacy", agreedPrivacy);
    formData.append("agreed_marketing", agreedMarketing);
    interestIds.forEach(id => formData.append("interest_ids", id));

    try {
      const response = await fetch("http://localhost:8000/api/accounts/signup/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        alert("회원가입이 완료되었습니다.");
        localStorage.clear();
        window.location.href = "/logIn/logIn.html";
      } else {
        const error = await response.json();
        alert("회원가입 실패: " + (error.message || "서버 오류"));

        // 실패 시 localStorage 초기화 추가
        localStorage.removeItem("join_email");
        localStorage.removeItem("join_password");
        localStorage.removeItem("join_password2");
        localStorage.removeItem("join_nickname");
        localStorage.removeItem("join_phone");
      }
    } catch (error) {
      console.error("에러 발생:", error);
      alert("서버 요청 중 문제가 발생했습니다.");
    }
  });

  // 건너뛰기
  skipSection.addEventListener("click", async () => {
    const confirmSkip = confirm("멘토 인증 없이 가입을 완료하시겠습니까?");
    if (!confirmSkip) return;

    const email = localStorage.getItem("join_email");
    const password = localStorage.getItem("join_password");
    const password2 = localStorage.getItem("join_password2");
    const nickname = localStorage.getItem("join_nickname");
    const phone = localStorage.getItem("join_phone");
    const userType = localStorage.getItem("user_type");
    const interestIds = JSON.parse(localStorage.getItem("join_interest_ids") || "[]");
    const isOver14 = localStorage.getItem("join_is_over_14") === "true";
    const agreedTerms = localStorage.getItem("join_agreed_terms") === "true";
    const agreedPrivacy = localStorage.getItem("join_agreed_privacy") === "true";
    const agreedMarketing = localStorage.getItem("join_agreed_marketing") === "true";

    const formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);
    formData.append("password2", password2);
    formData.append("nickname", nickname);
    formData.append("phone_number", phone);
    formData.append("user_type", userType);
    formData.append("mentor_skip", true);
    formData.append("is_over_14", isOver14);
    formData.append("agreed_terms", agreedTerms);
    formData.append("agreed_privacy", agreedPrivacy);
    formData.append("agreed_marketing", agreedMarketing);
    interestIds.forEach(id => formData.append("interest_ids", id));

    try {
      const response = await fetch("http://localhost:8000/api/accounts/signup/", {
        method: "POST",
        body: formData,
      });

      console.log("응답 상태:", response.status);
      console.log("응답 JSON:", await response.clone().json());

      if (response.ok) {
        alert("회원가입이 완료되었습니다.");
        localStorage.clear();
        window.location.href = "/logIn/logIn.html";
      } else {
        const error = await response.json();
        alert("가입 실패: " + (error.message || "서버 오류"));

        //실패 시 localStorage 초기화 추가
        localStorage.removeItem("join_email");
        localStorage.removeItem("join_password");
        localStorage.removeItem("join_password2");
        localStorage.removeItem("join_nickname");
        localStorage.removeItem("join_phone");
      }
    } catch (error) {
      console.error("에러 발생:", error);
      alert("서버 요청 중 문제가 발생했습니다.");
    }
  });
});
