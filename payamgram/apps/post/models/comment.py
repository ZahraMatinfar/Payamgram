from django.db import models

from apps.post.models import Post
from apps.user.models import User


class Comment(models.Model):
    context = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.id}: for {self.post.title} by {self.user.username}'
