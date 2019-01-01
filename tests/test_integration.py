from io import BytesIO
from unittest import TestCase

from wagtail.images.models import Filter, Image
from wagtail.images.tests.utils import get_test_image_file


class WebPIntegrationTest(TestCase):

    def test_webp(self):
        fil = Filter(spec='width-400|format-webp')
        image = Image.objects.create(
            title="Test image",
            file=get_test_image_file(),
        )
        out = fil.run(image, BytesIO())

        self.assertEqual(out.format_name, 'webp')
