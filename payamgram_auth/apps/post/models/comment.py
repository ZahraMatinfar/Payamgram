from django.db import models
from apps.post.models import Post
from payamgram_auth import settings


class Comment(models.Model):
    """
    Each text is sent by one person to a post.
    """
    context = models.CharField(max_length=200, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}: for {self.post.title} '
