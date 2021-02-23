from django.db import models
from apps.user.validators import minimum_age
from django_extensions.db.fields import AutoSlugField


class User(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=['username'])
    username = models.CharField(primary_key=True,max_length=100, unique=True)
    birthday = models.DateField(validators=[minimum_age])

    # image for profile

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
