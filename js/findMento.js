// 멘토 데이터 배열
const mentors = [
  {
    name: "김멘토",
    tags: ["프론트엔드 개발", "웹 개발", "워킹맘", "시간관리"],
    likes: 190
  },
  {
    name: "이멘토",
    tags: ["UX설계", "디자인 시스템"],
    likes: 175
  },
  {
    name: "박멘토",
    tags: ["기획", "창업", "비즈니스 전략"],
    likes: 183
  },
  {
    name: "정멘토",
    tags: ["AI개발", "데이터 분석"],
    likes: 167
  },
  // 필요한 만큼 더 추가 가능
];

// HTML 요소 참조
const mentoList = document.getElementById('mentoList');

// 카드 생성 및 렌더링
mentors.forEach(mentor => {
  const card = document.createElement('div');
  card.className = 'mento-card';

  card.innerHTML = `
    <div class="mento-profile">
      <div class="mento-image">
        <img src="/assets/mentoProfile.svg" alt="profile" class="mento-profile-icon"/>
      </div>
      <div class="mento-name">${mentor.name}</div>
    </div>
    <div class="mento-tags">
      ${mentor.tags.map(tag => `<span class="tag1">${tag}</span>`).join('')}
    </div>
    <div class="mento-footer">
      <div class="like">
        <img src="/assets/heartNone.svg" alt="좋아요" class="heart-icon">
        <span>${mentor.likes}</span>
      </div>
      <button class="more-btn">더보기</button>
    </div>
  `;

  // 카드 클릭 시 mentoDetail.html 이동
  card.addEventListener('click', () => {
    window.location.href = '/searchMento/mentoDetail.html';
  });

  // 하트 클릭 시 이동 막고 좋아요 처리
  const heartIcon = card.querySelector('.heart-icon');
  heartIcon.addEventListener('click', (e) => {
    e.stopPropagation(); // 카드 클릭 막기
    const isLiked = heartIcon.getAttribute('data-liked') === 'true';

    // 이미지 토글
    heartIcon.src = isLiked ? '/assets/heartNone.svg' : '/assets/heartSelect.svg';
    heartIcon.setAttribute('data-liked', !isLiked);

    // 좋아요 수 업데이트
    const countSpan = heartIcon.nextElementSibling;
    let count = parseInt(countSpan.textContent);
    countSpan.textContent = isLiked ? count - 1 : count + 1;
  });

  // 더보기 버튼 클릭 시 이동 막기
  const moreBtn = card.querySelector('.more-btn');
  moreBtn.addEventListener('click', (e) => {
    e.stopPropagation(); // 카드 클릭 막기
    // 필요 시 기능 추가
  });

  mentoList.appendChild(card);
});

async function loadSidebarProfile() {
  const token = localStorage.getItem("accessToken");

  try {
    const res = await fetch("http://localhost:8000/api/profiles/profile/me/", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!res.ok) throw new Error("프로필 정보 조회 실패");

    const data = await res.json();
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
