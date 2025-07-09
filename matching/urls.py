from django.urls import path
from .views import RecommendedMentorListView, MentorLikeView, MentorDetailView, MatchingRequestCreateView

urlpatterns = [
    path('recommend/', RecommendedMentorListView.as_view(), name='recommended-mentors'),
    path('like/', MentorLikeView.as_view(), name='mentor-like'),
    path('mentors/<int:mentor_id>/', MentorDetailView.as_view(), name='mentor-detail'),
    path('request/', MatchingRequestCreateView.as_view(), name='matching-request-create'),
]
