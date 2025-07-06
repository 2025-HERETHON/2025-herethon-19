from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostCreateSerializer, PostSerializer
from rest_framework.generics import RetrieveAPIView
from .models import Post, Comment
from .serializers import PostDetailSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data, context={'author': request.user})
        if serializer.is_valid():
            post = serializer.save()
            result_serializer = PostSerializer(post)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 상세 조회
class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

# 댓글 작성
class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            post.comment_count = post.comment_set.count()
            post.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# 좋아요 토글
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        post.like_count = post.likes.count()
        post.save()
        return Response({"message": "좋아요 취소", "liked": False})
    else:
        post.likes.add(user)
        post.like_count = post.likes.count()
        post.save()
        return Response({"message": "좋아요", "liked": True})