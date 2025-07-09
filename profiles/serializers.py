from rest_framework import serializers
from .models import Interest, Profile, MentorVerification
from django.contrib.auth import get_user_model

#관심사
class InterestSelectionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    interest_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    def validate_interest_ids(self, value):
        if not value:
            raise serializers.ValidationError("관심사를 최소 하나 이상 선택해야 합니다.")
        if not Interest.objects.filter(id__in=value).count() == len(value):
            raise serializers.ValidationError("유효하지 않은 관심사 ID가 있습니다.")
        return value

    def save(self, **kwargs):
        email = self.validated_data['email']
        interests = Interest.objects.filter(id__in=self.validated_data['interest_ids'])

        User = get_user_model()
        user = User.objects.get(email=email)
        profile = Profile.objects.get(user=user)
        profile.interests.set(interests)
        return profile

#이용약관
class AgreementSerializer(serializers.Serializer):
    email = serializers.EmailField()
    is_over_14 = serializers.BooleanField()
    agreed_terms = serializers.BooleanField()
    agreed_privacy = serializers.BooleanField()
    agreed_marketing = serializers.BooleanField()

    def save(self, **kwargs):
        email = self.validated_data['email']
        User = get_user_model()
        user = User.objects.get(email=email)
        profile, _ = Profile.objects.get_or_create(user=user)

        profile.is_over_14 = self.validated_data['is_over_14']
        profile.agreed_terms = self.validated_data['agreed_terms']
        profile.agreed_privacy = self.validated_data['agreed_privacy']
        profile.agreed_marketing = self.validated_data['agreed_marketing']
        profile.save()
        return profile

#멘토 인증
class MentorVerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = MentorVerification
        fields = ['email', 'introduction', 'document']

    def create(self, validated_data):
        email = validated_data.pop('email')
        User = get_user_model()
        user = User.objects.get(email=email)

        #중복 방지
        verification, _ = MentorVerification.objects.update_or_create(
            user=user,
            defaults=validated_data
        )
        return verification
    
#관심사 리스트 조회
class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name', 'category']