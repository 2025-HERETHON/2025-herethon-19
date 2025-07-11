from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from matching.models import MatchingRequest
from point.utils import adjust_point


class Command(BaseCommand):
    help = '여러 멘토/멘티 및 매칭/포인트 더미 생성'

    def handle(self, *args, **kwargs):
        self.stdout.write("더미 유저/매칭/포인트 생성 시작...\n")

        # 멘토1 생성
        mentor1, created = CustomUser.objects.get_or_create(
            email='mentor1@test.com',
            defaults={'nickname': '멘토짱1', 'user_type': 'mentor'}
        )
        if created:
            mentor1.set_password('test1234')
            mentor1.save()

        # 멘토2 생성
        mentor2, created = CustomUser.objects.get_or_create(
            email='mentor2@test.com',
            defaults={'nickname': '멘토짱2', 'user_type': 'mentor'}
        )
        if created:
            mentor2.set_password('test1234')
            mentor2.save()

        # 멘티1 생성
        mentee1, created = CustomUser.objects.get_or_create(
            email='mentee1@test.com',
            defaults={'nickname': '멘티짱1', 'user_type': 'mentee'}
        )
        if created:
            mentee1.set_password('test1234')
            mentee1.save()

        # 멘티2 생성
        mentee2, created = CustomUser.objects.get_or_create(
            email='mentee2@test.com',
            defaults={'nickname': '멘티짱2', 'user_type': 'mentee'}
        )
        if created:
            mentee2.set_password('test1234')
            mentee2.save()

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

        # 포인트 부여 (멘토1: 좋아요 + 리뷰 수신)
        adjust_point(mentor1, +5, event_type='like_received')
        adjust_point(mentor1, +5, event_type='review_received')

        # 멘티1: 리뷰 작성 & 열람
        adjust_point(mentee1, +5, event_type='review_written')
        adjust_point(mentee1, -5, event_type='review_opened')

        # 멘티2: 리뷰 작성만
        adjust_point(mentee2, +5, event_type='review_written')

        self.stdout.write(self.style.SUCCESS("✅ 더미 데이터 생성 완료"))
        self.stdout.write(f"멘토짱1 포인트: {mentor1.point}")
        self.stdout.write(f"멘토짱2 포인트: {mentor2.point}")
        self.stdout.write(f"멘티짱1 포인트: {mentee1.point}")
        self.stdout.write(f"멘티짱2 포인트: {mentee2.point}\n")
