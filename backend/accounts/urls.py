from django.urls import path
from .views import RegisterView, UserProfileView

urlpatterns = [
    # [توضیح]: مسیر ثبت‌نام کاربر جدید
    path('register/', RegisterView.as_view(), name='register'),

    # [توضیح]: مسیر مشاهده و ویرایش اطلاعات کاربر لاگین‌شده
    path('profile/', UserProfileView.as_view(), name='profile'),
]
