def get_pixel_iter(image):
    """
    Get an iterator over the pixel color values in the Pillow image.

    The iterator yields each value R then G then B, then right to left,
    then bottom to top.

    Each value is represented as an object with a \"bit_value\" attribute.
    Accessing the attribute accesses the corresponding bit in the value.
    """
    if "RGB" not in image.mode:
        raise ImageModeException()

    (width, height) = image.size
    for y in range(height - 1, -1, -1):
        for x in range(width - 1, -1, -1):
            for channel in range(3):
                yield _PixelValueBit(image, (x, y), channel)

class ImageModeException(Exception):
    """Exception raised when the image is not in a supported mode (RGB)"""
    def __init__(self):
        Exception.__init__(self,
            "Image does not have a supported color mode (RGB/RGBA)")

class _PixelValueBit:
    """
    Class that provides access to a bit of a pixel value.
    (BIT_POSITION determines which bit is accessed.)
    """

    BIT_POSITION = 0
    """Position of the bit being accessed (0 = LSB)"""

    def __init__(self, image, coordinates, channel):
        self.image = image
        self.coordinates = coordinates
        self.channel = channel

    @property
    def bit_value(self):
        """Get or set the bit (0 or 1)."""
        pixel_value = self.image.getpixel(self.coordinates)[self.channel]
        return int(bool(pixel_value & (1 << self.BIT_POSITION)))

    @bit_value.setter
    def bit_value(self, bit):
        pixel_list = list(self.image.getpixel(self.coordinates))
        pixel_value = pixel_list[self.channel]

        if bit:
            pixel_value |= (1 << self.BIT_POSITION)
        else:
            pixel_value &= ~(1 << self.BIT_POSITION)

        pixel_value &= 0xFF
        pixel_list[self.channel] = pixel_value
        self.image.putpixel(self.coordinates, tuple(pixel_list))