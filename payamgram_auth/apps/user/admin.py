from django.contrib import admin
from apps.user.models import UserFollowing, Profile, User


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'username']
    list_display_links = ['email']
    readonly_fields = ['key']
    inlines = (ProfileInline,)


@admin.register(UserFollowing)
class UserFollow(admin.ModelAdmin):
    list_display = ['id', 'user', 'following_user']
