from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import RecommendedMentorSerializer, MentorLikeSerializer

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
        ).prefetch_related('profile__interests', 'mentorverification')

        results = []
        for mentor in verified_mentors:
            mentor_interests = set(mentor.profile.interests.values_list('id', flat=True))
            mentor_categories = set(mentor.profile.interests.values_list('category', flat=True))
            
            matched_interest_count = len(my_interests & mentor_interests)
            if matched_interest_count == 0:
                continue

            intro_score = 1 if mentor.mentorverification.introduction.strip() else 0
            category_match_score = len(my_categories & mentor_categories)

            final_score = (
                matched_interest_count * 3 +
                intro_score * 1 +
                category_match_score * 2
            )

            mentor.matched_interest_count = matched_interest_count
            mentor.final_score = final_score
            results.append(mentor)

        results.sort(key=lambda x: x.final_score, reverse=True)
        serializer = RecommendedMentorSerializer(results, many=True)
        return Response(serializer.data)
    

class MentorLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MentorLikeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "좋아요가 등록되었습니다."}, status=201)
        return Response(serializer.errors, status=400)