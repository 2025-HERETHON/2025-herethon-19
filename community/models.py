from django.db import models 
from django.contrib.auth import get_user_model

User = get_user_model()

class Keyword(models.Model):
    CATEGORY_CHOICES = [
        ('it', 'IT/개발'),
        ('business', '비즈니스'),
        ('creative', '창의/콘텐츠'),
        ('career', '커리어/라이프 전환'),
        ('job', '취업/이직 준비'),
        ('growth', '자기성장'),
    ]

    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="it")

    def __str__(self):
        return f"[{self.get_category_display()}] {self.name}"
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    keywords = models.ManyToManyField(Keyword, blank=True)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)  # 좋아요 누른 사람들
    
    def __str__(self):
        return self.title
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"[{self.author}] {self.content[:20]}"

