from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model, authenticate, logout
from .serializers import SignupSerializer, LoginSerializer, UserUpdateSerializer, UserDeleteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import PasswordResetRequestForm, SetNewPasswordForm
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse

from matching.models import MatchingRequest

User = get_user_model()

# Create your views here.
class SignupView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = SignupSerializer

#로그인
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }, status=status.HTTP_200_OK)
            return Response({"error": "이메일 또는 비밀번호가 올바르지 않습니다."},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#비밀번호 재설정 요청
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = request.build_absolute_uri(f"/accounts/password-reset/{uid}/{token}/")
                send_mail(
                    '비밀번호 재설정 링크입니다',
                    f'아래 링크를 눌러 비밀번호를 재설정하세요:\n{reset_link}',
                    'hopeu5561@gmail.com',
                    [email],
                )
                return render(request, 'password_reset_sent.html')
            except User.DoesNotExist:
                form.add_error('email', '해당 이메일로 가입된 계정이 없습니다.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'password_reset_form.html', {'form': form})

#비밀번호 재설정 확인
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                return render(request, 'password_reset_complete.html')
        else:
            form = SetNewPasswordForm()
        return render(request, 'set_new_password.html', {'form': form})
    else:
        return render(request, 'password_reset_invalid.html')

#테스트
def test_email(request):
    send_mail(
        '테스트 메일 제목입니다.',
        '이것은 테스트 메일 본문입니다.',
        'hopeu5561@gmail.com',  # 보내는 사람
        ['asgvcx@naver.com'],  # 받는 사람
        fail_silently=False,
    )
    return HttpResponse("이메일이 전송되었습니다.")

#로그아웃
def logout_api_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': '로그아웃 성공'}, status=200)
    return JsonResponse({'error': '잘못된 요청'}, status=400)

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if refresh_token is None:
            return Response({"error": "Refresh 토큰이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  
            return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"error": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)
        

#회원정보 수정
class UserInfoUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserUpdateSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원정보가 수정되었습니다.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#회원탈퇴
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = UserDeleteSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user

            #매칭요청 상태 모두 'rejected' 처리
            MatchingRequest.objects.filter(mentor=user).update(status='rejected')
            MatchingRequest.objects.filter(mentee=user).update(status='rejected')

            #유저 소프트 삭제
            user.is_active = False
            user.save()

            return Response({"message": "회원 탈퇴가 완료되었고, 관련 매칭 요청이 모두 종료 처리되었습니다."},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)