from PIL import Image
from get_pixel_iter import get_pixel_iter
from io import BytesIO

class OutOfPixelsException(Exception):
    """
    Exception raised when there are not enough pixels in the image to
    embed the text.
    """
    def __init__(self):
        Exception.__init__(self, "Not enough pixels in the image")

def embed_text(input_file, output_file, text):
    """
    Embed the given text in the input image file and save it to the
    given output file.
    """
    with BytesIO(text.encode()) as text_file_obj:
        _embed_text_from_file_obj(input_file, output_file, text_file_obj)

def embed_text_from_file(input_file, output_file, text_file):
    """
    Embed the text from the text file in the input image file and save it
    to the given output file.
    """
    with open(text_file, mode="rb") as text_file_obj:
        _embed_text_from_file_obj(input_file, output_file, text_file_obj)

def _embed_text_from_file_obj(input_file, output_file, text_file_obj):
    """
    Embed the text from the text file object in the input image file and
    save it to the given output file.
    """
    image = Image.open(input_file)
    pixel_iter = get_pixel_iter(image)

    #Skip over the length and write the data first
    for i in range(33):
        next(pixel_iter)

    byte_length = 0
    for byte in iter(lambda: text_file_obj.read(1), b''):
        byte_length += 1
        _write_integer(pixel_iter, byte[0], 8)

    #Now go back and write the length
    pixel_iter = get_pixel_iter(image)
    bit_length = byte_length * 8
    _write_integer(pixel_iter, bit_length, 32)

    image.save(output_file)

def _write_integer(pixel_iter, value, bit_count):
    """Write the big-endian integer into the image."""
    try:
        for bit_position in range(bit_count - 1, -1, -1):
            bit = int(bool(value & (1 << bit_position)))
            next(pixel_iter).bit_value = bit
    except StopIteration:
        raise OutOfPixelsException()