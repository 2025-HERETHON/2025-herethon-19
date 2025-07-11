const pointRecords = [
  { action: "게시글 작성", point: 5, date: "2025.07.01", type: "plus" },
  { action: "좋아요", point: 5, date: "2025.07.01", type: "plus" },
  { action: "좋아요", point: 5, date: "2025.07.01", type: "plus" },
  { action: "리뷰 열람", point: -5, date: "2025.07.01", type: "minus" },
  { action: "좋아요", point: 5, date: "2025.07.01", type: "plus" },
  { action: "좋아요", point: 5, date: "2025.06.30", type: "plus" },
  { action: "리뷰 열람", point: -5, date: "2025.06.30", type: "minus" },
  { action: "좋아요", point: 5, date: "2025.06.30", type: "plus" },
  { action: "게시글 삭제", point: -5, date: "2025.06.29", type: "minus" },
];

const recordsPerPage = 7;
let currentPage = 1;

function renderPoints(page) {
  const list = document.getElementById("point-list");
  list.innerHTML = "";

  const start = (page - 1) * recordsPerPage;
  const selected = pointRecords.slice(start, start + recordsPerPage);

  selected.forEach((item) => {
    const card = document.createElement("div");
    card.className = "point-card";

    card.innerHTML = `
        <div class="point-left">
          <img src="../img/${item.type === "plus" ? "pointPlus.png" : "pointMinus.png"}" class="point-icon" alt="아이콘" />
          <div class="point-box">
            <div class="point-action">${item.action}</div>
            <div class="point-change ${item.type}">
              ${item.type === "plus" ? "+" : ""}${item.point}
            </div>
          </div>
        </div>
        <div class="point-date">${item.date}</div>
      `;
    list.appendChild(card);
  });

  renderPagination();
}

function renderPagination() {
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  const totalPages = Math.ceil(pointRecords.length / recordsPerPage);
  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.className = "page-btn";
    btn.textContent = i;
    btn.dataset.page = i;
    if (i === currentPage) btn.classList.add("active");
    btn.addEventListener("click", () => {
      currentPage = i;
      renderPoints(currentPage);
    });
    pagination.appendChild(btn);
  }
}

renderPoints(currentPage);
