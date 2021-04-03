from django.db import models
from apps.post.models import Post
from django.contrib.auth.models import User


class Comment(models.Model):
    context = models.CharField(max_length=200, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}: for {self.post.title} by {self.user.username}'
