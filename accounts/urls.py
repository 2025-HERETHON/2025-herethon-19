from django.urls import path
from .views import SignupView, LoginView, test_email, logout_api_view, LogoutView, UserInfoUpdateView, UserDeleteView
from . import views

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('test-email/', test_email, name='test_email'),
    #path('logout/', logout_api_view, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user-info/', UserInfoUpdateView.as_view(), name='user-info'),
    path('delete/', UserDeleteView.as_view(), name='user-delete'),  # 회원 탈퇴
]