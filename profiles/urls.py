from django.urls import path
from .views import InterestSelectionView, AgreementView, MentorVerificationView, skip_mentor_verification

urlpatterns = [
    path('interests/', InterestSelectionView.as_view(), name='interest-select'),
    path('agreements/', AgreementView.as_view(), name='agreement'),
    path('mentor-verification/', MentorVerificationView.as_view(), name='mentor-verification'),
    path('mentor-verification/skip/', skip_mentor_verification, name='skip_mentor_verification'),
]
