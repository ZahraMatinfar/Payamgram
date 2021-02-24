from django.contrib import admin

# Register your models here.
from apps.post.models.post import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    readonly_fields = ['published_date', 'slug', 'user_slug']
    list_display_links = ['id', 'title']
