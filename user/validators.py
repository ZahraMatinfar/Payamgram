from django.core.exceptions import ValidationError
from django.utils import timezone


def minimum_age(birthday):
    if timezone.now().year - birthday.year < 13:
        # raise ValidationError('You do not have the minimum age requirement')
        raise ValidationError('شما زیر سن قانونی برای ورود هستید.')
    else:
        return True


def password_validator(password):
    if len(password) < 8:
        raise ValidationError('too short!')

