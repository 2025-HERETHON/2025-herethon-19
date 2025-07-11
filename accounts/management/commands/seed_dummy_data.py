# accounts/management/commands/seed_rich_dummy_data.py
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import CustomUser
from matching.models import MatchingRequest
from point.utils import adjust_point

from matching.models import Review   

class Command(BaseCommand):
    help = '멘토·멘티 4쌍 / 매칭·리뷰·좋아요'

    def _create_user(self, email, nickname, user_type):
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={'nickname': nickname, 'user_type': user_type}
        )
        if created:
            user.set_password('test1234')
            user.save()
        return user

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("\n📌 리치 더미 데이터 생성 시작...\n"))

        # ---------- 1) 유저 8명 ----------
        mentors = [
            self._create_user(f"mentor{i}@test.com",  f"멘토{i}",  "mentor")
            for i in range(1, 5)
        ]
        mentees = [
            self._create_user(f"mentee{i}@test.com",  f"멘티{i}",  "mentee")
            for i in range(1, 5)
        ]

        # ---------- 2) 매칭 6건 ----------
        matching_specs = [
            # (멘토 index, 멘티 index, status)
            (0, 0, "accepted"),
            (1, 1, "accepted"),
            (2, 2, "pending"),
            (3, 3, "accepted"),
            (0, 2, "accepted"),  
            (1, 3, "pending"),
            (2, 3, "accepted"),
        ]
        for m_idx, t_idx, status in matching_specs:
            MatchingRequest.objects.get_or_create(
                mentor=mentors[m_idx],
                mentee=mentees[t_idx],
                defaults={'status': status}
            )

        # ---------- 3) 좋아요 3건 ----------
        adjust_point(mentors[0], +5, event_type="like_received")
        adjust_point(mentors[1], +5, event_type="like_received")
        adjust_point(mentors[0], +5, event_type="like_received")   # 멘토1 한 번 더

        # ---------- 4) 리뷰 4건 & 포인트 ----------
        review_pairs = [
            (mentees[0], mentors[0], "정말 친절한 설명 감사합니다!"),
            (mentees[1], mentors[1], "덕분에 많이 배웠습니다."),
            (mentees[2], mentors[0], "도움이 되었어요."),
            (mentees[3], mentors[2], "예시 리뷰"),
        ]
        for mentee, mentor, content in review_pairs:
            try:
                match = MatchingRequest.objects.get(
                mentor=mentor,
                mentee=mentee,
                status="accepted"
                )
            except MatchingRequest.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"❌ 매칭 없음: {mentor} ← {mentee}"))
                continue

            review, created = Review.objects.get_or_create(
                match=match,
                defaults={
                    "comment": content,
                    "rating": 5,
                    "created_at": timezone.now(),
                },
            )

            if created:
                adjust_point(mentee, +5, event_type="review_written")
                adjust_point(mentor, +5, event_type="review_received")

        # ---------- 5) 리뷰 열람(멘티0, 멘티1) ----------
        adjust_point(mentees[0], +5, event_type="review_written")
        adjust_point(mentees[1], +5, event_type="review_written")

        adjust_point(mentees[0], -5, event_type="review_opened")
        adjust_point(mentees[1], -5, event_type="review_opened")

        # ---------- 6) 결과 출력 ----------
        self.stdout.write(self.style.SUCCESS("\n✅ 리치 더미 데이터 생성 완료"))
        for u in mentors + mentees:
            self.stdout.write(f" - {u.nickname}  |  {u.user_type}  |  포인트 {u.point}")

        self.stdout.write("")  