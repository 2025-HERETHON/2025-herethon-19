const postsPerPage = 3;
let currentPage = 1;

// 예시 데이터
const posts = [
  {
    title: "React와 TypeScript로 토이 프로젝트 함께할 분 모집합니다!",
    date: "2025.07.01",
    tags: ["프론트엔드 개발", "스터디"],
    content: `React와 TypeScript를 활용한 간단한 웹 앱을 만들고 싶습니다. 코드 리뷰와 피드백도 주고받으면서 함께 성장해봐요!`,
  },
  {
    title: "리액트 상태 관리, 언제까지 useState로 버틸 수 있을까?",
    date: "2025.06.29",
    tags: ["프론트엔드 개발"],
    content: `Context API, Redux, Zustand 등 고민이 많아졌습니다. 여러분은 어떻게 상태 관리하시나요?`,
  },
  {
    title: "성능 최적화, 어디까지 신경 써야 할까요?",
    date: "2025.06.29",
    tags: ["프론트엔드 개발"],
    content: `Lighthouse 점수, 코드 스플리팅, 이미지 최적화 등 고려할 부분이 많아요. 실무에서는 어느 정도까지 고려하시나요?`,
  },
  {
    title: "추가 예시 글 제목",
    date: "2025.06.20",
    tags: ["웹 개발", "포트폴리오"],
    content: `더 많은 글이 추가되었을 때를 대비한 예시입니다.`,
  },
];

// 글 렌더링
function renderPosts(page) {
  const container = document.getElementById("post-container");
  container.innerHTML = "";

  const start = (page - 1) * postsPerPage;
  const selected = posts.slice(start, start + postsPerPage);

  selected.forEach((post) => {
    const card = document.createElement("div");
    card.className = "card-box";
    card.innerHTML = `
      <div class="date">${post.date}</div>
      <h3>${post.title}</h3>
      <div class="tags">
        ${post.tags.map((tag) => `<span class="tag">${tag}</span>`).join("")}
      </div>
      <p>${post.content}</p>
    `;
    container.appendChild(card);
  });

  updatePagination(page);
}

// 페이지네이션 생성 및 활성화
function updatePagination(activePage) {
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = ""; // 초기화

  const totalPages = Math.ceil(posts.length / postsPerPage);

  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.className = "page-btn";
    if (i === activePage) btn.classList.add("active");
    btn.dataset.page = i;
    btn.textContent = i;

    btn.addEventListener("click", () => {
      currentPage = i;
      renderPosts(currentPage);
    });

    pagination.appendChild(btn);
  }
}

// 초기 렌더링
renderPosts(currentPage);
