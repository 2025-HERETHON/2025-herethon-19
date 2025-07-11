document.addEventListener('DOMContentLoaded', () => {
  const input = document.querySelector('.comment-input');
  const sendBtn = document.querySelector('.send-btn');
  const commentList = document.querySelector('.dynamic-comments');
  const commentCountSpan = document.querySelector('.comment-count');

  let commentCount = 0;

  function getToday() {
    const now = new Date();
    return now.toISOString().split('T')[0];
  }

  function updateCommentCount(change) {
    commentCount += change;
    if (commentCountSpan) {
      commentCountSpan.textContent = commentCount;
    }
  }

  function createComment(text) {
    // 댓글 컨테이너
    const comment = document.createElement('div');
    comment.className = 'comment';

    // 프로필 이미지
    const profileImg = document.createElement('img');
    profileImg.className = 'comment-Profile-icon';
    profileImg.src = '/assets/commentProfile.svg';
    profileImg.alt = 'profile';

    // 댓글 내용 영역
    const body = document.createElement('div');
    body.className = 'comment-body';

    // 메타 정보
    const meta = document.createElement('div');
    meta.className = 'comment-meta';

    const main = document.createElement('div');
    main.className = 'comment-main';

    const author = document.createElement('span');
    author.className = 'comment-author';
    author.textContent = '김멘티';

    const textDiv = document.createElement('div');
    textDiv.className = 'comment-text';
    textDiv.textContent = text;

    const date = document.createElement('span');
    date.className = 'comment-date';
    date.textContent = getToday();

    main.appendChild(author);
    main.appendChild(textDiv);
    meta.appendChild(main);
    meta.appendChild(date);
    body.appendChild(meta);

    // 삭제 버튼
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'delete-btn';
    deleteBtn.textContent = '삭제';

    deleteBtn.addEventListener('click', () => {
      comment.remove();
      updateCommentCount(-1);
    });

    const actions = document.createElement('div');
    actions.className = 'comment-actions';
    actions.appendChild(deleteBtn);
    actions.style.marginTop = '6px';

    body.appendChild(actions);
    comment.appendChild(profileImg);
    comment.appendChild(body);

    // DOM에 추가
    commentList.appendChild(comment);
    updateCommentCount(1);
  }

  // 댓글 등록 버튼 클릭 시
  sendBtn.addEventListener('click', async () => {
    const value = input.value.trim();
    if (!value) return;

    const postId = document.body.dataset.postId;
    const token = localStorage.getItem('accessToken');

    try {
      const res = await fetch(`http://localhost:8000/api/community/posts/${postId}/comments/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ content: value })
      });

      if (res.ok) {
        createComment(value);
        input.value = '';
      } else {
        const err = await res.json();
        alert('댓글 등록 실패: ' + (err.content || '오류 발생'));
      }
    } catch (err) {
      alert('댓글 등록 중 오류 발생');
    }
  });

  // Enter 키 입력 시 댓글 등록
  input.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendBtn.click();
    }
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const heartIcon = document.querySelector('.heart-icon');
  const likeCount = document.querySelector('.like-count');
  const postId = document.body.dataset.postId;
  const token = localStorage.getItem('accessToken');

  let liked = false;
  let likeNum = parseInt(likeCount.textContent, 10) || 0;

  heartIcon.addEventListener('click', async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/community/posts/${postId}/like/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (res.ok) {
        const data = await res.json();
        liked = data.liked;

        if (liked) {
          heartIcon.src = '/assets/heartSelect.svg';
          likeNum += 1;
        } else {
          heartIcon.src = '/assets/heartNone.svg';
          likeNum -= 1;
        }

        likeCount.textContent = likeNum;
      } else {
        alert("좋아요 실패");
      }
    } catch (err) {
      console.error("좋아요 에러:", err);
      alert("좋아요 중 오류 발생");
    }
  });
});
