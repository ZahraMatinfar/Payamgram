from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    GENDERS = [('M', 'Male'), ('F', 'Female')]
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='target', primary_key=True)
    bio = models.TextField(blank=True)
    gender = models.CharField('gender', choices=GENDERS, max_length=1, blank=True)
    url = models.URLField(blank=True)
    mobile = models.CharField(max_length=13, blank=True)
    requests = models.ManyToManyField(User, related_name='request', blank=True)
    image = models.ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return f'{self.user.username}'
    # User.email = models.EmailField(blank=False)
