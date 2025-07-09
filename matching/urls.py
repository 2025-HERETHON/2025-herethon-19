from django.urls import path
from .views import RecommendedMentorListView, MentorLikeView, MentorDetailView, MatchingRequestCreateView, ReceivedRequestListView, MatchingRespondView

urlpatterns = [
    path('recommend/', RecommendedMentorListView.as_view(), name='recommended-mentors'),
    path('like/', MentorLikeView.as_view(), name='mentor-like'),
    path('mentors/<int:mentor_id>/', MentorDetailView.as_view(), name='mentor-detail'),
    path('request/', MatchingRequestCreateView.as_view(), name='matching-request-create'),#멘토 신청
    path('requests/', ReceivedRequestListView.as_view(), name='received-request-list'),#멘토가 받은 멘티 신청 목록 조회
    path('respond/', MatchingRespondView.as_view(), name='matching-respond'),#멘토가 수락/거절

]
