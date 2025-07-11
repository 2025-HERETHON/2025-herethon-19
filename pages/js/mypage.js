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
      // 여기서 DOM에 데이터 반영
      const nicknameEl = document.querySelector(".LvAndName span");
      const pointEl = document.querySelector(".leaf-count");
      const tagListEl = document.querySelector(".tag-list");

      nicknameEl.textContent = data.nickname;
      pointEl.textContent = `${data.point}잎`;

      // 관심사 태그 갱신
      tagListEl.innerHTML = ""; // 초기화
      data.interests.forEach((interest) => {
        const tag = document.createElement("span");
        tag.className = "tag";
        tag.textContent = interest;
        tagListEl.appendChild(tag);
      });
    })
    .catch((err) => {
      console.error("API 요청 실패:", err);
    });
});
