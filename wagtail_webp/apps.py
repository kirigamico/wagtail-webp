from django.apps import AppConfig
from willow.plugins.pillow import PillowImage
from willow.registry import registry


class WagtailWebPConfig(AppConfig):
    name = 'wagtail_webp'

    def ready(self):
        from .image_operations import pillow_save_as_webp
        registry.register_operation(PillowImage, 'save_as_webp', pillow_save_as_webp)
