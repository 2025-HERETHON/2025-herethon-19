// 전체 동의 처리
const agreeAll = document.getElementById('agreeAll');
const checkAllIcon = document.getElementById('checkAllIcon');
const checkIcons = document.querySelectorAll('.check-icon');

let isAllAgreed = false;

agreeAll.addEventListener('click', () => {
  isAllAgreed = !isAllAgreed;

  // 전체 아이콘 바꾸기
  checkAllIcon.src = isAllAgreed ? '/assets/checkON.svg' : '/assets/checkOFF.svg';

  // 각 항목 아이콘도 동일하게 변경
  checkIcons.forEach(icon => {
    icon.src = isAllAgreed ? '/assets/checkO.svg' : '/assets/checkX.svg';
  });
});

// 개별 항목 클릭 이벤트 등록 (추가된 부분)
checkIcons.forEach((icon, index) => {
  icon.addEventListener('click', () => {
    const isChecked = icon.src.includes('checkO.svg');
    icon.src = isChecked ? '/assets/checkX.svg' : '/assets/checkO.svg';

    // 모든 항목이 선택되었는지 확인해 전체 동의 상태도 동기화
    const allChecked = Array.from(checkIcons).every(i => i.src.includes('checkO.svg'));
    isAllAgreed = allChecked;
    checkAllIcon.src = allChecked ? '/assets/checkON.svg' : '/assets/checkOFF.svg';
  });
});

window.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('termsModal');
  const modalTitle = document.getElementById('modalTitle');
  const modalBody = document.getElementById('modalBody');
  const closeModal = document.getElementById('closeModal');

  const termsData = {
    0: {
      title: '[필수] HERizon 이용약관 동의',
      body: `
        <p><strong>제1조 (목적)</strong><br>
        이 약관은 HERizon(이하 “서비스”)의 이용조건 및 절차, 회원과 운영자의 권리·의무·책임사항을 규정함을 목적으로 합니다.</p>

        <p><strong>제2조 (회원가입 및 이용계약의 성립)</strong><br>
        회원가입은 본 약관에 동의한 후 가입 신청을 통해 완료됩니다. HERizon은 신청자의 서비스 이용을 승인함으로써 이용계약이 성립됩니다.</p>

        <p><strong>제3조 (서비스 내용)</strong><br>
        HERizon은 다음과 같은 서비스를 제공합니다:</p>
        <ol>
          <li>커리어 멘토-멘티 매칭</li>
          <li>커뮤니티 게시판</li>
          <li>멘토링 콘텐츠 및 자료 제공</li>
          <li>기타 HERizon이 정하는 서비스</li>
        </ol>

        <p><strong>제4조 (회원의 의무)</strong></p>
        <ol>
          <li>타인의 정보를 도용하지 않습니다.</li>
          <li>허위 정보나 부적절한 게시글을 올리지 않습니다.</li>
          <li>HERizon의 원활한 운영을 방해하지 않습니다.</li>
        </ol>

        <p><strong>제5조 (계약 해지 및 이용 제한)</strong><br>
        회원은 언제든지 탈퇴할 수 있으며, 약관 위반 시 서비스 이용이 제한될 수 있습니다.</p>
      `
    },
    1: {
      title: '[필수] 만 14세 이상 서비스 이용 동의',
      body: `
        <p>HERizon은 만 14세 미만 아동의 개인정보를 수집하지 않으며,<br>
        해당 연령 미만 사용자의 서비스 이용은 제한됩니다.</p>
        <p>회원은 본인이 만 14세 이상임을 확인하며 이에 동의합니다.</p>
      `
    },
    2: {
      title: '[필수] 개인정보 수집 / 이용 동의',
      body: `
        <p>HERizon은 아래와 같은 개인정보를 수집·이용합니다.</p>
        <p><strong>1. 수집 항목</strong></p>
        <ol>
          <li>필수: 이름, 이메일, 비밀번호</li>
          <li>선택: 관심 직무, 거주 지역</li>
        </ol>

        <p><strong>2. 이용 목적</strong></p>
        <ol>
          <li>멘토-멘티 매칭</li>
          <li>서비스 제공 및 운영</li>
          <li>커뮤니티 기능 이용</li>
        </ol>

        <p><strong>3. 보유 및 이용 기간</strong><br>
        회원 탈퇴 시까지 보관되며, 이후 지체 없이 파기됩니다.</p>

        <p>※ 자세한 내용은 <strong>[개인정보처리방침]</strong>을 확인해 주세요.</p>
      `
    },
    3: {
      title: '[선택] 마케팅 정보 수신 동의',
      body: `
        <p>HERizon은 신규 서비스, 이벤트, 맞춤 멘토링 콘텐츠 등의 소식을<br>
        이메일 또는 앱 알림으로 안내할 수 있습니다.</p>

        <p>본 동의는 선택사항이며,<br>
        거부하셔도 서비스 이용에 제한은 없습니다.</p>
      `
    }
  };

  const viewLinks = document.querySelectorAll('.view-link');

  viewLinks.forEach((link, index) => {
    link.addEventListener('click', () => {
      modalTitle.innerHTML = termsData[index].title;
      modalBody.innerHTML = termsData[index].body;
      modal.style.display = 'flex';
    });
  });

  closeModal.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  window.addEventListener('click', e => {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const nextButton = document.querySelector(".next-button");

  nextButton.addEventListener("click", async () => {
    const checkIcons = document.querySelectorAll('.terms-list li .check-icon');

    const isTermsAgreed = checkIcons[0].src.includes("checkO.svg");
    const isOver14 = checkIcons[1].src.includes("checkO.svg");
    const isPrivacyAgreed = checkIcons[2].src.includes("checkO.svg");
    const isMarketingAgreed = checkIcons[3].src.includes("checkO.svg");

    if (!isTermsAgreed || !isOver14 || !isPrivacyAgreed) {
      alert("필수 약관에 모두 동의해야 회원가입이 가능합니다.");
      return;
    }

    const email = localStorage.getItem("join_email");
    const userType = localStorage.getItem("user_type"); // "mentor" 또는 "mentee"

    if (!email) {
      console.warn("이메일 누락. localStorage 값:", localStorage);
      alert("이메일 정보가 없습니다. 처음부터 다시 진행해주세요.");
      window.location.href = "/join/joinStep1.html";
      return;
    }

    // 약관 동의 정보를 localStorage에 저장
    localStorage.setItem("join_is_over_14", isOver14);
    localStorage.setItem("join_agreed_terms", isTermsAgreed);
    localStorage.setItem("join_agreed_privacy", isPrivacyAgreed);
    localStorage.setItem("join_agreed_marketing", isMarketingAgreed);

    // 다음 단계로 분기
    if (userType === "mentor") {
      window.location.href = "/join/joinStep4Mento.html";
    } else {
      // 멘티는 회원가입 완료 처리 (여기서 직접 API 요청할 수도 있음)
      window.location.href = "/logIn/login.html";
    }
  });
});