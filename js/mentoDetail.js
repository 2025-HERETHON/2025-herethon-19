document.addEventListener("DOMContentLoaded", () => {
  const heart = document.querySelector(".heart-icon");
  const count = document.querySelector(".like-count");

  heart.addEventListener("click", () => {
    const liked = heart.getAttribute("data-liked") === "true";
    heart.setAttribute("data-liked", !liked);

    // 이미지 토글
    heart.src = liked ? "/assets/heartNone.svg" : "/assets/heartSelect.svg";

    // 숫자 갱신
    let current = parseInt(count.textContent, 10);
    count.textContent = liked ? current - 1 : current + 1;
  });
});

// 모달 열기
function openModal(id) {
  document.getElementById(id).style.display = "flex";
}

// 모달 닫기
function closeModal(id) {
  document.getElementById(id).style.display = "none";
}

// 모든 닫기 버튼에 이벤트 등록
document.querySelectorAll(".close-btn, .cancel-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const modalId = btn.dataset.close;
    if (modalId) closeModal(modalId);
  });
});

// 멘토 신청 버튼 클릭 시
document.querySelector(".apply-btn").addEventListener("click", () => {
  openModal("applyModal");
});

// 열람하기 버튼들 이벤트 등록
document.querySelectorAll(".review-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    openModal("confirmPointModal");
  });
});

// 예 버튼 클릭 → 조건 분기
document.getElementById("confirmPointYes").addEventListener("click", () => {
  const userPoint = 10; // 추후 API 연동 예정
  closeModal("confirmPointModal");

  if (userPoint < 5) {
    openModal("pointLackModal");
  } else {
    openModal("reviewPopupModal");
  }
});

async function loadSidebarProfile() {
  const token = localStorage.getItem("accessToken");

  try {
    const response = await fetch("http://localhost:8000/api/profiles/profile/me/", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!response.ok) throw new Error("프로필 정보 조회 실패");
    const data = await response.json();

    const usernameEl = document.querySelector(".username");
    if (usernameEl) usernameEl.textContent = data.nickname || "닉네임 없음";

    const pointEl = document.querySelector(".point");
    if (pointEl) pointEl.textContent = `${data.point ?? 0}잎`;

    const tagListEl = document.querySelector(".tag-list");
    if (tagListEl && Array.isArray(data.interests)) {
      tagListEl.innerHTML = "";
      data.interests.forEach(tag => {
        const span = document.createElement("span");
        span.className = "tag";
        span.textContent = tag;
        tagListEl.appendChild(span);
      });
    }

  } catch (err) {
    console.error("❌ 사이드바 프로필 불러오기 실패:", err.message);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // "멘토 탐색" 링크 클릭 시 페이지 이동
  const exploreLink = document.querySelector('.header-nav a:nth-child(2)'); // 두 번째 a 태그 (멘토 탐색)

  if (exploreLink) {
    exploreLink.addEventListener('click', (e) => {
      e.preventDefault(); // 기본 이동 방지
      window.location.href = '/searchMento/findMento.html'; // 원하는 경로로 이동
    });
  }
});

