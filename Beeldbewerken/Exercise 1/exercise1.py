# Author: Jayke Meijer 6049885

from pylab import *

# Make the CST version of the image
def cst(f):
    fmin = amin(f) # the min value in an array
    fmax = amax(f) # the max value in an array
    return (f-fmin)/(fmax-fmin)

# Get the original image as matrix
img = imread('lowcontrast.png')

# Show the original image
figure(1)
clf()
im = imshow(img, vmin=0,vmax=1)

# Calculate and show the histogram of the original image
figure(2)
clf()
h,be = histogram(img.flatten(), bins = 40)
bar(be[0:-1], h, width=diff(be)[0])
xlim((0,1))

# Get the CST of the original figure
cst_figure = cst(img)

# Show the CST version of the original figure
figure(3)
clf()
im = imshow(cst_figure, vmin=0,vmax=1)

# Show the histogram of the CST version
figure(4)
clf()
h,be = histogram(cst_figure.flatten(), bins = 40)
bar(be[0:-1], h, width=diff(be)[0])
xlim((0,1))

# Show all the figures
show()
