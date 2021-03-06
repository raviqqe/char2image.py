import sys

import numpy
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont


__all__ = [
    'char_to_image',
    'char_to_image_dict',
    'chars_to_images',
    'filename_to_font'
]


FOREGROUND_COLOR = 255
BACKGROUND_COLOR = 0


def char_to_image(char, font, *, size):
    empty_image = PIL.Image.new("L", size, color=BACKGROUND_COLOR)

    try:
        image = empty_image.copy()
        PIL.ImageDraw.Draw(image).text((0, 0),
                                       char,
                                       font=font,
                                       fill=FOREGROUND_COLOR)
        return numpy.array(image, dtype=numpy.uint8)
    except UnicodeEncodeError:
        print(("Could not render the unicode character \\u{:04X}"
               .format(ord(char))),
              file=sys.stderr)
        return None


def char_to_image_dict(chars, font):
    size = tuple(map(max, zip(*[font.getsize(char) for char in chars])))
    pairs = {char: char_to_image(char, font, size=size) for char in chars}
    return {char: image.tolist() for char, image in pairs.items()
            if image is not None and (image != BACKGROUND_COLOR).any()}


def chars_to_images(chars, font, unknown_char='\uFFFD'):
    char_to_image = char_to_image_dict(set(chars), font)

    return [(char_to_image[char]
             if char in char_to_image else
             char_to_image[unknown_char])
            for char in chars]


def filename_to_font(filename, size):
    return PIL.ImageFont.truetype(filename, size=size)
