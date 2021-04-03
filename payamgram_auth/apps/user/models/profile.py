import os
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from apps.user.managers import UserManager
from apps.user.validators import UnicodeUsernameValidator, mobile_validator, mobile_len_validator
from payamgram_auth import settings


def get_upload_path(instance, filename):
    """
    :return: Specifies the location of the image of a profile
    """
    return os.path.join(f'profiles/{instance.user.username}', filename)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField("email address", unique=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    slug = AutoSlugField(populate_from=['username'], unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    mobile = models.CharField(max_length=13, validators=[mobile_validator, mobile_len_validator], unique=True)
    key = models.CharField(max_length=100, null=True, blank=True, editable=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    """
    A string describing the name of the field on the user model that is used as the unique identifier
    """
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        app_label = 'user'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def full_name(self):
        return self.get_full_name()


class Profile(models.Model):
    GENDERS = [('M', 'Male'), ('F', 'Female')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='target',
                                primary_key=True)
    bio = models.TextField(blank=True)
    gender = models.CharField('gender', choices=GENDERS, max_length=1, blank=True)
    url = models.URLField(blank=True)
    requests = models.ManyToManyField(User, related_name='request', blank=True)
    image = models.ImageField(upload_to=get_upload_path, blank=True, default='profile.svg')

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        self.image.delete(False)
