from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import InterestSelectionSerializer, AgreementSerializer, MentorVerificationSerializer
from rest_framework.parsers import MultiPartParser, FormParser

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
    parser_classes = [MultiPartParser, FormParser]  # 파일 업로드
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MentorVerificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "멘토 인증 정보가 저장되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)