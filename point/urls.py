from django.urls import path
from .views import PointHistoryView

urlpatterns = [
    path('history/', PointHistoryView.as_view(), name='point-history'),
]