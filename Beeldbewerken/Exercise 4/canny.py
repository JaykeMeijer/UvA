from gaussian_functions import gD
from sys import argv, exit
from pylab import figure, subplot, imread, imshow, show

def canny(F, s):
    '''Apply a canny edge detector to the image.'''
    gaussian_blur = gD(F, s, 2, 2)
    threshold = 0.5
    
    for x in range(len(gaussian_blur[0])):
        for y in range(len(gaussian_blur)):   
            gaussian_blur[x][y] = zero_crossings(gaussian_blur, x, y)
    
    return gaussian_blur
    
def zero_crossings(image, x, y):
    '''Check if there are positive and negative pixels on either side of a
    given pixel.'''
    left = image[x-1][y] if inImage(image, x-1, y) else 0
    right = image[x+1][y] if inImage(image, x+1, y) else 0
    above = image[x][y-1] if inImage(image, x, y-1) else 0
    below = image[x][y+1] if inImage(image, x, y+1) else 0
    l_above = image[x-1][y-1] if inImage(image, x-1, y-1) else 0
    r_above = image[x+1][y-1] if inImage(image, x+1, y-1) else 0
    l_below = image[x-1][y+1] if inImage(image, x-1, y+1) else 0
    r_below = image[x+1][y+1] if inImage(image, x+1, y+1) else 0
    
    if (left * right < 0) or (above * below < 0) or \
       (l_above * r_below < 0) or (l_below * r_above < 0):
        return image[x][y]
    else:
        return 0       
    
def inImage(image, x, y):
    return (x > 0 and x < len(image) - 1 and y > 0 and y < len(image[0]) - 1)

if len(argv) != 2:
    print "Usage: python canny.py [s]"
    exit(1)
           
s = float(argv[1])
Image = imread('cameraman.png')
result = canny(Image, s)

figure()
subplot(121)
imshow(Image, cmap='gray')
subplot(122)
imshow(result, cmap='gray')
show()
