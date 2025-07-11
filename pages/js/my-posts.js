window.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("accessToken");
  const postsPerPage = 3;
  let currentPage = 1;

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

  // 게시글 목록 API 요청
  function fetchPosts(page) {
    fetch(`http://localhost:8000/api/mypage/posts/?page=${page}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("게시글 불러오기 실패");
        return res.json();
      })
      .then((data) => {
        console.log("게시글 응답:", data);
        renderPosts(data.results);
        updatePagination(data.total_pages || 1);
      })
      .catch((err) => {
        console.error("게시글 API 요청 실패:", err);
      });
  }

  function renderPosts(posts) {
    const container = document.getElementById("post-container");
    container.innerHTML = "";

    posts.forEach((post) => {
      const card = document.createElement("div");
      card.className = "card-box";
      card.innerHTML = `
        <div class="date">${post.created_at?.slice(0, 10) || "날짜 없음"}</div>
        <h3>${post.title}</h3>
        <div class="tags">
          ${(post.keywords || []).map((tag) => `<span class="tag">${tag.name}</span>`).join("")}
        </div>
        <p>${post.content_preview}</p>
      `;
      container.appendChild(card);
    });
  }

  function updatePagination(totalPages) {
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    for (let i = 1; i <= totalPages; i++) {
      const btn = document.createElement("button");
      btn.className = "page-btn";
      if (i === currentPage) btn.classList.add("active");
      btn.dataset.page = i;
      btn.textContent = i;

      btn.addEventListener("click", () => {
        currentPage = i;
        fetchPosts(currentPage);
      });

      pagination.appendChild(btn);
    }
  }

  // 초기 게시글 요청
  fetchPosts(currentPage);
});
