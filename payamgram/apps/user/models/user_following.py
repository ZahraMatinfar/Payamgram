from django.db import models

from apps.user.models import User


class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name="following", on_delete=models.DO_NOTHING)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id.username} follows {self.following_user_id.username}'
