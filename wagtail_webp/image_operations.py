from django.conf import settings
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


def filter_run_patch(self, image, output):
    # ==> Begin copy-pasta
    with image.get_willow_image() as willow:
        original_format = willow.format_name

        # Fix orientation of image
        willow = willow.auto_orient()

        env = {
            'original-format': original_format,
        }
        for operation in self.operations:
            willow = operation.run(willow, image, env) or willow

        # Find the output format to use
        if 'output-format' in env:
            # Developer specified an output format
            output_format = env['output-format']
        else:
            # Default to outputting in original format
            output_format = original_format

            # Convert BMP files to PNG
            if original_format == 'bmp':
                output_format = 'png'

            # Convert unanimated GIFs to PNG as well
            if original_format == 'gif' and not willow.has_animation():
                output_format = 'png'

        if output_format == 'jpeg':
            # Allow changing of JPEG compression quality
            if 'jpeg-quality' in env:
                quality = env['jpeg-quality']
            elif hasattr(settings, 'WAGTAILIMAGES_JPEG_QUALITY'):
                quality = settings.WAGTAILIMAGES_JPEG_QUALITY
            else:
                quality = 85

            # If the image has an alpha channel, give it a white background
            if willow.has_alpha():
                willow = willow.set_background_color_rgb((255, 255, 255))

            return willow.save_as_jpeg(
                output,
                quality=quality,
                progressive=True,
                optimize=True,
            )
        elif output_format == 'png':
            return willow.save_as_png(output, optimize=True)
        elif output_format == 'gif':
            return willow.save_as_gif(output)
        elif output_format == 'webp':
            return willow.save_as_webp(output)
    # ==> End copy-pasta
