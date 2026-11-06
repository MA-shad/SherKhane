from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    [توضیح]: سریالایزر برای نمایش اطلاعات عمومی کاربر
    [آموزشی]: فرانت‌اند از این فیلدها استفاده می‌کنه تا نام کاربر و تاریخ عضویت رو توی نوبار و صفحه پروفایل نشون بده.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    """
    [توضیح]: سریالایزر ثبت‌نام کاربر جدید با اعتبارسنجی رمز
    [آموزشی]: فیلد password دارای write_only=True است تا رمز عبور در پاسخ سرور (JSON) بازگردانده نشود و امنیت حفظ شود.
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            'min_length': 'رمز عبور باید حداقل ۸ کاراکتر باشد.'
        }
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # [توضیح]: ساخت کاربر با متد استاندارد جنگو
        # [آموزشی]: حتماً از create_user استفاده می‌کنیم تا رمز عبور به صورت خودکار با الگوریتم PBKDF2 هش شود، نه متن خام.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
