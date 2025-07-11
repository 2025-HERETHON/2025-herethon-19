from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from matching.models import MatchingRequest
from point.utils import adjust_point


class Command(BaseCommand):
    help = '여러 멘토/멘티 및 매칭/포인트 더미 생성'

    def handle(self, *args, **kwargs):
        self.stdout.write("더미 유저/매칭/포인트 생성 시작...")

        # 멘토 2명
        mentor1, _ = CustomUser.objects.get_or_create(
            email='mentor1@test.com',
            defaults={'password': 'test1234', 'nickname': '멘토짱1', 'is_mentor': True}
        )
        mentor2, _ = CustomUser.objects.get_or_create(
            email='mentor2@test.com',
            defaults={'password': 'test1234', 'nickname': '멘토짱2', 'is_mentor': True}
        )

        # 멘티 2명
        mentee1, _ = CustomUser.objects.get_or_create(
            email='mentee1@test.com',
            defaults={'password': 'test1234', 'nickname': '멘티짱1'}
        )
        mentee2, _ = CustomUser.objects.get_or_create(
            email='mentee2@test.com',
            defaults={'password': 'test1234', 'nickname': '멘티짱2'}
        )

        # 매칭 생성
        MatchingRequest.objects.get_or_create(
            mentor=mentor1, mentee=mentee1, defaults={'status': 'accepted'}
        )
        MatchingRequest.objects.get_or_create(
            mentor=mentor2, mentee=mentee2, defaults={'status': 'accepted'}
        )
        MatchingRequest.objects.get_or_create(
            mentor=mentor1, mentee=mentee2, defaults={'status': 'pending'}
        )

        # 포인트 테스트
        # 멘토1: 좋아요 + 리뷰 수신
        adjust_point(mentor1, +5, "좋아요 받음")
        adjust_point(mentor1, +5, "리뷰 수신 보상")

        # 멘토2: 좋아요만 받음
        adjust_point(mentor2, +5, "좋아요 받음")

        # 멘티1: 리뷰 작성 + 리뷰 열람
        adjust_point(mentee1, +5, "리뷰 작성 보상")
        adjust_point(mentee1, -5, "리뷰 열람")

        # 멘티2: 리뷰 작성만 함
        adjust_point(mentee2, +5, "리뷰 작성 보상")

        self.stdout.write(self.style.SUCCESS("더미 데이터 생성 완료 ✅"))
