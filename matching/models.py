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