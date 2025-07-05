from django.db import models
from django.conf import settings

# Create your models here.
class Interest(models.Model):
    CATEGORY_CHOICES = [
        ('it', 'IT/개발'),
        ('business', '비즈니스'),
        ('creative', '창의/콘텐츠'),
        ('career', '커리어/라이프 전환'),
        ('job', '취업/이직 준비'),
        ('growth', '자기성장'),
    ]

    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    interests = models.ManyToManyField(Interest, blank=True)

    # 약관 동의 필드 추가
    agreed_terms = models.BooleanField(default=False)
    is_over_14 = models.BooleanField(default=False)
    agreed_privacy = models.BooleanField(default=False)
    agreed_marketing = models.BooleanField(default=False)

#멘토 인증
class MentorVerification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    introduction = models.TextField(blank=True)
    document = models.FileField(upload_to='mentor_docs/', blank=True, null=True)  
    is_verified = models.BooleanField(default=False)#관리자가 True로 설정해야지 멘토 인증 완료

    is_skipped = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - Mentor Verification"
