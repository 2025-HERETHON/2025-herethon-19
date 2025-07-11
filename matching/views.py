from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import RecommendedMentorSerializer, MentorLikeSerializer, MentorDetailSerializer, MatchingRequestCreateSerializer, ReceivedRequestSerializer, MatchingResponseSerializer, MyMatchingStatusSerializer, ReviewSerializer, ReviewDetailSerializer, MyMenteeStatusSerializer, MenteeCancelMatchingSerializer, MentorCancelMatchingSerializer
from django.db.models import Count
from .pagination import MentorPagination
from rest_framework.generics import RetrieveAPIView
from profiles.models import MentorVerification
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import MatchingRequest, Review, MentorLike, ReviewViewHistory
from accounts.models import CustomUser
from rest_framework.generics import CreateAPIView
from point.utils import adjust_point

# Create your views here.

User = get_user_model()

class RecommendedMentorListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'mentee':
            return Response({"error": "멘티만 매칭 서비스를 사용할 수 있습니다."}, status=403)
    
        my_interests = set(user.profile.interests.values_list('id', flat=True))
        my_categories = set(user.profile.interests.values_list('category', flat=True))

        #인증된 멘토만 조회
        verified_mentors = User.objects.filter(
            user_type='mentor',
            mentorverification__is_verified=True
        ).prefetch_related('profile__interests', 'mentorverification'
        ).annotate(
            like_count=Count('likes_received')
        )   

        results = []
        for mentor in verified_mentors:
            mentor_interests = set(mentor.profile.interests.values_list('id', flat=True))
            mentor_categories = set(mentor.profile.interests.values_list('category', flat=True))
            
            matched_interest_count = len(my_interests & mentor_interests)
            if matched_interest_count == 0:
                continue

            intro_score = 1 if mentor.mentorverification.introduction.strip() else 0
            category_match_score = len(my_categories & mentor_categories)
            like_score = mentor.like_count * 2

            final_score = (
                matched_interest_count * 3 +
                intro_score * 1 +
                category_match_score * 2 +
                like_score
            )

            mentor.matched_interest_count = matched_interest_count
            mentor.final_score = final_score
            results.append(mentor)

        # 정렬 + 페이지네이션
        results.sort(key=lambda x: x.final_score, reverse=True)

        paginator = MentorPagination()
        page = paginator.paginate_queryset(results, request)
        serializer = RecommendedMentorSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)    

class MentorLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        mentor_id = request.data.get('mentor_id')
        if not mentor_id:
            return Response({'error': 'mentor_id는 필수입니다.'}, status=400)

        try:
            mentor = CustomUser.objects.get(id=mentor_id, user_type='mentor')
        except CustomUser.DoesNotExist:
            return Response({'error': '해당 멘토를 찾을 수 없습니다.'}, status=404)

        mentee = request.user
        if mentor == mentee:
            return Response({'error': '자기 자신에게 좋아요를 보낼 수 없습니다.'}, status=400)

        #중복 좋아요 방지
        like, created = MentorLike.objects.get_or_create(mentor=mentor, mentee=mentee)
        if not created:
            return Response({'message': '이미 좋아요를 보냈습니다.'}, status=200)

        #포인트 적립
        adjust_point(mentor, +5, 'like_received')

        return Response({'message': '좋아요가 등록되었습니다.'}, status=201)
    
#멘토 매칭 상세 페이지
class MentorDetailView(RetrieveAPIView):
    queryset = MentorVerification.objects.filter(is_verified=True)
    serializer_class = MentorDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def get_object(self):
        mentor_id = self.kwargs["mentor_id"] 
        return get_object_or_404(
            MentorVerification.objects.filter(is_verified=True),
            user__id=mentor_id
        )
    
#멘토신청
class MatchingRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MatchingRequestCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "멘토에게 요청을 보냈습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#멘토가 받은 멘티 신청 목록 조회
class ReceivedRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'mentor':
            return Response({'error': '멘토만 접근할 수 있습니다.'}, status=403)

        requests = MatchingRequest.objects.filter(mentor=user).order_by('-created_at')
        serializer = ReceivedRequestSerializer(requests, many=True)
        return Response(serializer.data)
    
#멘토가 수락/거절
class MatchingRespondView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MatchingResponseSerializer(data=request.data)
        if serializer.is_valid():
            request_obj = serializer.save()
            message = "매칭 요청을 수락했습니다." if request_obj.status == 'accepted' else "매칭 요청을 거절했습니다."
            return Response({"message": message})
        return Response(serializer.errors, status=400)
    
#멘티가 내가 신청한 멘토와의 매칭 상태 확인
class MyMatchingStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'mentee':
            return Response({"error": "멘티만 조회 가능합니다."}, status=403)

        requests = MatchingRequest.objects.filter(mentee=user).select_related('mentor')
        serializer = MyMatchingStatusSerializer(requests, many=True)
        return Response(serializer.data)
    
class ReviewCreateView(CreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()
    
#멘토가 멘티가 신청한 멘티와의 매칭 상태 확인
class MyMenteeStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.user_type != 'mentor':
            return Response({"error": "멘토만 조회 가능합니다."}, status=403)

        requests = MatchingRequest.objects.filter(mentor=user).select_related('mentee')
        serializer = MyMenteeStatusSerializer(requests, many=True)
        return Response(serializer.data)

    
#리뷰열람
class ReviewOpenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        user = request.user

        try:
            review = Review.objects.select_related('match__mentor').get(id=review_id)
        except Review.DoesNotExist:
            return Response({'error': '리뷰가 존재하지 않습니다.'}, status=404)

        if review.match.mentee == user:
            return Response({'error': '본인이 작성한 리뷰는 열람할 수 없습니다.'}, status=400)

        #열람 이력 확인
        already_viewed = ReviewViewHistory.objects.filter(user=user, review=review).exists()

        if not already_viewed:
            #포인트 차감
            if user.point < 5:
                return Response({'error': '포인트가 부족합니다.'}, status=403)

            adjust_point(
                user=user,
                amount=-5,
                event_type="review_opened",
                description=f"[리뷰 열람] {review.match.mentor.nickname} 멘토"
            )

            #열람 기록 저장
            ReviewViewHistory.objects.create(user=user, review=review)

        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data, status=200)
    
class MenteeCancelMatchingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MenteeCancelMatchingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "매칭이 종료되었습니다."}, status=200)
        return Response(serializer.errors, status=400)


class MentorCancelMatchingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MentorCancelMatchingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "매칭이 종료되었습니다."}, status=200)
        return Response(serializer.errors, status=400)