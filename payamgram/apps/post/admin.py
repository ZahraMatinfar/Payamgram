from django.contrib import admin

# Register your models here.
from apps.post.models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    readonly_fields = ['published_date', 'slug', 'user_slug']
    list_display_links = ['id', 'title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post']
