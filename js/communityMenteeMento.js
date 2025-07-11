const openBtn = document.querySelector('.keyword-add');
const modal = document.getElementById('keywordModal');
const closeBtn = document.getElementById('closeModal');
const submitBtn = document.querySelector('.modal-submit');
const tagButtons = document.querySelectorAll('.tag2');
const selectedContainer = document.getElementById('selectedKeywords');

// 모달 열기
openBtn.addEventListener('click', () => {
  // 화면에 이미 표시된 키워드(span 내부 text)
  const selectedTexts = Array.from(document.querySelectorAll('.selected-keyword .text'))
    .map(span => span.textContent.trim());

  // 모든 태그에서 selected 제거
  tagButtons.forEach(tag => {
    tag.classList.remove('selected');
  });

  // 이미 선택된 키워드만 다시 selected 클래스 추가
  tagButtons.forEach(tag => {
    if (selectedTexts.includes(tag.textContent.trim())) {
      tag.classList.add('selected');
    }
  });

  modal.style.display = 'flex';
});

// 모달 닫기
closeBtn.addEventListener('click', () => {
  modal.style.display = 'none';
});

// 바깥 클릭 시 닫기
window.addEventListener('click', (e) => {
  if (e.target === modal) {
    modal.style.display = 'none';
  }
});

// 태그 선택 토글
tagButtons.forEach(tag => {
  tag.addEventListener('click', () => {
    tag.classList.toggle('selected');
  });
});

// 완료 버튼 클릭 시
submitBtn.addEventListener('click', () => {
  const selectedTags = Array.from(document.querySelectorAll('.tag2.selected'))
    .map(tag => tag.textContent.trim());

  // 기존 표시된 키워드 span들
  const existingKeywords = Array.from(document.querySelectorAll('.selected-keyword .text'))
    .map(span => span.textContent.trim());

  // 먼저 기존 DOM에서 중복 제거 후 유지
  selectedContainer.innerHTML = '';
  selectedTags.forEach(text => {
    createKeywordTag(text);
  });

  modal.style.display = 'none'; // 모달 닫기
});

// 키워드 태그 만들기 함수
function createKeywordTag(text) {
  const wrapper = document.createElement('span');
  wrapper.className = 'selected-keyword';

  const textSpan = document.createElement('span');
  textSpan.className = 'text';
  textSpan.textContent = text;

  const removeBtn = document.createElement('span');
  removeBtn.className = 'remove';
  removeBtn.innerHTML = '&times;';
  removeBtn.style.marginLeft = '8px';
  removeBtn.style.cursor = 'pointer';

  removeBtn.addEventListener('click', () => {
    wrapper.remove();
  });

  wrapper.appendChild(textSpan);
  wrapper.appendChild(removeBtn);
  selectedContainer.appendChild(wrapper);
}

// 게시글 등록 처리
const submitButton = document.querySelector('.btn-submit');
const titleInput = document.querySelector('.write-input');
const contentInput = document.querySelector('.write-textarea');

submitButton.addEventListener('click', async () => {
  const token = localStorage.getItem("accessToken");

  const title = titleInput.value.trim();
  const content = contentInput.value.trim();
  const keywordSpans = document.querySelectorAll('.selected-keyword .text');

  if (!title || !content || keywordSpans.length === 0) {
    alert("제목, 내용, 키워드를 모두 입력해주세요.");
    return;
  }

  const keywords = Array.from(keywordSpans).map(text => text.textContent.trim());

  const body = {
    title: title,
    content: content,
    keywords: keywords
  };

  try {
    const response = await fetch("http://localhost:8000/api/community/posts/create/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      const errData = await response.json();
      alert("게시글 등록 실패: " + (errData.title || "오류 발생"));
      return;
    }

    alert("게시글이 등록되었습니다.");
    window.location.href = "/communityUI/communityMain.html";
  } catch (error) {
    console.error("에러:", error);
    alert("게시글 등록 중 오류가 발생했습니다.");
  }
});

