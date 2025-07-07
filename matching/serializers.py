from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MentorLike
from profiles.models import Profile, MentorVerification
from matching.models import MentorLike

User = get_user_model()

class RecommendedMentorSerializer(serializers.ModelSerializer):
    interests = serializers.StringRelatedField(many=True, source='profile.interests')
    introduction = serializers.CharField(source='mentorverification.introduction', allow_blank=True)
    matched_interest_count = serializers.IntegerField()
    final_score = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'nickname', 'introduction', 'interests', 'matched_interest_count', 'final_score']

class MentorLikeSerializer(serializers.Serializer):
    mentor_id = serializers.IntegerField()

    def validate_mentor_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("해당 멘토가 존재하지 않습니다.")
        if user.user_type != 'mentor':
            raise serializers.ValidationError("해당 유저는 멘토가 아닙니다.")
        return value

    def create(self, validated_data):
        mentee = self.context['request'].user
        mentor = User.objects.get(id=validated_data['mentor_id'])
        like, created = MentorLike.objects.get_or_create(mentee=mentee, mentor=mentor)
        if not created:
            raise serializers.ValidationError("이미 좋아요를 누른 멘토입니다.")
        return like

class RecommendedMentorSerializer(serializers.ModelSerializer):
    interests = serializers.StringRelatedField(many=True, source='profile.interests')
    introduction = serializers.CharField(source='mentorverification.introduction', allow_blank=True)
    matched_interest_count = serializers.IntegerField()
    final_score = serializers.IntegerField()
    like_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'nickname', 'introduction', 'interests',
                  'matched_interest_count', 'like_count', 'final_score']

#멘토 매칭 상세 페이지
class MentorDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    nickname = serializers.CharField(source='user.nickname')
    interests = serializers.SerializerMethodField()
    introduction = serializers.CharField()
    document_url = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = MentorVerification
        fields = ['id', 'nickname', 'interests', 'introduction', 'document_url', 'like_count']

    def get_interests(self, obj):
        profile = Profile.objects.get(user=obj.user)
        return [interest.name for interest in profile.interests.all()]

    def get_document_url(self, obj):
        if obj.document:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.document.url)
        return None

    def get_like_count(self, obj):
        return MentorLike.objects.filter(mentor=obj.user).count()