from django.urls import path
from .views import (
    MyPostsListView, MyCommentsListView, MyLikesListView,
    DeletePostView, DeleteCommentView, DeleteLikeView
)

urlpatterns = [
    path('posts/', MyPostsListView.as_view(), name='my-posts'),
    path('comments/', MyCommentsListView.as_view(), name='my-comments'),
    path('likes/', MyLikesListView.as_view(), name='my-likes'),

    path('posts/<int:post_id>/', DeletePostView.as_view(), name='delete-post'),
    path('comments/<int:comment_id>/', DeleteCommentView.as_view(), name='delete-comment'),
    path('likes/<int:post_id>/', DeleteLikeView.as_view(), name='delete-like'),
]