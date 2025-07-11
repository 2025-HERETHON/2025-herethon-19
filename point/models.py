from django.db import models
from django.conf import settings

# Create your models here.

class PointHistory(models.Model):
    REASON_CHOICES = [
        ('like_received', '좋아요 받음'),
        ('match_request_received', '멘토링 요청 받음'),
        ('review_written', '리뷰 작성'),
        ('review_opened', '리뷰 열람'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()
    event_type = models.CharField(max_length=50, default='unspecified')
    description = models.TextField(blank=True)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.nickname} | {self.amount:+}P | {self.get_reason_display()}"
    

#리뷰열람여부
class ReviewAccessLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey('matching.Review', on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')  #하나의 리뷰에 대해 한 번만 접근 기록 가능