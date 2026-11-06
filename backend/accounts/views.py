from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    [توضیح]: اندپوینت ثبت‌نام کاربر جدید
    [آموزشی]: از AllowAny استفاده می‌کنیم چون کاربری که هنوز ثبت‌نام نکرده مهمان است و نباید برای ثبت‌نام نیاز به لاگین داشته باشد.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    [توضیح]: اندپوینت مشاهده و ویرایش مشخصات کاربر لاگین‌شده
    [آموزشی]: به جای دریافت id در آدرس، از self.request.user استفاده می‌کنیم تا هر کاربر فقط به اطلاعات خودش دسترسی داشته باشد.
    [آموزشی]: دسترسی IsAuthenticated یعنی فقط کاربری که توکن معتبر ارسال کرده مجاز به دیدن این بخش است.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # [توضیح]: برگرداندن کاربری که لاگین کرده است
        return self.request.user
