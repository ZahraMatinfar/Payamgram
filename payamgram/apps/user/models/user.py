# from hashlib import sha256
from hashlib import sha256

from django.db import models


from django_extensions.db.fields import AutoSlugField

from apps.user.manager import UserManager
from apps.user.validators import minimum_age


class User(models.Model):
    username = models.CharField(max_length=100, unique=True, primary_key=True)
    password = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=['username'])
    email = models.EmailField(max_length=200)
    birthday = models.DateField(validators=[minimum_age])
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    login = models.BooleanField(default=False)
    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.password = sha256(self.password.encode('utf-8')).hexdigest()
        return super().save(*args, **kwargs)