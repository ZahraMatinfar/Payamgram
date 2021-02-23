from django.db import models

# Create your models here.
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField

from apps.user.models import User


class Post(models.Model):
    title = models.CharField(max_length=50)
    caption = models.TextField()
    published_date = models.DateTimeField(editable=False)
    slug = AutoSlugField(populate_from=['title'], unique=True, allow_unicode=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.id} : {self.title} published at {self.published_date}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.published_date = timezone.now()
        return super().save(*args, **kwargs)

    @property
    def age(self):
        return timezone.now() - self.published_date
