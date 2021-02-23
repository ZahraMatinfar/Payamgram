from django.core.exceptions import ValidationError
from django.utils import timezone


def minimum_age(birthday_year):
    if timezone.now().year - birthday_year.year < 13:
        raise ValidationError('You do not have the minimum age requirement')