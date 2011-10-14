# By Jayke and Richard
from scipy.ndimage import convolve
from pylab import *
from mpl_toolkits.mplot3d import Axes3D

def f(s, n, x, y):
   """Gaussian function"""
   return 1 / (2 * pi * (s ** 2)) * (e ** -(((x - n / 2)**2 + (y - n / 2)**2 ) 
                                                              / (2 * (s ** 2))))
        
# Gaussian filter with a kernel of 6s - 1 values
def gauss(s):
    """Two dimensional Gaussian mask"""
    # 1 for verbose, 0 for non-verbose
    debug = 0;    
    
    # if s is even, the heighest value will not be in the middle of the 2D
    # array.
    # a = 1 for even and 0 for odd
    #a = 1 if (int(s) % 2 == 0) else 0
        
    # for sufficient result use ceil(6s) by ceil(6s) for a gaussian filter
    # read: http://en.wikipedia.org/wiki/Gaussian_blur for more explaination     
    n = int(ceil(6 * s) + 1)
    s = float(s)
    
    # n * n zero matrix of floats3
    gaussFilter = zeros((n, n), dtype=float)

    for i in range(n):
        for j in range(n):
            gaussFilter[i][j] = f(s, n, i, j)
            
            if debug: print("%.4f" % gaussFilter[i][j]),
        if debug: print '\n'
    
    # All values between 0 and 1
    return gaussFilter #/ gaussFilter.sum()
    
F = imread('cameraman.png') 

B = gauss(3)

figure(1)
fig = figure()

X = arange(0, B.shape[0])
Y = arange(0, B.shape[1])

X, Y = meshgrid(X, Y)

ax = Axes3D(fig)

surf = ax.plot_surface(X, Y, B, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False)

figure(2)
subplot(121)
imshow(B, cmap='gray')
G = convolve(F, B, mode='nearest')
subplot(122)
imshow(G, cmap ='gray') 
show()
#subplot(111)
#imshow(F, cmap ='gray')

#subplot(122)

#show()
