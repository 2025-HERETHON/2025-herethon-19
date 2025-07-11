import random
from community.models import Post, Comment, Keyword
from django.contrib.auth import get_user_model
from profiles.models import Profile, Interest

User = get_user_model()

# 좋아요 모델 import (예시)
from community.models import Like  # 실제 프로젝트에 맞게 경로 및 모델명 수정 필요

def create_test_users():
    users_info = [
        {"email": "dbstj23145890@naver.com", "nickname": "김멘티", "user_type": "mentee"},
        {"email": "dbstj23145891@naver.com", "nickname": "박멘토", "user_type": "mentor"},
        {"email": "dbstj23145892@naver.com", "nickname": "이사용자", "user_type": "mentee"},
    ]
    users = []
    for info in users_info:
        if not User.objects.filter(email=info["email"]).exists():
            user = User.objects.create_user(
                email=info["email"],
                password="Test1234!!",
                nickname=info["nickname"],
                user_type=info["user_type"],
                point=50
            )
            profile = Profile.objects.create(user=user)
            interests_names = ["백엔드 개발", "데이터 분석", "마케팅"]
            for name in interests_names:
                interest, _ = Interest.objects.get_or_create(name=name, defaults={"category": "it"})
                profile.interests.add(interest)
            users.append(user)
        else:
            users.append(User.objects.get(email=info["email"]))
    print("테스트 유저 생성 완료")
    return users

def create_dummy_posts_and_comments(users):
    author = users[0]  # 첫 번째 유저가 게시글 작성자 (김멘티)
    other_users = users[1:]  # 다른 유저들

    dummy_posts_data = [
        {
            "title": "시간 관리 질문드려요.",
            "content": "효율적인 시간 관리를 위해 어떤 방법을 사용하시나요? 추천하는 앱이나 팁 있으면 알려주세요!",
            "tags": ["시간관리", "생산성"],
            "comments": [
                {"author": author, "content": "저는 토마토 타이머 기법을 사용해요!"},
                {"author": other_users[0], "content": "시간 기록 앱 써보는 것도 추천합니다."},
            ],
        },
        {
            "title": "프론트엔드 스터디",
            "content": "React, Vue, Angular 중 어떤 프레임워크로 스터디 시작하는 게 좋을까요?",
            "tags": ["프론트엔드 개발", "스터디"],
            "comments": [
                {"author": author, "content": "저는 React 추천해요. 자료도 많고 커뮤니티도 활발합니다."},
                {"author": other_users[1], "content": "Vue도 배우기 쉽고 좋은 것 같아요!"},
            ],
        },
        {
            "title": "리액트 상태 관리, 언제까지 useState로 버틸 수 있을까?",
            "content": "Context API, Redux, Zustand 등 고민이 많아졌습니다. 여러분은 어떻게 상태 관리하시나요?",
            "tags": ["프론트엔드 개발"],
            "comments": [
                {"author": author, "content": "저도 함께 공부하고 싶어요! 미팅 일정 어떻게 정하실 건가요?"},
                {"author": other_users[0], "content": "상태 관리 라이브러리 추천 부탁드립니다."},
            ],
        },
        {
            "title": "성능 최적화, 어디까지 신경 써야 할까요?",
            "content": "Lighthouse 점수에 집착하는 게 맞는 걸까요? 사용자 경험에 더 집중해야 할까요?",
            "tags": ["프론트엔드 개발"],
            "comments": [
                {"author": author, "content": "성능 최적화는 이미지 최적화부터 시작하는 게 좋다고 들었어요."},
                {"author": other_users[1], "content": "디자인 시스템 고민 공감합니다. 작은 프로젝트라도 미리 도입해두면 편해요."},
            ],
        },
    ]

    created_posts = []

    for post_data in dummy_posts_data:
        post = Post.objects.create(
            author=author,
            title=post_data["title"],
            content=post_data["content"]
        )
        # 태그 연결
        for tag_name in post_data["tags"]:
            keyword, created = Keyword.objects.get_or_create(name=tag_name, defaults={'category': 'it'})
            if not created and keyword.category != "it":
                keyword.category = "it"
                keyword.save()
            post.keywords.add(keyword)

        # 댓글 생성
        for comment_info in post_data.get("comments", []):
            Comment.objects.create(
                post=post,
                author=comment_info["author"],
                content=comment_info["content"]
            )
        
        created_posts.append(post)

    # 좋아요(Like) 생성 — 첫 번째 유저가 모든 게시글 중 절반 정도 좋아요 누른 상태로 만들기 (예시)
    for post in created_posts[:len(created_posts)//2]:
        Like.objects.get_or_create(user=author, post=post)

    print("더미 게시글, 댓글, 좋아요 생성 완료")
    return created_posts

def run_all():
    users = create_test_users()
    posts = create_dummy_posts_and_comments(users)
    return posts

