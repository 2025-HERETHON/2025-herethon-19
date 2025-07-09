from .models import PointHistory

REASON_MAPPING = {
    'like_received': '좋아요 받음',
    'match_request_received': '멘토링 요청 받음',
    'review_written': '리뷰 작성',
    'review_received': '리뷰 받음',
    'review_opened': '리뷰 열람',
}

def adjust_point(user, amount, event_type=None, description=""):
    from .models import PointHistory
    reason = REASON_MAPPING.get(event_type, None)

    user.point += amount
    user.save()

    PointHistory.objects.create(
        user=user,
        amount=amount,
        event_type=event_type or "unspecified",
        reason=reason,
        description=description
    )
