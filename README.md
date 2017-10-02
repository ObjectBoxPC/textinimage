# Text in Image

Philip Chung

CPSC 353

October 31, 2017

Text in Image is a simple steganography tool that embeds text into the color values of an image.

## System Requirements

* Python 3 (tested on 3.5)
* Pillow (tested on 4.1.2)

## Basic Usage

To embed text:

	python3 textinimage.py embed -i original.jpg -t "Top secret" -o steg.png

To extract text:

	python3 textinimage.py extract -i steg.png

For additional options, run `python3 textinimage.py [operation] -h`.

### Note on Image Formats

Images with embedded text should be in a lossless format such as PNG, so that the exact pixel values are preserved.

## Architecture

The program consists of several Python modules, one for parsing command-line arguments, one for embedding, one for extracting, etc., along with a main script (`textinimage.py`) that calls the modules.

The code is greatly simplified by the `get_pixel_iter` module, which provides an iterator over the color values. This gives a linear view of the pixel values that the embedding and extracting modules can manipulate, without having to deal with pixel positions.