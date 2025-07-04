from django.urls import path
from .views import InterestSelectionView, AgreementView, MentorVerificationView

urlpatterns = [
    path('interests/', InterestSelectionView.as_view(), name='interest-select'),
    path('agreements/', AgreementView.as_view(), name='agreement'),
    path('mentor-verification/', MentorVerificationView.as_view(), name='mentor-verification'),
]
