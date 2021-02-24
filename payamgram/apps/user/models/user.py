from django.db import models

from apps.user.manager import UserPosts
from apps.user.validators import minimum_age
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse


class User(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=['username'])
    username = models.CharField(primary_key=True, max_length=100, unique=True)
    birthday = models.DateField(validators=[minimum_age])

    # image for profile
    objects = UserPosts()
    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse('user_detail', args=[(self.username)])
