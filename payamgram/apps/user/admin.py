from django.contrib import admin

from apps.user.models import User
from apps.user.models import UserFollowing


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    list_display_links = ['username']
    readonly_fields = ['login']


@admin.register(UserFollowing)
class UserFollow(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'following_user_id']
