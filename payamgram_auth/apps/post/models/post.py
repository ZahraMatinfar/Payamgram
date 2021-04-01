import os
from django.db import models
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField
from payamgram_auth import settings


def get_upload_path(instance, filename):
    return os.path.join(f'posts/{instance.user.id}', filename)


class Post(models.Model):
    title = models.CharField(max_length=50)
    caption = models.TextField(blank=True)
    published_date = models.DateTimeField(editable=False, auto_now_add=True)
    slug = AutoSlugField(populate_from=['title'], unique=True, allow_unicode=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', default=None, blank=True)
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return f'{self.id} : {self.title} published at {self.published_date}'

    @property
    def age(self):
        """
        :return: age of a post .Indicates how much time has passed since the post was sent
        """
        return timezone.now() - self.published_date

    class Meta:
        ordering = ['-published_date__year', '-published_date__day', '-published_date__hour',
                    '-published_date__minute', '-published_date__second']

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        # print(self.image.path)
        self.image.delete(False)
