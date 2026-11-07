from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = 'پروفایل ادبی'
    verbose_name_plural = 'پروفایل ادبی'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'date_joined')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'xp_points', 'current_streak', 'literary_title', 'last_activity_date')
    search_fields = ('user__username', 'display_name')
    list_filter = ('last_activity_date',)
