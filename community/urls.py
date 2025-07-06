from django.urls import path
from .views import PostListView, PostCreateAPIView, PostDetailView, toggle_like, CommentCreateView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateAPIView.as_view(), name='post-create'),
     path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/like/', toggle_like, name='post-like'),
    path('posts/<int:post_id>/comments/', CommentCreateView.as_view(), name='post-comment'),
]