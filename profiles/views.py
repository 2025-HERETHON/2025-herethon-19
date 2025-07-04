from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import InterestSelectionSerializer, AgreementSerializer, MentorVerificationSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from .models import MentorVerification
from django.contrib.auth import get_user_model
# Create your views here.
#관심사
class InterestSelectionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InterestSelectionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "관심사가 저장되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#약관동의
class AgreementView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AgreementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "약관 동의가 저장되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#멘토인증
class MentorVerificationView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MentorVerificationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "멘토 인증이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#건너뛰기
User = get_user_model()

@api_view(['POST'])
def skip_mentor_verification(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "이메일이 필요합니다."}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "해당 이메일로 가입된 사용자가 없습니다."}, status=404)

    if MentorVerification.objects.filter(user=user).exists():
        return Response({"error": "이미 멘토 인증 정보를 제출한 사용자입니다."}, status=400)

    MentorVerification.objects.create(user=user, is_skipped=True)
    return Response({"message": "멘토 인증 건너뛰기 완료"}, status=200)