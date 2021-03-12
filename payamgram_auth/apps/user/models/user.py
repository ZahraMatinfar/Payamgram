from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _

from apps.user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    slug = AutoSlugField(populate_from=['email'], unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        app_label = 'user'

    # def get_full_name(self):
    #     full_name = '%s %s' % (self.first_name, self.last_name)
    #     return full_name.strip()
    #
    # def get_short_name(self):
    #     return self.first_name
