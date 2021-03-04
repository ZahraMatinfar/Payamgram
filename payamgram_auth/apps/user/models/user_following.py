from django.db import models

from django.contrib.auth.models import User


class UserFollowing(models.Model):
    user = models.ForeignKey(User, related_name="follower", on_delete=models.DO_NOTHING)
    following_user = models.ForeignKey(User, related_name="followings", on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} follows {self.following_user.username}'
