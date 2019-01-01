from io import BytesIO
from unittest import TestCase

from wagtail.images.models import Filter, Image
from wagtail.images.tests.utils import get_test_image_file

from wagtail_webp.image_operations import FormatOperation


class WebPIntegrationTest(TestCase):

    def test_webp(self):
        fil = Filter(spec='width-400|format-webp')
        image = Image.objects.create(
            title="Test image",
            file=get_test_image_file(),
        )
        out = fil.run(image, BytesIO())

        self.assertEqual(out.format_name, 'webp')


class FormatOperationTest(TestCase):

    def test_base_support(self):
        formats = ['jpeg', 'png', 'gif']

        for fmt in formats:
            operation = FormatOperation(None, fmt)

            mock_env = {}
            operation.run(willow=None, image=None, env=mock_env)

            self.assertEqual(fmt, mock_env['output-format'])

    def test_webp_support(self):
        operation = FormatOperation(None, 'webp')

        mock_env = {}
        operation.run(willow=None, image=None, env=mock_env)

        self.assertEqual('webp', mock_env['output-format'])

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            FormatOperation(None, 'mp4')
