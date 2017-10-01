from PIL import Image
from get_pixel_iter import get_pixel_iter
from io import BytesIO

class BadImageDataException(Exception):
    """Exception raised when the embedded image data is malformed"""
    def __init__(self, message):
        Exception.__init__(self, message)

def extract_text(input_file, output_file=None):
    """
    Extract the text from the given input image file.

    The output file can be a filename or None. If the output file is None
    (or another value considered \"false\"), then the text is written to
    standard output.
    """
    image = Image.open(input_file)
    pixel_iter = get_pixel_iter(image)
    bit_length = _read_bit_length(pixel_iter)
    if not _is_multiple_of_eight(bit_length):
        raise BadImageDataException("Bit length is not a multiple of eight")
    byte_length = bit_length // 8

    if output_file:
        with open(output_file, mode="wb") as output:
            _write_text(pixel_iter, output, byte_length)
        print("Text written to {}".format(output_file))
    else:
        with BytesIO() as output:
            _write_text(pixel_iter, output, byte_length)
            try:
                print(output.getvalue().decode())
            except UnicodeError as ex:
                raise BadImageDataException(
                    "Cannot print text, as it is not valid UTF-8/ASCII.")

def _read_bit_length(pixel_iter):
    """
    Read the bit length (32 bits) at the beginning of the image.

    This also skips over the 33rd bit.
    """
    length = _read_integer(pixel_iter, 32)
    #Ignore 33rd value
    next(pixel_iter)
    return length

def _read_integer(pixel_iter, bit_count):
    """Read a big-endian integer from the image."""
    int_value = 0
    try:
        for i in range(bit_count):
            bit = next(pixel_iter).bit_value
            int_value = (int_value << 1) | bit
        return int_value
    except StopIteration:
        raise BadImageDataException("Premature end of data")

def _is_multiple_of_eight(bit_length):
    """Check if the bit length is a multiple of eight."""
    return (bit_length // 8) * 8 == bit_length

def _write_text(pixel_iter, output, byte_length):
    """Write the text from the image to the output file."""
    for i in range(byte_length):
        output.write(_read_byte(pixel_iter))

def _read_byte(pixel_iter):
    """Read a byte from the image, returned as a byte string."""
    byte_value = _read_integer(pixel_iter, 8)
    return bytes([byte_value])
