import numpy as np
import sys
import time
import functools
import traceback

from PIL import Image, ImageDraw
from math import *


def measure_time(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print("Finished {0} in {1} secs".format(func.__name__, run_time))
        return value
    return wrapper_timer


def run_inversion(name: str, radius: int, centre_delta: tuple = None, out_name: str = None, show_result = True):
    image = Image.open(name)
    width = image.size[0]
    height = image.size[1]

    pixels = load_pixels(image)

    if centre_delta:
        centre = complex(width // 2 + centre_delta[0], height // 2 + centre_delta[1])
    else:
        centre = complex(width // 2, height // 2)

    inverted_pixels = invert_image(pixels, width, height, centre, radius)
    inverted_image = Image.fromarray(inverted_pixels, 'RGB')

    if out_name:
        inverted_image.save(out_name)

    if show_result:
        draw = ImageDraw.Draw(image)
        draw.ellipse(
            (centre.real - radius, centre.imag - radius, centre.real + radius, centre.imag + radius),
            outline = (0, 255, 42)
        )
        del draw
        image.show()
        inverted_image.show()


@measure_time
def load_pixels(image: Image) -> np.array:
    return np.array(image.getdata(), dtype=np.int8).reshape(image.size[1], image.size[0], 3)


@measure_time
def invert_image(pixels: np.array, width: int, height: int, centre: complex, radius: int) -> np.array:
    new_pixels = np.zeros((height, width, 3), dtype = np.int8)
    for y in range(0, height):
        for x in range(0, width):

            def circle_invert(z: complex, centre: complex, radius: int):
                return (radius ** 2 / (z.conjugate() - centre.conjugate())) + centre

            try:
                inversion = circle_invert(complex(x, y), centre, radius)
                new_x = round(inversion.real)
                new_y = round(inversion.imag)
                new_pixels[new_y, new_x] = pixels[y, x]
            except IndexError:
                pass
            except ZeroDivisionError:
                pass

    return new_pixels


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
            out_name = None

        if '-q' in args:
            show_result = False
        else:
            show_result = True

        run_inversion(name, radius, centre, out_name, show_result)

    except IndexError:
        print("Usage: python inversion.py <file> <radius> [-c <centre-delta-x> <centre-delta-y>] [-o <out-name>]")

    except:
        traceback.print_exc()
    

