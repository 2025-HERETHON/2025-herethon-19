from rest_framework import serializers
from .models import Interest, Profile, MentorVerification
from django.contrib.auth import get_user_model

User = get_user_model()

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
    
class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name', 'category']

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
    

#멘토링 인증 API(회원가입 때 멘토 인증 건너뛰기 한 멘토만)
class MentorVerificationUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = MentorVerification
        fields = ['email', 'introduction', 'document']  

    def update(self, instance, validated_data):
        instance.introduction = validated_data.get('introduction', instance.introduction)
        instance.document = validated_data.get('document', instance.document)
        instance.is_skipped = False  # 건너뛰기 해제
        instance.is_verified = False  # 검토 후 관리자 승인 필요
        instance.save()
        return instance

    
#관심사 조회 수정
class MyInterestCombinedSerializer(serializers.ModelSerializer):
    interest_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Profile
        fields = ['interest_ids']

    def to_representation(self, instance):
        return {
            "interests": [
                {"id": interest.id, "name": interest.name, "category": interest.category}
                for interest in instance.interests.all()
            ]
        }

    def validate_interest_ids(self, value):
        if not value:
            raise serializers.ValidationError("관심사를 최소 하나 이상 선택해야 합니다.")
        if not Interest.objects.filter(id__in=value).count() == len(value):
            raise serializers.ValidationError("유효하지 않은 관심사 ID가 있습니다.")
        return value

    def update(self, instance, validated_data):
        interest_ids = validated_data.get("interest_ids")
        if interest_ids:
            interests = Interest.objects.filter(id__in=interest_ids)
            instance.interests.set(interests)
            instance.save()
        return instance

