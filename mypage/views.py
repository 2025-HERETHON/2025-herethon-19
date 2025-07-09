# community/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from community.models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

from rest_framework.permissions import IsAuthenticated
from matching.models import MatchingRequest

# 페이지네이션 클래스 정의 (페이지당 3개)
class SmallResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10

# 내가 쓴 게시물 리스트 조회
class MyPostsListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_at')

# 내가 쓴 댓글 리스트 조회 (페이지당 10개)
class MyCommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 댓글 페이지네이션 따로 지정 (10개씩)
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user).order_by('-created_at')

# 내가 좋아요 누른 글 리스트 조회 (페이지당 3개)
class MyLikesListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        return self.request.user.liked_posts.all().order_by('-created_at')

# 삭제 API 구현

class DeletePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id, author=request.user)
            post.delete()
            return Response({'result': 'success'})
        except Post.DoesNotExist:
            return Response({'result': 'error', 'message': 'Post not found or no permission'}, status=status.HTTP_404_NOT_FOUND)

class DeleteCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
            comment.delete()
            return Response({'result': 'success'})
        except Comment.DoesNotExist:
            return Response({'result': 'error', 'message': 'Comment not found or no permission'}, status=status.HTTP_404_NOT_FOUND)

class DeleteLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            user = request.user
            if user in post.likes.all():
                post.likes.remove(user)
                post.like_count = post.likes.count()
                post.save()
                return Response({'result': 'success'})
            else:
                return Response({'result': 'error', 'message': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'result': 'error', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

#매칭된 멘토/멘티 리스트 조회
class MyMentorOrMenteeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.user_type == "mentor":
            # 멘토 → 매칭된 멘티들
            mentees = MatchingRequest.objects.filter(
                mentor=user, status="accepted"
            ).select_related('mentee')
            mentee_nicknames = [m.mentee.nickname for m in mentees]
            return Response({"my_mentees": mentee_nicknames})

        else:
            # 멘티 → 매칭된 멘토들
            mentors = MatchingRequest.objects.filter(
                mentee=user, status="accepted"
            ).select_related('mentor')
            mentor_nicknames = [m.mentor.nickname for m in mentors]
            return Response({"my_mentors": mentor_nicknames})