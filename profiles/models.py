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