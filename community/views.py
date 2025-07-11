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
from point.models import PointHistory
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.authentication import JWTAuthentication

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
class CommentCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        # Post 존재 여부 확인
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound("Post not found")
        return Comment.objects.filter(post=post).order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)
        # 댓글 수 갱신
        post.comment_count = post.comment_set.count()
        post.save()

# 좋아요 토글
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    author = post.author

    if user in post.likes.all():
        post.likes.remove(user)
        post.like_count = post.likes.count()
        post.save()
        return Response({"message": "좋아요 취소", "liked": False})
    else:
        post.likes.add(user)
        post.like_count = post.likes.count()
        post.save()

        # 자기 글이 아니면 포인트 지급
        if user != author:
            author.point += 5
            author.save()

            PointHistory.objects.create(
                user=author,
                amount=5,
                reason='community_like_received',
                event_type='like',
                description=f"{user.nickname}님이 '{post.title}'에 좋아요를 눌렀습니다."
            )

        return Response({"message": "좋아요", "liked": True})