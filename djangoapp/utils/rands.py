import string
from random import SystemRandom

from django.utils.text import slugify


def random_letters(k=5):
    return SystemRandom().choices(
        ''.join(string.ascii_letters + string.digits,
                k=k
                )
    )


def slugify_new(text, k):
    return slugify(text) + '-' + random_letters(k)
