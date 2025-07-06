from rest_framework import serializers
from .models import Post, Keyword

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    keywords = KeywordSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'keywords',
            'content',
            'like_count',
            'comment_count',
            'created_at',
            'author',
        ]
