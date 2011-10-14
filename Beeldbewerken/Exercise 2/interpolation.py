# This is a python module performs an interpolation on an image to get the 
# value for a non-integer pixelpoint.
#
# Authors: Jayke Meijer (6049885) and Richard Torenvliet (6138861)
from pylab import imread, plot, array, linspace, floor, ceil, show, figure

def pV(image, x, y, method):
  if inImage(image, x, y):
    if method == "nearest":
        interpolatedValue = image[round(x)][round(y)]
    elif method == "linear":
        x_low = floor(x)
        x_high = floor(x + 1)
        y_low = floor(y)
        y_high = floor(y + 1)
        x_y = (x_high - x_low) * (y_high - y_low)
        
        interpolatedValue = image[x_low][y_low] / x_y * (x_high - x) * (y_high - y)\
                          + image[x_high][y_low] / x_y * (x - x_low) * (y_high - y)\
                          + image[x_low][y_high] / x_y * (x_high - x) * (y - y_low)\
                          + image[x_high][y_high] / x_y * (x - x_low) * (y - y_low)
    else:
        print "No valid method"
        interpolatedValue = -1
    return interpolatedValue
  else:
    constantValue = 0
    return constantValue
    
def inImage(image, x, y):
    return (x > 0 and x < len(image) - 1 and y > 0 and y < len(image[0]) - 1)
    
def profile(image, x0, y0, x1, y1, n, method):
  # profile of an image along line in n points
  return array( [ pV(image,x,y,method) for (x,y) in zip(linspace(x0,x1,n), linspace(y0,y1,n)) ])
