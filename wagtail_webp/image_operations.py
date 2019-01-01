from wagtail.images.image_operations import FormatOperation as BaseFormatOperation
from willow.image import ImageFile


class FormatOperation(BaseFormatOperation):
    def construct(self, fmt):
        self.format = fmt

        if self.format not in ['jpeg', 'png', 'gif', 'webp']:
            raise ValueError("Format must be either 'jpeg', 'png', 'gif' or 'webp'")


class WEBPImageFile(ImageFile):
    format_name = 'webp'


def pillow_save_as_webp(image, output):
    # Pillow only checks presence of optimize kwarg, not its value
    image.image.save(output, 'WEBP')
    return WEBPImageFile(output)
