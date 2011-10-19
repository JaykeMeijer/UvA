# By Jayke and Richard
from scipy.ndimage import convolve, convolve1d
from pylab import figure, subplot, imread, ceil, zeros, pi, e, arange, \
meshgrid, cm, imshow, show
from mpl_toolkits.mplot3d import Axes3D

# Return value of Gauss on given x and y with scale s and size of n (= 6 * s)
def f(s, n, x, y):
   """Gaussian function"""
   return 1 / (2 * pi * (s ** 2)) * (e ** -(((x - n / 2)**2 + (y - n / 2)**2 ) 
                                                              / (2 * (s ** 2))))
                                                              
# Return value of Gauss on given x and y with scale s and size of n (= 6 * s)
def f1(s, n, x):
   """1-D Gaussian function"""
   return 1 / (2 * pi * (s ** 2)) * (e ** -(((x - n / 2)**2) / (2 * (s ** 2))))
        
# Gaussian filter with a kernel of 6s - 1 values
def gauss(s):
    """Contruct a 2-D Gaussian mask"""        
    # for sufficient result use ceil(6s) by ceil(6s) for a gaussian filter
    # read: http://en.wikipedia.org/wiki/Gaussian_blur for more explaination     
    n = int(ceil(6 * s) + 1)
    s = float(s)
    
    # n * n zero matrix of floats
    gaussFilter = zeros((n, n), dtype=float)

    # fill gaussFilter[][] with gaussian values on x and y
    for x in range(n):
        for y in range(n):
            gaussFilter[x][y] = f(s, n, x, y)
            
    # All values between 0 and 1
    return gaussFilter / gaussFilter.sum()
    
def gauss1(s):
    '''Construct a 1-D Gaussian mask''' 
    # for sufficient result use ceil(6s) by ceil(6s) for a gaussian filter
    # read: http://en.wikipedia.org/wiki/Gaussian_blur for more explaination     
    n = int(ceil(6 * s) + 1)
    s = float(s)
    
    # n * n zero matrix of floats
    gaussFilter = zeros((n), dtype=float)

    # fill gaussFilter[] with gaussian values on x
    for x in range(n):
        gaussFilter[x] = f1(s, n, x)
            
    # All values between 0 and 1
    return gaussFilter / gaussFilter.sum()
   
Image = imread('cameraman.png')

Gs = gauss(3)
Gsx = gauss1(3)
        
fig = figure()

X = arange(0, Gs.shape[0])
Y = arange(0, Gs.shape[1])

# create meshgrid
X, Y = meshgrid(X, Y)

# matplot lib version < 1.0 uses Axes3D
ax = Axes3D(fig)

surf = ax.plot_surface(X, Y, Gs, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False)

figure(2)

# Convolution with gauss function (B)
G = convolve(Image, Gs, mode='nearest')
G2 = convolve1d(Image, Gsx, axis=0, mode='nearest')
G2 = convolve1d(G2, Gsx, axis=1, mode='nearest')

# Original image
subplot(421)
imshow(Image, cmap ='gray')

# Mask 1
subplot(423)
imshow(Gs, cmap='gray')

# Image with mask 1
subplot(424)
imshow(G, cmap ='gray') 

# Mask 2 in one direction
subplot(425)
imshow((Gsx, Gsx), cmap='gray')

# Image with mask 2
subplot(426)
imshow(G2, cmap ='gray')
show()
