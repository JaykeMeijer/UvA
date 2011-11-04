# These are a number of gaussian functions and convolutions.
# Authors: Jayke Meijer (6049885) and Richard Torenvliet (6138861)
from scipy.ndimage import convolve, convolve1d
from pylab import ceil, zeros, pi, e, exp, sqrt, dot, array

def f(s, n, x, y):
   """Gaussian function. Return value of Gauss on given x and y with scale s 
   and size of n (= 6 * s)."""
   return 1 / (2 * pi * (s ** 2)) * (e ** -(((x - n / 2)**2 + (y - n / 2)**2 ) 
                                                              / (2 * (s ** 2))))

def f1(s, x):
   """1-D Gaussian function. Return value of Gauss on given x with scale s and 
   size of n (= 6 * s)."""
   return 1 / (sqrt(2 * pi * (s ** 2))) * (e ** -((x**2) / (2 * (s ** 2))))
   
def f1_1(s, x):
   """1-D Gaussian function, first derivative"""
   return 1 / (2 * pi * s ** 4) * (-x * e ** -(x ** 2 / (2 * s ** 2)))
   
def f1_2(s, x):
   """1-D Gaussian function, second derivative"""
   return 1 / (2 * pi * s ** 6) * \
            (-(x ** 2 - s ** 2) * e ** -(x ** 2 / (2 * s ** 2)))
        
def gauss(s):
    """Contruct a 2-D Gaussian mask with a kernel of 6s - 1 values"""        
    # for sufficient result use ceil(6s) by ceil(6s) for a gaussian filter
    # read: http://en.wikipedia.org/wiki/Gaussian_blur for more explaination     
    s = float(s)
    n = int(ceil(6 * s) + 1)
    
    # n * n zero matrix of floats
    gaussFilter = zeros((n, n), dtype=float)

    # fill gaussFilter[][] with gaussian values on x and y
    for x in xrange(n):
        for y in xrange(n):
            gaussFilter[x][y] = f(s, n, x, y)
            
    # All values between 0 and 1
    return gaussFilter / gaussFilter.sum()
    
def gauss1(s, func):
    '''Construct a 1-D Gaussian mask''' 
    # for sufficient result use ceil(6s) by ceil(6s) for a gaussian filter
    # read: http://en.wikipedia.org/wiki/Gaussian_blur for more explaination     
    s = float(s)
    r = int(ceil(3 * s))
    n = int(ceil(6 * s) + 1)
    
    # n * n zero matrix of floats
    gaussFilter = zeros((n), dtype=float)

    # fill gaussFilter[] with gaussian values on x
    for x in range(n):
        gaussFilter[x] = func(s, x - r)
    
    return gaussFilter

def gD(F, s, iorder, jorder):
    '''Create the Gaussian derivative convolution of image F.'''
    functions = [f1, f1_1, f1_2]
    s = float(s)
    
    filt_x = gauss1(s, functions[iorder])
    filt_y = gauss1(s, functions[jorder])
    
    gaussFilter = zeros((len(filt_x), len(filt_x)))
    
    for x in range(len(filt_x)):
        for y in range(len(filt_y)):
            gaussFilter[x][y] = filt_y[y] * filt_x[x]
            
    gaussFilter
    
    return convolve1d(convolve1d(F, filt_x, axis=0, mode='nearest'), filt_y, axis=1, mode='nearest')
#    return convolve(F, gaussFilter, mode='nearest')
