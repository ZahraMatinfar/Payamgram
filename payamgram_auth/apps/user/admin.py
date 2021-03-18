from django.contrib import admin
# from apps.user.models import UserFollowing, Profile, Request
from apps.user.models import UserFollowing, Profile, User


# from apps.user.models import  Profile


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'username']
    list_display_links = ['email']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(UserFollowing)
class UserFollow(admin.ModelAdmin):
    list_display = ['id', 'user', 'following_user']

# @admin.register(Request)
# class UserFollow(admin.ModelAdmin):
#     list_display = ['id']
