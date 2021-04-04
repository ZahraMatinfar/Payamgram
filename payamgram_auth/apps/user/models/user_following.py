from django.db import models

from apps.user.models import User
from payamgram_auth import settings


class UserFollowing(models.Model):
    """
    a model for implementation of following system.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="follower", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="followings", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} follows {self.following_user.username}'
