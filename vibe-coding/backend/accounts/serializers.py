from rest_framework import serializers
from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    literary_title = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = ['display_name', 'bio', 'avatar', 'xp_points', 'current_streak', 'literary_title', 'last_activity_date']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'profile']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={'min_length': 'رمز عبور باید حداقل ۸ کاراکتر باشد.'}
    )
    display_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'display_name']

    def create(self, validated_data):
        display_name = validated_data.pop('display_name', '')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        UserProfile.objects.create(
            user=user,
            display_name=display_name or validated_data['username']
        )
        return user
