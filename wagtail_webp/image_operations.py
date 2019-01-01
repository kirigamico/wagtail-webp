from wagtail.images.image_operations import FormatOperation as BaseFormatOperation


class FormatOperation(BaseFormatOperation):
    def construct(self, fmt):
        self.format = fmt

        if self.format not in ['jpeg', 'png', 'gif', 'webp']:
            raise ValueError("Format must be either 'jpeg', 'png', 'gif' or 'webp'")
