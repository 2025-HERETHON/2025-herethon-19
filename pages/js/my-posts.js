const postsPerPage = 3;
let currentPage = 1;
const token = localStorage.getItem("accessToken");

// 토큰 확인용 로그
console.log("accessToken:", token);

// 글 렌더링 함수
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
        ${post.keywords.map((tag) => `<span class="tag">${tag.name}</span>`).join("")}
      </div>
      <p>${post.content_preview}</p>
    `;
    container.appendChild(card);
  });
}

// 페이지네이션 렌더링 함수
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

// API 요청 함수
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
      console.log("응답 확인:", data);
      renderPosts(data.results); // posts → results
      updatePagination(data.total_pages); // total_pages가 있어야 함
    })
    .catch((err) => {
      console.error("API 요청 실패:", err);
    });
}

// 초기 호출
fetchPosts(currentPage);
