import numpy as np
import sys

from PIL import Image, ImageDraw
from math import *


def circle_invert(z: complex, centre: complex, radius: int):
    return (radius ** 2 / (z.conjugate() - centre.conjugate())) + centre


def invert_image(name: str, radius: int, centre_delta: tuple = None, out_name = None):
    image = Image.open(name)
    width = image.size[0]
    height = image.size[1]
    pixels_list = image.load()
    pixels = np.array(image.getdata(), dtype=np.int8).reshape(height, width, 3)

    if centre_delta:
        centre = complex(width // 2 + centre_delta[0], height // 2 + centre_delta[1])
    else:
        centre = complex(width // 2, height // 2)

    new_pixels = np.zeros((height, width, 3), dtype = np.int8)

    for y in range(height):
        for x in range(width):
            try:
                inversion = circle_invert(complex(x, y), centre, radius)
                new_x = round(inversion.real)
                new_y = round(inversion.imag)
                new_pixels[new_y, new_x] = pixels[y, x]
            except IndexError:
                pass
            except ZeroDivisionError:
                pass

    draw = ImageDraw.Draw(image)
    draw.ellipse(
        (centre.real - radius, centre.imag - radius, centre.real + radius, centre.imag + radius),
        outline = (0, 255, 42)
    )
    del draw
    image.show()

    inverted_image = Image.fromarray(new_pixels, 'RGB')
    inverted_image.show()
    if out_name:
        inverted_image.save(out_name)


if __name__ == "__main__":
    try:
        args = sys.argv

        name = args[1]

        radius = int(args[2])

        if '-c' in args:
            index = args.index('-c')
            centre_x = int(args[index + 1])
            centre_y = int(args[index + 2])
            centre = (centre_x, centre_y)
        else:
            centre = None

        if '-o' in args:
            index = args.index('-o')
            out_name = args[index + 1]
        else:
            out_name = 'inverted.jpg'

        invert_image(name, radius, centre, out_name)

    except IndexError:
        print("Usage: python inversion.py <file> <radius> [-c <centre-delta-x> <centre-delta-y>] [-o <out-name>]")

    except:
        print(sys.exc_info()[0], sys.exc_info()[1])
    