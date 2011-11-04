# This program times the 1D and 2D gaussian convolution.
# Authors: Jayke Meijer (6049885) and Richard Torenvliet (6138861)
from scipy.ndimage import convolve, convolve1d
from pylab import figure, show, zeros, average, plot, imread, legend, xlabel, \
ylabel
from sys import argv, exit
from gaussian_functions import gauss, gauss1, f1
from time import time

if len(argv) != 2:
    print "Usage: python time.py '1D'|'2D'"
    exit(1)
           
method = argv[1]

Image = imread('cameraman.png')
timings = zeros((20))
timings[0] = 0
temp = zeros((3))

if method == '2D':
    for i in xrange(1, 20):
        for j in xrange(0,3):
            start = time()
            Gs = gauss(i)
            G = convolve(Image, Gs, mode='nearest')
            stop = time()
            temp[j] = stop - start
        timings[i] = average(temp)
elif method == '1D':
    for i in xrange(1, 20):
        for j in xrange(0,3):
            start = time()
            Gsx = gauss1(i, f1)
            G2 = convolve1d(Image, Gsx, axis=0, mode='nearest')
            G2 = convolve1d(G2, Gsx, axis=1, mode='nearest')
            stop = time()
            temp[j] = stop - start
        timings[i - 1] = average(temp)
else:
    print 'Invalid method'
    exit(1)
        
figure()
plot(timings, label=method)
xlabel('s')
ylabel('Time(s)')
legend()
show()
