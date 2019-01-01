from wagtail.core import hooks

from .image_operations import FormatOperation


@hooks.register('register_image_operations')
def register_image_operations():
    return [
        ('format', FormatOperation),
    ]
