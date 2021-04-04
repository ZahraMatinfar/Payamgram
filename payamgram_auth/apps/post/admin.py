from django.contrib import admin
from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    registered Post
    """
    list_display = ['id', 'title', 'slug', 'user']
    readonly_fields = ['published_date', 'slug']
    list_display_links = ['id', 'title']
    search_fields = ['image']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    registered Comment
    """
    list_display = ['id', 'user', 'post']
