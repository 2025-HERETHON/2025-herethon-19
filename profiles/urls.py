from django.urls import path
from .views import InterestSelectionView

urlpatterns = [
    path('interests/', InterestSelectionView.as_view(), name='interest-select'),
]
