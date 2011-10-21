from gaussian_functions import gD
from sys import argv, exit
from pylab import figure, subplot, imread, imshow, show

def canny(F, s):
    '''Apply a canny edge detector to the image.'''
    gaussian_blur = gD(F, s, 2, 2)
    
    for x in range(len(gaussian_blur[0])):
        for y in range(len(gaussian_blur)):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    pass
    
    return result
    
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
