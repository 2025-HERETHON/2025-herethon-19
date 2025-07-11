window.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("accessToken");

  if (!token) {
    console.error("토큰 없음: 로그인 필요");
    return;
  }

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
        if (levelIcon) levelIcon.setAttribute("src", "img/mentorLv.svg");
      }

      // 멘토 or 멘티의 매칭된 상대 리스트 불러오기
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
          const mentorsCnt = document.querySelector(".mentors-cnt");
          if (!mentorsCnt) return;

          mentorsCnt.innerHTML = ""; // 초기화

          // 매칭된 사람만 추가 (수락된 경우만)
          matches
            .filter((m) => m.status === "accepted")
            .forEach((match) => {
              const name = userType === "mentor" ? match.mentee_nickname : match.mentor_nickname;

              const box = document.createElement("div");
              box.className = "mentors-box";

              box.innerHTML = `
                <div class="mentor-pro">
                  <img src="img/profile.svg" alt="프로필 아이콘" width="80px" />
                  <div>${name}</div>
                </div>
              `;
              mentorsCnt.appendChild(box);
            });
        });
    })
    .catch((err) => {
      console.error("API 요청 실패:", err);
    });
});
