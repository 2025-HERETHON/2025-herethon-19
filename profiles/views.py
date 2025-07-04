from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import InterestSelectionSerializer, AgreementSerializer

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