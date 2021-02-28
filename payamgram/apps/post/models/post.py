from django.db import models

# Create your models here.
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField

from apps.user.models import User


class Post(models.Model):
    title = models.CharField(max_length=50)
    caption = models.TextField()
    published_date = models.DateTimeField(editable=False, auto_now_add=True)
    slug = AutoSlugField(populate_from=['title'], unique=True, allow_unicode=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # Without auth , we need to find out who is creating a post . This field help us.
    user_slug = AutoSlugField(populate_from=['user'])
    likes = models.ManyToManyField(User, related_name='likes', default=None)

    def __str__(self):
        return f'{self.id} : {self.title} published at {self.published_date}'

    @property
    def age(self):
        """
        :return: age of a post .Indicates how much time has passed since the post was sent
        """
        return timezone.now() - self.published_date
