from django.urls import path
from .views import InterestSelectionView, AgreementView, MentorVerificationView, skip_mentor_verification, MentorVerificationApproveView, InterestListView, MyProfileSimpleView, MentorVerificationUpdateView

urlpatterns = [
    path('interests/', InterestSelectionView.as_view(), name='interest-select'),
    path('interests/list/', InterestListView.as_view(), name='interest-list'),
    path('agreements/', AgreementView.as_view(), name='agreement'),
    path('mentor-verification/', MentorVerificationView.as_view(), name='mentor-verification'),
    path('mentor-verification/skip/', skip_mentor_verification, name='skip_mentor_verification'),
    path('mentor-verification/<int:user_id>/verify/', MentorVerificationApproveView.as_view()),
    path('profile/me/', MyProfileSimpleView.as_view(), name='my-profile-simple'),
    path('mentor-verification/update/', MentorVerificationUpdateView.as_view(), name='mentor-verification-update'),

]
