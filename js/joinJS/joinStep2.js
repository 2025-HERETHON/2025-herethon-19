document.addEventListener("DOMContentLoaded", () => {
  const tags = document.querySelectorAll('.tag');
  const nextButton = document.querySelector('.next-button');

  // 태그 클릭 시 선택/해제
  tags.forEach(tag => {
    tag.addEventListener('click', () => {
      tag.classList.toggle('selected');
    });
  });

  // 다음 버튼 클릭 시
  nextButton.addEventListener('click', () => {
    const selectedTags = document.querySelectorAll('.tag.selected');
    const interestIds = Array.from(selectedTags).map(tag => parseInt(tag.dataset.id, 10));

    const email = localStorage.getItem("join_email");
    if (!email) {
      alert("이메일 정보가 없습니다. 이전 단계부터 다시 시작해주세요.");
      window.location.href = "/join/joinStep1.html";
      return;
    }

    if (interestIds.length === 0) {
      alert("관심 분야를 하나 이상 선택해주세요.");
      return;
    }

    // 로컬스토리지에 관심사 저장
    localStorage.setItem("join_interest_ids", JSON.stringify(interestIds));

    console.log("관심사 저장됨:", interestIds);

    // 다음 단계로 이동
    window.location.href = "/join/joinStep3.html";
  });
});
