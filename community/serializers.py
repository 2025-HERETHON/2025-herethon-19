from rest_framework import serializers
from .models import Post, Keyword,Comment

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'name', 'category']  # category 필드 있으면 포함, 없으면 빼도 됨

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

class PostCreateSerializer(serializers.ModelSerializer):
    keywords = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'keywords']

    def create(self, validated_data):
        keywords_data = validated_data.pop('keywords')
        user = self.context['request'].user  # author는 뷰에서 전달받는 대신 여기서 받는 게 안전
        post = Post.objects.create(author=user, **validated_data)

        for keyword_name in keywords_data:
            keyword, created = Keyword.objects.get_or_create(name=keyword_name)
            post.keywords.add(keyword)

        return post
    
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']

class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    keywords = KeywordSerializer(many=True, read_only=True)
    comments = CommentSerializer(source='comment_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author',
            'created_at', 'like_count', 'comment_count',
            'keywords', 'comments',
        ]

