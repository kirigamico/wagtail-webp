from django.apps import AppConfig
from willow.plugins.pillow import PillowImage
from willow.registry import registry


class WagtailWebPConfig(AppConfig):
    name = 'wagtail_webp'

    def ready(self):
        from wagtail.images.models import Filter

        from .image_operations import filter_run_patch, pillow_save_as_webp

        registry.register_operation(PillowImage, 'save_as_webp', pillow_save_as_webp)

        # Monkeypatch Filter.run
        Filter.run = filter_run_patch
