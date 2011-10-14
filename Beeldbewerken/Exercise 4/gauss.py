from scipy.ndimage.filters import convolve
from pylab import *
from numpy import zeros

def f(s, n, x, y):
   """Gaussian function"""
   return 1 / (2 * pi * (s ** 2)) * (e ** -((x - n / 2)**2 + (y - n / 2)**2 ) / (2 * (s ** 2)))
        
# Gaussian filter with a kernel of 6s - 1 values
def gauss(s):
    """Two dimensional Gaussian mask"""
    # one for verbose, zero for non-verbose
    debug = 0;    
    
    # if s is even, the heighest value will not be in the middle of the 2D
    # array
    # a = 1 for even and 0 for odd
    a = 1 if (int(s) % 2 == 0) else 0
        
    # for sufficient result use ceil(6s) by ceil(6s) for a gaussian filter
    # read: http://en.wikipedia.org/wiki/Gaussian_blur for more explaination     
    n = int(ceil(6 * s) - a)
    s = float(s)
    
    # n * n zero matrix of floats3
    gaussFilter = zeros((n, n), dtype=float)

    for i in range(n):
        for j in range(n):
            gaussFilter[i][j] = f(s, n, i, j)
            
            if debug: print("%.4f" % gaussFilter[i][j]),
        if debug: print '\n'
    
F = imread('cameraman.png')

G = convolve(F, gauss(2), mode='nearest')

subplot(111)
imshow(F, cmap ='gray')
show()
subplot(122)
imshow(G, cmap ='gray') 
