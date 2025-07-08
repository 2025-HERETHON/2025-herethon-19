# community/serializers.py
from rest_framework import serializers
from community.models import Post, Comment, Keyword

class KeywordSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display')

    class Meta:
        model = Keyword
        fields = ['id', 'name', 'category']

class PostSerializer(serializers.ModelSerializer):
    keywords = KeywordSerializer(many=True, read_only=True)
    content_preview = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content_preview', 'created_at', 'keywords']

    def get_content_preview(self, obj):
        return obj.content[:100]

class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='post.id', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    content_preview = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'post_title', 'content_preview', 'created_at']

    def get_content_preview(self, obj):
        return obj.content[:100]
