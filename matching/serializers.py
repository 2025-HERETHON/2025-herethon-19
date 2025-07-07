from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RecommendedMentorSerializer(serializers.ModelSerializer):
    interests = serializers.StringRelatedField(many=True, source='profile.interests')
    introduction = serializers.CharField(source='mentorverification.introduction', allow_blank=True)
    matched_interest_count = serializers.IntegerField()
    final_score = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'nickname', 'introduction', 'interests', 'matched_interest_count', 'final_score']
