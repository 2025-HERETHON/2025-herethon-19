from django.urls import path
from .views import RecommendedMentorListView, MentorLikeView, MentorDetailView, MatchingRequestCreateView, ReceivedRequestListView, MatchingRespondView, MyMatchingStatusView, ReviewCreateView, ReviewOpenView, MyMenteeStatusView, MenteeCancelMatchingView, MentorCancelMatchingView

urlpatterns = [
    path('recommend/', RecommendedMentorListView.as_view(), name='recommended-mentors'),
    path('like/', MentorLikeView.as_view(), name='mentor-like'),
    path('mentors/<int:mentor_id>/', MentorDetailView.as_view(), name='mentor-detail'),
    path('request/', MatchingRequestCreateView.as_view(), name='matching-request-create'),#멘토 신청
    path('requests/', ReceivedRequestListView.as_view(), name='received-request-list'),#멘토가 받은 멘티 신청 목록 조회
    path('respond/', MatchingRespondView.as_view(), name='matching-respond'),#멘토가 수락/거절
    path('my-matches/', MyMatchingStatusView.as_view(), name='my-matching-status'),#매칭상태확인(멘티입장)
    path('matching-status/mentee/', MyMenteeStatusView.as_view(), name='my_mentee_status'),#매칭상태확인(멘토입장)
    path('review/<int:match_id>/', ReviewCreateView.as_view(), name='review-create'),
    path('review/<int:review_id>/open/', ReviewOpenView.as_view(), name='review-open'),
    path('cancel/mentee/', MenteeCancelMatchingView.as_view()),
    path('cancel/mentor/', MentorCancelMatchingView.as_view()),
]
