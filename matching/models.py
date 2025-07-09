from django.db import models
from django.conf import settings

# Create your models here.
class MentorLike(models.Model):
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes_received'
    )
    mentee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes_given'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mentor', 'mentee')  #중복 방지용, 	한 멘티가 한 멘토에게는 한 번만 좋아요 가능

    def __str__(self):
        return f"{self.mentee.email} → {self.mentor.email}"

class MatchingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', '진행 전'),
        ('accepted', '진행 중'),
        ('rejected', '종료'),
    ]

    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests')
    mentee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mentor', 'mentee')  #중복 요청 방지

    def __str__(self):
        return f"{self.mentee.nickname} → {self.mentor.nickname} ({self.status})"