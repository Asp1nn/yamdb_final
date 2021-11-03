from datetime import date

from rest_framework.exceptions import ValidationError


def year_not_from_the_future(value):
    if value > date.today().year:
        raise ValidationError('Год не может быть из будущего:(')
