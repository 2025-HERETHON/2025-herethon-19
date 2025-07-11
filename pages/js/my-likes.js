const postsPerPage = 3;
let currentPage = 1;
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

    nicknameEl.textContent = data.nickname;
    pointEl.textContent = `${data.point}잎`;

    tagListEl.innerHTML = "";
    data.interests.forEach((interest) => {
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = interest;
      tagListEl.appendChild(tag);
    });
  })
  .catch((err) => {
    console.error("프로필 API 요청 실패:", err);
  });

// 글 렌더링
function renderPosts(postList) {
  const container = document.getElementById("post-container");
  container.innerHTML = "";

  postList.forEach((post) => {
    const card = document.createElement("div");
    card.className = "card-box";
    card.innerHTML = `
      <div class="date">${post.created_at?.slice(0, 10) || "날짜 없음"}</div>
      <h3>${post.title}</h3>
      <div class="tags">
        ${post.keywords?.map((tag) => `<span class="tag">${tag.name}</span>`).join("") || ""}
      </div>
      <p>${post.content}</p>
    `;
    container.appendChild(card);
  });
}

// 페이지네이션 생성
function updatePagination(totalCount) {
  const totalPages = Math.ceil(totalCount / postsPerPage);
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
      fetchLikedPosts(currentPage);
    });

    pagination.appendChild(btn);
  }
}

// API 호출
function fetchLikedPosts(page) {
  fetch(`http://localhost:8000/api/mypage/likes/?page=${page}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      if (!res.ok) throw new Error("좋아요 글 불러오기 실패");
      return res.json();
    })
    .then((data) => {
      if (!data.results || !Array.isArray(data.results)) {
        console.error("좋아요 글 리스트가 유효하지 않습니다:", data);
        return;
      }
      renderPosts(data.results);
      updatePagination(data.count);
    })
    .catch((err) => {
      console.error("API 요청 실패:", err);
    });
}

// 초기 렌더링
fetchLikedPosts(currentPage);
