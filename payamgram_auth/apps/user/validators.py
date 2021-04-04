import re
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = _(
        'Enter a valid username. This value may contain only English letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = re.ASCII


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = 0


def mobile_validator(mobile):
    """
    validator for check mobile start number.
    """
    if mobile[0:4] != '+989':
        raise ValidationError('Invalid mobile')


def mobile_len_validator(mobile):
    """
    validator for check mobile length
    """
    if len(mobile) != 13:
        raise ValidationError('Invalid mobile len')