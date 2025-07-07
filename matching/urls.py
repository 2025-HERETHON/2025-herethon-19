from django.urls import path
from .views import RecommendedMentorListView, MentorLikeView, MentorDetailView

urlpatterns = [
    path('recommend/', RecommendedMentorListView.as_view(), name='recommended-mentors'),
    path('like/', MentorLikeView.as_view(), name='mentor-like'),
    path('mentors/<int:pk>/', MentorDetailView.as_view(), name='mentor-detail'),
]
