# community/dummy_data.py

from community.models import Post, Comment, Keyword
from django.contrib.auth import get_user_model

User = get_user_model()

def create_test_user():
    if not User.objects.filter(email="dbstj231458@naver.com").exists():
        User.objects.create_user(email="dbstj231458@naver.com", password="Test1234!!")
        print("테스트 계정 생성 완료.")
    else:
        print("이미 존재하는 테스트 계정입니다.")

def create_dummy_posts_and_comments():
    user = User.objects.get(email="dbstj231458@naver.com")

    dummy_posts = [
        {
            "title": "React와 TypeScript로 토이 프로젝트 함께할 분 모집합니다!",
            "content": "React와 TypeScript를 활용한 간단한 웹 앱을 만들고 싶습니다. 코드 리뷰와 피드백도 주고받으면서 함께 성장해봐요!",
            "tags": ["프론트엔드 개발", "스터디"],
            "comments": [
                "저도 프론트엔드 최신 트렌드에 관심 많아요. 자료 공유도 부탁드려요!",
                "같이 하면 더 재미있겠네요! 참여하고 싶어요.",
            ],
        },
        {
            "title": "리액트 상태 관리, 언제까지 useState로 버틸 수 있을까?",
            "content": "Context API, Redux, Zustand 등 고민이 많아졌습니다. 여러분은 어떻게 상태 관리하시나요?",
            "tags": ["프론트엔드 개발"],
            "comments": [
                "저도 함께 공부하고 싶어요! 미팅 일정 어떻게 정하실 건가요?",
                "상태 관리 라이브러리 추천 부탁드립니다.",
            ],
        },
        {
            "title": "성능 최적화, 어디까지 신경 써야 할까요?",
            "content": "Lighthouse 점수에 집착하는 게 맞는 걸까요? 사용자 경험에 더 집중해야 할까요?",
            "tags": ["프론트엔드 개발"],
            "comments": [
                "성능 최적화는 이미지 최적화부터 시작하는 게 좋다고 들었어요.",
                "디자인 시스템 고민 공감합니다. 작은 프로젝트라도 미리 도입해두면 편해요.",
            ],
        },
    ]

    for post_data in dummy_posts:
        post = Post.objects.create(
            author=user,
            title=post_data["title"],
            content=post_data["content"]
        )
        # 태그 처리
        for tag_name in post_data["tags"]:
            keyword, _ = Keyword.objects.get_or_create(name=tag_name, category="it")
            post.keywords.add(keyword)
        # 댓글 처리
        for comment_text in post_data.get("comments", []):
            Comment.objects.create(post=post, author=user, content=comment_text)

    print("더미 게시글과 댓글이 성공적으로 생성되었습니다.")

def run_all():
    create_test_user()
    create_dummy_posts_and_comments()
