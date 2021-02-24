from django.db import models


class UserPosts(models.Manager):  # list of posts for each user

    def get_post_user(self):
        return [user for user in self.all() if user.post_set.all()]
