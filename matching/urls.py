from django.urls import path
from .views import RecommendedMentorListView

urlpatterns = [
    path('recommend/', RecommendedMentorListView.as_view(), name='recommended-mentors'),
]
