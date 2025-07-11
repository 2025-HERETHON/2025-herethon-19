from django.contrib import admin
from .models import Post, Keyword, Comment

admin.site.register(Post)
admin.site.register(Keyword)

admin.site.register(Comment)