const recordsPerPage = 7;
let currentPage = 1;
let pointHistory = [];

const token = localStorage.getItem("accessToken");

// 프로필 정보 요청
fetch("http://localhost:8000/api/profiles/profile/me/", {
  method: "GET",
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  },
})
  .then((response) => {
    if (!response.ok) {
      throw new Error("프로필 정보 불러오기 실패");
    }
    return response.json();
  })
  .then((data) => {
    const nicknameEl = document.querySelector(".LvAndName span");
    const pointEl = document.querySelector(".leaf-count");
    const tagListEl = document.querySelector(".tag-list");
    const labelEl = document.querySelector(".menteeORmentor");
    const levelIcon = document.querySelector(".lv-icon");

    nicknameEl.textContent = data.nickname;
    pointEl.textContent = `${data.point}잎`;
    tagListEl.innerHTML = "";

    // 관심사 태그 추가 및 mentor일 경우 스타일 지정
    data.interests.forEach((interest) => {
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = interest;

      if (data.user_type === "mentor") {
        tag.style.border = "1px solid #7B6CF6";
        tag.style.background = "rgba(123, 108, 246, 0.50)";
      }

      tagListEl.appendChild(tag);
    });

    // mentor인 경우 배경색 변경
    if (data.user_type === "mentor") {
      const mentorBackgroundTargets = document.querySelectorAll(".my-info-cnt, .mymentor");
      mentorBackgroundTargets.forEach((el) => {
        el.style.background = "rgba(123, 108, 246, 0.10)";
      });

      // 텍스트 변경: 나의 멘토 → 나의 멘티
      if (labelEl) {
        labelEl.textContent = "나의 멘티";
      }
      if (levelIcon) {
        levelIcon.setAttribute("src", "../img/mentorLv.svg");
      }
    }
  })
  .catch((err) => {
    console.error("API 요청 실패:", err);
  });

function fetchPointHistory() {
  if (!token) {
    console.error("토큰 없음: 로그인 필요");
    return;
  }

  fetch("http://localhost:8000/api/point/history/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      if (!res.ok) throw new Error("포인트 내역 요청 실패");
      return res.json();
    })
    .then((data) => {
      // 총 보유 포인트 표시
      const pointTotalEl = document.querySelector(".point-value");
      if (pointTotalEl) {
        pointTotalEl.textContent = data.point;
      }

      // 히스토리 배열 변환 및 저장
      if (!Array.isArray(data.history)) {
        console.error("히스토리 데이터 형식 오류:", data);
        return;
      }

      pointHistory = data.history.map((item) => ({
        action: item.reason,
        point: item.amount,
        date: item.created_at,
        type: item.amount > 0 ? "plus" : "minus",
      }));

      renderPoints(currentPage);
    })
    .catch((err) => {
      console.error("API 요청 실패:", err);
    });
}

function renderPoints(page) {
  const list = document.getElementById("point-list");
  list.innerHTML = "";

  const start = (page - 1) * recordsPerPage;
  const selected = pointHistory.slice(start, start + recordsPerPage);

  selected.forEach((item) => {
    const card = document.createElement("div");
    card.className = "point-card";

    card.innerHTML = `
      <div class="point-left">
        <img src="../img/${item.type === "plus" ? "pointPlus.png" : "pointMinus.png"}" class="point-icon" alt="아이콘" />
        <div class="point-box">
          <div class="point-action">${item.action}</div>
          <div class="point-change ${item.type}">
            ${item.type === "plus" ? "+" : ""}${item.point}
          </div>
        </div>
      </div>
      <div class="point-date">${item.date}</div>
    `;
    list.appendChild(card);
  });

  renderPagination();
}

function renderPagination() {
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  const totalPages = Math.ceil(pointHistory.length / recordsPerPage);
  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.className = "page-btn";
    btn.textContent = i;
    btn.dataset.page = i;
    if (i === currentPage) btn.classList.add("active");
    btn.addEventListener("click", () => {
      currentPage = i;
      renderPoints(currentPage);
    });
    pagination.appendChild(btn);
  }
}

// 최초 실행
fetchPointHistory();
