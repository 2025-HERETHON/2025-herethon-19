document.addEventListener('DOMContentLoaded', function () {
  const modal = document.querySelector('.modal-overlay');
  const closeBtn = document.querySelector('.modal-close');

  const hasShownPopup = localStorage.getItem('hasSeenPremiumPopup');
  if (!hasShownPopup && modal) {
    modal.style.display = 'flex';
    localStorage.setItem('hasSeenPremiumPopup', 'true');
  }
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      modal.style.display = 'none';
    });
  }

  loadSidebarProfile();
  loadCommunityPosts();

  // 글쓰기 버튼 이벤트 추가
  const writeBtn = document.querySelector('.write-btn');
  if (writeBtn) {
    writeBtn.addEventListener('click', async () => {
      const token = localStorage.getItem("accessToken");
      try {
        const res = await fetch("http://localhost:8000/api/profiles/profile/me/", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });
        if (!res.ok) throw new Error("유저 정보 불러오기 실패");
        const data = await res.json();
        if (data.is_mentor) {
          window.location.href = "/communityUI/communityMento.html";
        } else {
          window.location.href = "/communityUI/communityMentee.html";
        }
      } catch (err) {
        alert("사용자 정보를 불러오지 못했습니다.");
      }
    });
  }
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

async function loadCommunityPosts(page = 1, search = "") {
  const token = localStorage.getItem("accessToken");
  try {
    const url = new URL(`http://localhost:8000/api/community/posts/`);
    url.searchParams.append("page", page);
    if (search) url.searchParams.append("search", search);

    const response = await fetch(url.toString(), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    if (!response.ok) throw new Error("게시글 불러오기 실패");
    const data = await response.json();
    renderPosts(data.results);
  } catch (err) {
    console.error("에러 발생:", err.message);
  }
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
        <img src="/assets/${post.liked ? 'heartSelect' : 'heartNone'}.svg" class="heart-icon" style="cursor:pointer" />
        <span class="like-count">${post.like_count}</span>
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

    const likeIcon = postCard.querySelector(".heart-icon");
    const likeCountSpan = postCard.querySelector(".like-count");

    likeIcon.addEventListener("click", async (e) => {
      e.preventDefault();
      e.stopPropagation();

      const token = localStorage.getItem("accessToken");
      try {
        const res = await fetch(`http://localhost:8000/api/community/posts/${post.id}/like/`, {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });

        if (!res.ok) throw new Error("좋아요 요청 실패");
        const data = await res.json();

        likeIcon.setAttribute("src", data.liked
          ? `/assets/heartSelect.svg?v=${Date.now()}`
          : `/assets/heartNone.svg?v=${Date.now()}`);

        const currentCount = parseInt(likeCountSpan.textContent);
        likeCountSpan.textContent = data.liked ? currentCount + 1 : currentCount - 1;

      } catch (err) {
        console.error("좋아요 처리 에러:", err.message);
      }
    });

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
      loadCommunityPosts(1, keyword);
    });
  }
});

document.addEventListener('click', function (e) {
  if (e.target.classList.contains('post-link')) {
    const postId = e.target.dataset.id;
    window.location.href = `/communityUI/communityPost.html?id=${postId}`;
  }
});

async function loadSidebarProfile() {
  const token = localStorage.getItem("accessToken");

  try {
    const response = await fetch("http://localhost:8000/api/profiles/profile/me/", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!response.ok) throw new Error("프로필 정보 조회 실패");
    const data = await response.json();

    const usernameEl = document.querySelector(".username");
    if (usernameEl) usernameEl.textContent = data.nickname || "닉네임 없음";

    const pointEl = document.querySelector(".point");
    if (pointEl) pointEl.textContent = `${data.point ?? 0}잎`;

    const tagListEl = document.querySelector(".tag-list");
    if (tagListEl && Array.isArray(data.interests)) {
      tagListEl.innerHTML = "";
      data.interests.forEach(tag => {
        const span = document.createElement("span");
        span.className = "tag";
        span.textContent = tag;
        tagListEl.appendChild(span);
      });
    }

  } catch (err) {
    console.error("❌ 사이드바 프로필 불러오기 실패:", err.message);
  }
}
