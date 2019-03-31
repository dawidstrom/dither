from multikernel import kernel, multikernel
from PIL import Image
from itertools import chain
import time
import sys


start = time.time()


def dither(pixels, kernel_size, kernel_filter):
    """
    Simple ordered dithering filter. The purpose of this method 
    is to simulate grayscale information when downsampling an 
    image as just black and white.

    Args
    pixels: Input pixels, nested array of rgb tuples (r,g,b).
    kernel_size: Not used for dithering.
    kernel_filter: Determines what pixels to turn black vs white.
    """
    grey_pixels = map(lambda p: sum(p)/3, pixels) # Get grayscale of image.
    k_filter = list(chain(*kernel_filter)) # Flatten kernel.

    # Color pixels with a value higher than its
    #filtered = list(map(lambda p: (255,255,255) if p[0]>p[1] else (0,0,0), zip(grey_pixels, k_filter)))
    filtered = [(val,val,val) for val in grey_pixels]
    return filtered


def print_help():
    """
    Prints command usage.
    """
    print("Usage: python dither.py image.[jpg, png, etc]")


if __name__ == '__main__':
    # Determine if the correct number of parameters were given.
    if (len(sys.argv) != 2):
        print_help()
        sys.exit()

    kernel_size = (2,2)
    #kernel_filter = [[128]]
    kernel_filter = [[0,64],[128,196]]
    #kernel_filter = [[0,28,56],[85,113,142],[170,199,227]]

    im = Image.open(sys.argv[1])
    image = kernel(im, dither, kernel_size, kernel_filter);
    
    # Print elapsed time.
    print(time.time()-start)
    
    image.show()
