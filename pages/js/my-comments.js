const commentsPerPage = 7;
let currentPage = 1;

let comments = [
  { content: "저도 요즘 성능 최적화 고민 중이에요! 어떤 방법으로 시작하셨는지 궁금합니다.", date: "2025.07.01" },
  { content: "저도 함께 공부하고 싶어요! 미팅 일정 어떻게 정하실 건가요?", date: "2025.07.01" },
  { content: "디자인 시스템 고민 공감합니다. 작은 프로젝트라도 미리 도입해두면 나중에 편할 것 같더라고요.", date: "2025.07.01" },
  { content: "React와 TypeScript 토이 프로젝트, 너무 좋은 아이디어네요. 참여하고 싶습니다!", date: "2025.06.30" },
  { content: "성능 최적화는 이미지 최적화부터 시작하는 게 좋다고 들었어요. 경험 공유해주시면 감사하겠습니다", date: "2025.06.30" },
  { content: "저도 프론트엔드 최신 트렌드에 관심 많아요. 자료 공유도 부탁드려요!", date: "2025.06.28" },
  { content: "디자인 시스템 도입 후 개발 속도가 확실히 빨라졌어요. 꼭 도입해보시길 추천드려요.", date: "2025.06.28" },
  { content: "토이 프로젝트 하면 코드 리뷰하면 실력 많이 늘 것 같아요. 참여 신청합니다!", date: "2025.06.28" },
  { content: "성능 최적화 팁이나 좋은 자료 있으면 공유해주세요. 저도 도움받고 싶어요.", date: "2025.06.28" },
  { content: "성능 최적화 팁이나 좋은 자료 있으면 공유해주세요. 저도 도움받고 싶어요.", date: "2025.06.28" },
];

function renderComments(page) {
  const container = document.getElementById("post-container");
  container.innerHTML = "";

  const start = (page - 1) * commentsPerPage;
  const selected = comments.slice(start, start + commentsPerPage);

  selected.forEach((comment, index) => {
    const realIndex = start + index;
    const card = document.createElement("div");
    card.className = "card-box";
    card.innerHTML = `
      <div class="date">${comment.date}</div>
      <p>${comment.content}</p>
      <button class="delete-btn" data-index="${realIndex}">✕</button>
    `;
    container.appendChild(card);
  });

  // 삭제 버튼 이벤트
  document.querySelectorAll(".delete-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const idx = Number(e.target.dataset.index);
      comments.splice(idx, 1);
      const maxPage = Math.ceil(comments.length / commentsPerPage);
      if (currentPage > maxPage) currentPage = maxPage;
      renderComments(currentPage);
      renderPagination();
    });
  });

  // 페이지 버튼 활성화
  document.querySelectorAll(".page-btn").forEach((btn) => {
    btn.classList.toggle("active", Number(btn.dataset.page) === page);
  });
}

function renderPagination() {
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  const pageCount = Math.ceil(comments.length / commentsPerPage);
  if (pageCount === 0) return;

  for (let i = 1; i <= pageCount; i++) {
    const btn = document.createElement("button");
    btn.className = "page-btn";
    btn.textContent = i;
    btn.dataset.page = i;
    if (i === currentPage) btn.classList.add("active");
    btn.addEventListener("click", () => {
      currentPage = i;
      renderComments(currentPage);
      renderPagination();
    });
    pagination.appendChild(btn);
  }
}

renderComments(currentPage);
renderPagination();
