from scipy.ndimage import convolve, convolve1d
from pylab import figure, show, zeros, average, plot, imread, legend, subplot,\
imshow, title, delaxes
from sys import argv, exit
from gaussian_functions import gD

if len(argv) != 2:
    print "Usage: python time.py s"
    exit(1)
           
s = float(argv[1])

Image = imread('cameraman.png')
Images = zeros((6, Image.shape[0], Image.shape[1]))
labels = ['F', 'Fx', 'Fy', 'Fxx', 'Fxy', 'Fyy']
Images[0] = Image
j = 0

Images[1] = gD(Image, s, 1, 0)
Images[2] = gD(Image, s, 0, 1)
Images[3] = gD(Image, s, 2, 0)
Images[4] = gD(Image, s, 1, 1)
Images[5] = gD(Image, s, 0, 2)

figure()
for i in xrange(1, 10):
    if i in [1, 4, 5, 7, 8, 9]:
        subplot(330 + i)
        imshow(Images[j], cmap='gray')
        title(labels[j])

        j += 1

show()    
