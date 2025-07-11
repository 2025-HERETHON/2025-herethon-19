const commentsPerPage = 10;
let currentPage = 1;
const token = localStorage.getItem("accessToken");

// 댓글 렌더링
function renderComments(commentList) {
  const container = document.getElementById("post-container");
  container.innerHTML = "";

  commentList.forEach((comment) => {
    const card = document.createElement("div");
    card.className = "card-box";
    card.innerHTML = `
      <div class="date">${comment.created_at?.slice(0, 10) || "날짜 없음"}</div>
      <h4>게시글: ${comment.post_title}</h4>
      <p>${comment.content_preview}</p>
    `;
    container.appendChild(card);
  });
}

// 페이지네이션
function updatePagination(totalCount) {
  const totalPages = Math.ceil(totalCount / commentsPerPage);
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.className = "page-btn";
    btn.textContent = i;
    btn.dataset.page = i;
    if (i === currentPage) btn.classList.add("active");

    btn.addEventListener("click", () => {
      currentPage = i;
      fetchComments(currentPage);
    });

    pagination.appendChild(btn);
  }
}

// API 호출
function fetchComments(page) {
  fetch(`http://localhost:8000/api/mypage/comments/?page=${page}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      if (!res.ok) throw new Error("댓글 불러오기 실패");
      return res.json();
    })
    .then((data) => {
      if (!data.results || !Array.isArray(data.results)) {
        console.error("댓글 리스트가 유효하지 않습니다:", data);
        return;
      }
      renderComments(data.results);
      updatePagination(data.count);
    })
    .catch((err) => {
      console.error("API 요청 실패:", err);
    });
}

// 초기 실행
fetchComments(currentPage);
