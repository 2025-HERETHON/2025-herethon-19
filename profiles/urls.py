from django.urls import path
from .views import InterestSelectionView, AgreementView

urlpatterns = [
    path('interests/', InterestSelectionView.as_view(), name='interest-select'),
    path('agreements/', AgreementView.as_view(), name='agreement'),
]
