from rest_framework import serializers
from .models import Interest, Profile
from django.contrib.auth import get_user_model

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
