from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']
        


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={'min_length': 'رمز عبور باید حداقل ۸ کاراکتر باشد.'}
    )

    password_confirm = serializers.CharField(
        write_only=True,
        error_messages={'required': 'تکرار رمز عبور الزامی است.'}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm']

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("وارد کردن ایمیل الزامی است.")
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("کاربری با این ایمیل از قبل در سایت ثبت‌نام کرده است.")
        return value.lower()

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "رمزهای عبور واردشده با یکدیگر همخوانی ندارند."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }
        return data

