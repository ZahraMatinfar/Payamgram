from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    GENDERS = [('M', 'Male'), ('F', 'Female')]
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile', primary_key=True)
    bio = models.TextField(blank=True)
    gender = models.CharField('gender', choices=GENDERS, max_length=1, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return f'{self.user.username}'
    # User.email = models.EmailField(blank=False)
