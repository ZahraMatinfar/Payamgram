from django.db import models
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField

from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=50)
    caption = models.TextField()
    published_date = models.DateTimeField(editable=False, auto_now_add=True)
    slug = AutoSlugField(populate_from=['title'], unique=True, allow_unicode=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', default=None)

    # likes = models.ForeignKey(User, related_name='likes', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f'{self.id} : {self.title} published at {self.published_date}'

    @property
    def age(self):
        """
        :return: age of a post .Indicates how much time has passed since the post was sent
        """
        return timezone.now() - self.published_date

    class Meta:
        # ordering = ['-published_date']
        ordering = ['-published_date__year', '-published_date__day', '-published_date__hour', '-published_date__minute']
