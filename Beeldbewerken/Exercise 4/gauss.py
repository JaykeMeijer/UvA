# By Jayke and Richard
from scipy.ndimage import convolve, convolve1d
from pylab import figure, subplot, imread, zeros, arange, \
meshgrid, cm, imshow, show
from mpl_toolkits.mplot3d import Axes3D
from sys import argv, exit
from gaussian_functions import gauss, gauss1, gD, f1, f1_1, f1_2

if len(argv) != 4:
    print "Usage: python gauss.py s '1D'|'2D'|'gD' 1|0 (1 shows output \
           images, 0 does not)"
    exit(1)
           
s = float(argv[1])
method = argv[2]
show_out = int(argv[3])
Image = imread('cameraman.png')

if method == '2D':
    Gs = gauss(s)
    G = convolve(Image, Gs, mode='nearest')
elif method == '1D':
    Gsx = gauss1(s, f1)
    G2 = convolve1d(Image, Gsx, axis=0, mode='nearest')
    G2 = convolve1d(G2, Gsx, axis=1, mode='nearest')
elif method == 'gD':
    iorder = 2
    jorder = 2
    result = gD(Image, s, iorder, jorder)
else:
    print "Invalid method"
    exit(1)

if show_out == 1:
    if method == '2D':
        fig = figure()
        X = arange(0, Gs.shape[0])
        Y = arange(0, Gs.shape[1])

        # create meshgrid
        X, Y = meshgrid(X, Y)

        # matplot lib version < 1.0 uses Axes3D
        ax = Axes3D(fig)

        surf = ax.plot_surface(X, Y, Gs, rstride=1, cstride=1, cmap=cm.jet, \
                                linewidth=0, antialiased=False)        
    
    figure(2)

    # Original image
    subplot(211)
    imshow(Image, cmap ='gray')

    if method == '2D':
        # Mask 1
        subplot(223)
        imshow(Gs, cmap='gray')

        # Image with mask 1
        subplot(224)
        imshow(G, cmap ='gray')
    elif method == '1D':
        # Mask 2 in one direction
        subplot(223)
        imshow((Gsx, Gsx), cmap='gray')

        # Image with mask 2
        subplot(224)
        imshow(G2, cmap ='gray')
    else:
        subplot(212)
        imshow(result, cmap='gray')
    
    show()
