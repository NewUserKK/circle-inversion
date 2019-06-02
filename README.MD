# Circle inversion
A simple script for circle inverting an image.

Works best with high-resolution images. 
Black 'flower' in the centre of resulting image happens because images are not infinite and therefore there's no pixels to go there. Black parts between pixels in the outer circle exist for the opposite reason -- usually there are less pixels within the circle to go out. Also there is a rounding problem -- inverted pixels' coordinates are float but coordinates on screen are integers so we need to round them.

## Usage:
`python inversion.py <file> <radius> [-c <centre-delta-x> <centre-delta-y>] [-o <out-name>] [-q]`
* file - input file for inversion
* radius - radius of circle respecting to which image will be inverted
* -c centre-delta-x/y - delta of circle from centre of image, 0 by default
* -o out-name - output file, none by default
* -q - won't show the result. Be sure that -o option is present if you want to see the result somewhere

## Dependencies:
* numpy
* PIL

## Example:

![Before](https://github.com/NewUserKK/circle-inversion/blob/master/example/blackhole.jpg)

![After (radius = 80)](https://github.com/NewUserKK/circle-inversion/blob/master/example/inverted.jpg)
