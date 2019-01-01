from io import BytesIO
import imghdr

from django.test import TestCase
from willow.image import Image

from wagtail_webp.image_operations import WEBPImageFile


class SaveAsWebPTest(TestCase):

    def test_pillow_save_as_webp(self):
        output = BytesIO()
        with open('tests/images/flower.jpg', 'rb') as f:
            image = Image.open(f)

            return_value = image.save_as_webp(output)
            output.seek(0)

            self.assertIsInstance(return_value, WEBPImageFile)
            self.assertEqual('webp', return_value.format_name)
            self.assertEqual('webp', imghdr.what(output))
            self.assertEqual(output, return_value.f)
