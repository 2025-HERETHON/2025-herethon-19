from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MentorLike, MatchingRequest
from profiles.models import Profile, MentorVerification
from matching.models import MentorLike, Review
from point.utils import adjust_point

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
    
#멘토 신청
class MatchingRequestCreateSerializer(serializers.ModelSerializer):
    mentor_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MatchingRequest
        fields = ['mentor_id']

    def validate_mentor_id(self, value):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(id=value, user_type='mentor').exists():
            raise serializers.ValidationError("존재하지 않는 멘토입니다.")
        return value

    def create(self, validated_data):
        mentee = self.context['request'].user
        mentor_id = validated_data['mentor_id']

        #중복 신청 방지
        if MatchingRequest.objects.filter(mentee=mentee, mentor_id=mentor_id).exists():
            raise serializers.ValidationError("이미 해당 멘토에게 요청을 보냈습니다.")

        return MatchingRequest.objects.create(
            mentee=mentee,
            mentor_id=mentor_id,
            status='pending'
        )

#멘토가 받은 멘티 신청 목록 조회
class ReceivedRequestSerializer(serializers.ModelSerializer):
    mentee_nickname = serializers.CharField(source='mentee.nickname')

    class Meta:
        model = MatchingRequest
        fields = ['id', 'mentee_nickname', 'created_at', 'status']

#멘토가 수락/거절
class MatchingResponseSerializer(serializers.Serializer):
    request_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=['accept', 'reject'])

    def validate(self, data):
        try:
            request_obj = MatchingRequest.objects.get(id=data['request_id'])
        except MatchingRequest.DoesNotExist:
            raise serializers.ValidationError("해당 매칭 요청이 존재하지 않습니다.")
        if request_obj.status != 'pending':
            raise serializers.ValidationError("이미 처리된 요청입니다.")
        return data

    def save(self, **kwargs):
        request_obj = MatchingRequest.objects.get(id=self.validated_data['request_id'])
        action = self.validated_data['action']
        request_obj.status = 'accepted' if action == 'accept' else 'rejected'
        request_obj.save()
        return request_obj
    
#멘티가 내가 신청한 멘토와의 매칭 상태 확인
class MyMatchingStatusSerializer(serializers.ModelSerializer):
    mentor_nickname = serializers.CharField(source='mentor.nickname')
    mentor_email = serializers.SerializerMethodField()
    mentor_phone = serializers.SerializerMethodField()

    class Meta:
        model = MatchingRequest
        fields = ['id', 'mentor_nickname', 'status', 'mentor_email', 'mentor_phone']

    def get_mentor_email(self, obj):
        if obj.status == 'accepted':
            return obj.mentor.email
        return None

    def get_mentor_phone(self, obj):
        if obj.status == 'accepted':
            return obj.mentor.phone_number  
        return None
    
#멘토가 멘티가 신청한 멘티와의 매칭 상태 확인
class MyMenteeStatusSerializer(serializers.ModelSerializer):
    mentee_nickname = serializers.CharField(source='mentee.nickname')
    mentee_email = serializers.SerializerMethodField()
    mentee_phone = serializers.SerializerMethodField()

    class Meta:
        model = MatchingRequest
        fields = ['id', 'mentee_nickname', 'status', 'mentee_email', 'mentee_phone']

    def get_mentee_email(self, obj):
        if obj.status == 'accepted':
            return obj.mentee.email
        return None

    def get_mentee_phone(self, obj):
        if obj.status == 'accepted':
            return obj.mentee.phone_number
        return None

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'created_at']

    def validate(self, data):
        request = self.context['request']
        match_id = self.context['view'].kwargs.get('match_id')
        try:
            match = MatchingRequest.objects.get(id=match_id, mentee=request.user)
        except MatchingRequest.DoesNotExist:
            raise serializers.ValidationError("해당 매칭을 찾을 수 없습니다.")

        if match.status != 'accepted':
            raise serializers.ValidationError("매칭이 수락된 상태에서만 리뷰 작성이 가능합니다.")

        if Review.objects.filter(match=match).exists():
            raise serializers.ValidationError("이미 리뷰를 작성하셨습니다.")

        return data

    def create(self, validated_data):
        request = self.context['request']
        match_id = self.context['view'].kwargs.get('match_id')
        match = MatchingRequest.objects.get(id=match_id)

        #리뷰 생성되면
        review = Review.objects.create(match=match, **validated_data)

        #해당 멘토에게 포인트 적립
        adjust_point(
            user=match.mentor,
            amount=5,
            event_type="review_received",
            description="멘티로부터 리뷰를 받았습니다."
        )

         #리뷰 작성자(멘티)에게 포인트 적립
        adjust_point(
            user=request.user,
            amount=5,
            event_type='review_written',
            description='멘토에게 리뷰를 작성했습니다.'
        )

        return review
    
#리뷰열람
class ReviewDetailSerializer(serializers.ModelSerializer):
    mentor_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'created_at', 'mentor_nickname']

    def get_mentor_nickname(self, obj):
        return obj.match.mentor.nickname