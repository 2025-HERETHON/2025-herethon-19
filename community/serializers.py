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


# 등록용 serializer (write용)
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
        # author는 뷰에서 추가로 넘겨줌
        post = Post.objects.create(**validated_data)

        for keyword_name in keywords_data:
            keyword, created = Keyword.objects.get_or_create(name=keyword_name)
            post.keywords.add(keyword)

        return post