document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("accessToken");
  if (!token) {
    alert("로그인이 필요합니다.");
    window.location.href = "/logIn/logIn.html";
  }
});
const heartIcon = document.getElementById('heartIcon');
const likeCount = document.getElementById('likeCount');

let liked = false;

heartIcon?.addEventListener('click', () => {
  liked = !liked;
  heartIcon.src = liked ? '/assets/heartSelect.svg' : '/assets/heartNone.svg';

  let count = parseInt(likeCount.textContent);
  likeCount.textContent = liked ? count + 1 : count - 1;
});

document.addEventListener('DOMContentLoaded', function () {
  const modal = document.querySelector('.modal-overlay');
  const closeBtn = document.querySelector('.modal-close');

  const hasShownPopup = sessionStorage.getItem('hasSeenPremiumPopup');

  if (!hasShownPopup) {
    modal.style.display = 'flex';
    sessionStorage.setItem('hasSeenPremiumPopup', 'true');
  }

  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const postItems = document.querySelectorAll('.post-item');
  const pagination = document.querySelector('.pagination');

  if (postItems.length > 5) {
    pagination.style.display = 'block';
  } else {
    pagination.style.display = 'none';
  }
});

document.addEventListener('DOMContentLoaded', () => {
  loadCommunityPosts(); // 첫 로드
});

async function loadCommunityPosts(page = 1, search = "") {
  const token = localStorage.getItem("accessToken");

  try {
    const url = new URL(`http://localhost:8000/api/community/posts/`);
    url.searchParams.append("page", page);
    if (search) {
      url.searchParams.append("search", search);
    }

    const response = await fetch(url.toString(), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error("게시글 불러오기 실패");
    }

    const data = await response.json();
    renderPosts(data.results);
  } catch (err) {
    console.error("에러 발생:", err.message);
  }
  console.log("📌 사용 중인 accessToken:", token);
  console.log("📨 요청 URL:", url.toString());
  console.log("📤 fetch 요청 헤더:", {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  });

}

function renderPosts(posts) {
  const postList = document.querySelector(".post-list");
  postList.innerHTML = "";

  posts.forEach(post => {
    const postCard = document.createElement("div");
    postCard.classList.add("post-card");

    const tags = post.keywords.map(tag => `<span class="tag">${tag.name}</span>`).join('');

    postCard.innerHTML = `
      <div class="post-header">
        <div class="post-title post-link" data-id="${post.id}">${post.title}</div>
        <div class="post-tag">${tags}</div>
      </div>
      <div class="post-content">
        <p>${post.content}</p>
      </div>
      <div class="post-meta">
        <img src="/assets/heartNone.svg" class="heart-icon" />
        <span>${post.like_count}</span>
        <img src="/assets/commentIcon.svg" class="comment-icon" />
        <span>${post.comment_count}</span>
        <span class="divider"></span>
        <div class="info">
          <span>${formatDate(post.created_at)}</span>
          <span class="divider"></span>
          <span>${post.author.username}</span>
        </div>
      </div>
    `;

    postList.appendChild(postCard);
  });
}

function formatDate(isoString) {
  const date = new Date(isoString);
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`;
}

document.addEventListener('DOMContentLoaded', () => {
  const searchBtn = document.querySelector('.search-btn');
  const searchInput = document.querySelector('.community-search');

  if (searchBtn) {
    searchBtn.addEventListener('click', () => {
      const keyword = searchInput.value.trim();
      loadCommunityPosts(1, keyword); // 검색 기능
    });
  }
});

document.addEventListener('click', function (e) {
  if (e.target.classList.contains('post-link')) {
    const postId = e.target.dataset.id;
    window.location.href = `/communityUI/communityPost.html?id=${postId}`;
  }
});
