window.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("accessToken");

  if (!token) {
    console.error("토큰 없음: 로그인 필요");
    return;
  }

  // 프로필 정보 요청 및 이후 모든 처리
  fetch("http://localhost:8000/api/profiles/profile/me/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) throw new Error("프로필 정보 불러오기 실패");
      return response.json();
    })
    .then((data) => {
      const userType = data.user_type;

      const nicknameEl = document.querySelector(".LvAndName span");
      const pointEl = document.querySelector(".leaf-count");
      const tagListEl = document.querySelector(".tag-list");
      const labelEl = document.querySelector(".menteeORmentor");
      const levelIcon = document.querySelector(".lv-icon");

      if (nicknameEl) nicknameEl.textContent = data.nickname;
      if (pointEl) pointEl.textContent = `${data.point}잎`;

      if (tagListEl && Array.isArray(data.interests)) {
        tagListEl.innerHTML = "";
        data.interests.forEach((interest) => {
          const tag = document.createElement("span");
          tag.className = "tag";
          tag.textContent = interest;

          if (userType === "mentor") {
            tag.style.border = "1px solid #7B6CF6";
            tag.style.background = "rgba(123, 108, 246, 0.50)";
          }

          tagListEl.appendChild(tag);
        });
      }

      if (userType === "mentor") {
        const bgEls = document.querySelectorAll(".my-info-cnt, .mymentor");
        bgEls.forEach((el) => {
          el.style.background = "rgba(123, 108, 246, 0.10)";
        });

        if (labelEl) labelEl.textContent = "나의 멘티";
        if (levelIcon) levelIcon.setAttribute("src", "../img/mentorLv.svg");
      }

      const container = document.getElementById("request-list");
      if (!container) return;

      const url = userType === "mentor" ? "http://localhost:8000/api/matching/matching-status/mentee/" : "http://localhost:8000/api/matching/my-matches/";

      fetch(url, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      })
        .then((res) => {
          if (!res.ok) throw new Error("매칭 정보 불러오기 실패");
          return res.json();
        })
        .then((matches) => {
          container.innerHTML = "";

          matches.forEach((match) => {
            const isAccepted = match.status === "accepted";
            const name = userType === "mentor" ? match.mentee_nickname : match.mentor_nickname;
            const email = userType === "mentor" ? match.mentee_email : match.mentor_email;
            const phone = userType === "mentor" ? match.mentee_phone : match.mentor_phone;

            const card = document.createElement("div");
            card.className = "request-card";

            let contactInfo = "<p>연락처 비공개</p>";
            if (isAccepted && email && phone) {
              contactInfo = `
                  <p class="email">📧 ${email}</p>
                  <p class="phone">📞 ${phone}</p>
                `;
            }

            let buttons = "";
            if (userType === "mentor" && !isAccepted) {
              buttons = `
                  <div class="action-buttons">
                    <button class="accept-btn" data-id="${match.id}">수락</button>
                    <button class="reject-btn" data-id="${match.id}">거절</button>
                  </div>
                `;
            }

            card.innerHTML = `
                <div class="profile-box">
                  <img src="../img/profile.svg" alt="유저 이미지" class="mentee-img" />
                  <div class="mentee-info">
                    <p class="mentee-name">${name}</p>
                    <p class="request-date">${isAccepted ? "수락됨" : "대기 중"}</p>
                  </div>
                </div>
                <div class="action-info">${contactInfo}</div>
                ${buttons}
              `;

            container.appendChild(card);
          });

          // 이벤트 바인딩 (수락/거절 버튼)
          if (userType === "mentor") {
            container.querySelectorAll(".accept-btn").forEach((btn) => {
              btn.addEventListener("click", () => {
                const requestId = btn.dataset.id;
                respondToRequest(requestId, "accept", token);
              });
            });

            container.querySelectorAll(".reject-btn").forEach((btn) => {
              btn.addEventListener("click", () => {
                const requestId = btn.dataset.id;
                respondToRequest(requestId, "rejected", token);
              });
            });
          }
        });
    })
    .catch((err) => {
      console.error("전체 처리 중 오류:", err);
    });
});

// 멘토 응답 처리 함수
function respondToRequest(requestId, action, token) {
  fetch("http://localhost:8000/api/matching/respond/", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      request_id: Number(requestId),
      action: action,
    }),
  })
    .then((res) => {
      if (!res.ok) throw new Error("응답 처리 실패");
      return res.json();
    })
    .then(() => {
      alert(`요청이 ${action === "accept" ? "수락" : "거절"}되었습니다.`);
      location.reload();
    })
    .catch((err) => {
      console.error("멘토 응답 중 오류:", err);
    });
}
