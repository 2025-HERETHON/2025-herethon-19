from django.db import transaction
from rest_framework import serializers
from django.contrib.auth import get_user_model
from profiles.models import Profile, Interest, MentorVerification

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    # password2 = serializers.CharField(write_only=True)

    # class Meta:
    #     model = User
    #     fields = ['email', 'password', 'password2', 'nickname', 'phone_number', 'user_type']

    # def validate(self, data):
    #     if data['password'] != data['password2']:
    #         raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
    #     return data

    # def create(self, validated_data):
    #     validated_data.pop('password2')
    #     password = validated_data.pop('password')
    #     user = User(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user
    
    # 비밀번호 확인용
    password2 = serializers.CharField(write_only=True)
    # 관심사
    interest_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )

    # 약관
    is_over_14 = serializers.BooleanField(required=True)
    agreed_terms = serializers.BooleanField(required=True)
    agreed_privacy = serializers.BooleanField(required=True)
    agreed_marketing = serializers.BooleanField(required=False, default=False)

    # 멘토 인증
    mentor_introduction = serializers.CharField(
        required=False, allow_blank=True, max_length=2000
    )
    mentor_document = serializers.FileField(required=False, allow_null=True)
    mentor_skip = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = (
            "email", "password", "password2",  # 비밀번호 확인용
            "nickname", "phone_number", "user_type",  # 기본 회원 정보
            "interest_ids",  # 관심사
            "is_over_14", "agreed_terms", "agreed_privacy", "agreed_marketing",  # 약관
            "mentor_introduction", "mentor_document", "mentor_skip",  # 멘토 인증
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data["password"] != data.pop("password2"):
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        if not data.get("agreed_terms") or not data.get("agreed_privacy"):
            raise serializers.ValidationError("필수 약관에 동의해야 합니다.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        # 약관, 관심사, 멘토 인증 꺼내기
        interest_ids = validated_data.pop("interest_ids", [])
        profile_kwargs = {
            "is_over_14": validated_data.pop("is_over_14"),
            "agreed_terms": validated_data.pop("agreed_terms"),
            "agreed_privacy": validated_data.pop("agreed_privacy"),
            "agreed_marketing": validated_data.pop("agreed_marketing", False),
        }
        mentor_intro = validated_data.pop("mentor_introduction", "")
        mentor_doc = validated_data.pop("mentor_document", None)
        mentor_skip = validated_data.pop("mentor_skip", False)

        # 유저 생성
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)

        # 프로필 생성
        profile = Profile.objects.create(user=user, **profile_kwargs)

        # 관심사 연결
        if interest_ids:
            interests = Interest.objects.filter(id__in=interest_ids)
            profile.interests.set(interests)

        # 멘토 인증 or 건너뛰기
        if user.user_type == "mentor":
            MentorVerification.objects.create(
                user=user,
                introduction=mentor_intro,
                document=mentor_doc,
                is_skipped=mentor_skip,
                is_verified=False
            )

        return user

    def to_representation(self, instance):
        return {
            "email": instance.email,
            "nickname": instance.nickname,
            "phone_number": instance.phone_number,
            "user_type": instance.user_type
        }

#로그인
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

#회원정보 조회 및 수정
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'nickname', 'phone_number']  # email은 read-only로도 가능

        extra_kwargs = {
            'email': {'read_only': True},  # 이메일은 수정 불가
        }


#회원탈퇴
class UserDeleteSerializer(serializers.Serializer):
    confirm = serializers.BooleanField()

    def validate_confirm(self, value):
        if not value:
            raise serializers.ValidationError("유의사항 동의가 필요합니다.")
        return value