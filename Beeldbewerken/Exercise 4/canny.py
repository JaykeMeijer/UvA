from gaussian_functions import gD
from sys import argv, exit
from pylab import figure, subplot, imread, imshow, show, zeros

def canny(F, s):
    '''Apply a canny edge detector to the image.'''
    blurred = gD(F, s, 2, 2)
    
    result = zeros(blurred.shape)
    for x in range(len(blurred[0])):
        for y in range(len(blurred)):
            result[x][y] = zero_crossings(blurred, x, y)
    
    return result
    
def zero_crossings(image, x, y):
    '''Check if there are positive and negative pixels on either side of a
    given pixel.'''
    left = image[x-1][y] if inImage(image, x-1, y) else 255
    right = image[x+1][y] if inImage(image, x+1, y) else 255
    above = image[x][y-1] if inImage(image, x, y-1) else 255
    below = image[x][y+1] if inImage(image, x, y+1) else 255
    l_above = image[x-1][y-1] if inImage(image, x-1, y-1) else 255
    r_above = image[x+1][y-1] if inImage(image, x+1, y-1) else 255
    l_below = image[x-1][y+1] if inImage(image, x-1, y+1) else 255
    r_below = image[x+1][y+1] if inImage(image, x+1, y+1) else 255
    
    if left * right <= 0 or above * below <= 0 or \
       l_above * r_below <= 0 or l_below * r_above <= 0:
        return image[x][y]
    else:
        return 255.0
    
def inImage(image, x, y):
    return (x > 0 and x < len(image) - 1 and y > 0 and y < len(image[0]) - 1)

if len(argv) != 1:
    print "Usage: python canny.py"
    exit(1)
           
Image = imread('cameraman.png')
result = canny(Image, 1)

# Create image overlay
result2 = zeros((result.shape[0], result.shape[1], 3))
for x in range(len(result2[0])):
        for y in range(len(result2)):
            if result[x][y] < 255:
                result2[x][y] = (1.0, 1.0, 0)
            else:
                result2[x][y] = (Image[x][y], Image[x][y], Image[x][y])

figure()
subplot(131)
imshow(Image, cmap='gray')
subplot(132)
imshow(result, cmap='gray')
subplot(133)
imshow(result2, cmap='rgb')
show()
