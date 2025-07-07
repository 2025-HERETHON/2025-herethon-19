from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import RecommendedMentorSerializer, MentorLikeSerializer, MentorDetailSerializer
from django.db.models import Count
from .pagination import MentorPagination
from rest_framework.generics import RetrieveAPIView
from profiles.models import MentorVerification
from django.shortcuts import get_object_or_404

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
        serializer = MentorLikeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "좋아요가 등록되었습니다."}, status=201)
        return Response(serializer.errors, status=400)
    
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