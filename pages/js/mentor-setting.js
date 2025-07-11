window.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("accessToken");

  if (!token) {
    console.error("토큰 없음: 로그인 필요");
    return;
  }
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

  fetch("http://localhost:8000/api/matching/my-matches/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error(`HTTP ${res.status} - 인증 오류 또는 서버 오류`);
      }
      return res.json();
    })
    .then((mentors) => {
      if (!Array.isArray(mentors)) {
        console.error("멘토 응답 데이터가 배열이 아닙니다:", mentors);
        return;
      }

      const container = document.querySelector(".right-aside-cnt");

      mentors.forEach((mentor) => {
        const isAccepted = mentor.status === "accepted";

        const mentorHTML = `
            <div class="mentor-line">
              <div class="mentor-left">
                <div class="profile-box">
                  <img src="../img/profile.svg" alt="멘토 이미지" class="mentor-img" />
                  <p class="mentor-name">${mentor.mentor_nickname}</p>
                </div>
                <div class="mentor-text">
                  <p><img src="../img/phone.svg" class="icon" />${isAccepted ? mentor.mentor_phone : "비공개"}</p>
                  <p><img src="../img/mail.svg" class="icon" />${isAccepted ? mentor.mentor_email : "비공개"}</p>
                </div>
              </div>
              <div class="mentor-right">
                <div class="mentor-status">
                  <span class="label">매칭 상태</span>
                  <span class="badge ${isAccepted ? "ing" : "wait"}">
                    ${isAccepted ? "진행 중" : "대기 중"}
                  </span>
                </div>
                ${
                  isAccepted
                    ? `<span class="review-link">후기 작성</span>
                <span class="disconnect">연결 해제</span>`
                    : ""
                }
              </div>
            </div>
          `;

        container.insertAdjacentHTML("beforeend", mentorHTML);
      });
    })
    .catch((err) => {
      console.error("멘토 정보 불러오기 실패:", err);
    });
});
