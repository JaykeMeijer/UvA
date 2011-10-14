from numpy import zeros, arange, pi, e, ceil, meshgrid, array
from matplotlib.pyplot import imread, imshow, plot, xlabel, ylabel, show, \
        subplot, xlim, savefig
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import convolve, convolve1d
from time import time
from sys import argv, exit

def exit_with_usage():
    """Print an error message with the program's usage and exit the program."""
    print 'Usage: python %s timer METHOD [ REPEAT ] | diff SCALE' \
            ' | der SCALE IORDER JORDER' % argv[0]
    exit(1)

def Gauss(s):
    """Sample a two-dimensional Gaussian function of scale s."""
    size = int(ceil(3 * s))
    r = 2 * size
    W = zeros((r, r))
    t = float(s) ** 2
    a = 1 / (2 * pi * t)

    # Sample the Gaussian function
    for x in xrange(r):
        for y in xrange(r):
            W[x, y] = a * e ** -(((x - size) ** 2 + (y - size) ** 2) / (2 * t))

    # Make sure that the sum of all kernel values is equal to one
    return W / W.sum()

def Gauss1(s):
    """Sample a one-dimensional Gaussian function of scale s."""
    size = int(ceil(3 * s))
    r = 2 * size
    W = zeros((r,))
    t = float(s) ** 2
    a = 1 / (2 * pi * t)

    # Sample the Gaussian function
    W = array([a * e ** -((x - size) ** 2 / (2 * t)) for x in xrange(r)])

    # Make sure that the sum of all kernel values is equal to one
    return W / W.sum()

def plot_mask(W, ax, stride):
    """"""
    x = arange(W.shape[0])
    Y, X = meshgrid(x, x)
    ax.plot_surface(X, Y, W, rstride=stride, cstride=stride, cmap='jet')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('g(x, y)')

def gD(F, s, iorder, jorder):
    """Create the Gaussian derivative convolution of image F."""
    funcs = [lambda x: e ** -(x ** 2 / (2 * s ** 2)) / (2 * pi * s ** 2), \
             lambda x: -x * e ** -(x ** 2 / (2 * s ** 2)) \
                       / (2 * pi * s ** 4), \
             lambda x: -(x ** 2 - s ** 2) * e ** -(x ** 2 / (2 * s ** 2)) \
                       / (2 * pi * s ** 6)]
    size = int(ceil(3 * s))
    r = 2 * size
    iterator = map(float, range(r))
    W = zeros((r, r))
    Fx = funcs[iorder]
    Fy = funcs[jorder]

    for x in iterator:
        for y in iterator:
            W[x, y] = Fx(x - size) * Fy(y - size)

    return W, convolve(F, W, mode='nearest')

if __name__ == '__main__':
    if len(argv) < 2:
        exit_with_usage()

    F = imread('cameraman.png')

    if argv[1] == 'der':
        if len(argv) < 5:
            exit_with_usage()

        s = float(argv[2])
        W, G = gD(F, s, int(argv[3]), int(argv[4]))
        subplot(131)
        imshow(F, cmap='gray')
        plot_mask(W, subplot(132, projection='3d'), s / 4)
        subplot(133)
        imshow(G, cmap='gray')
    elif argv[1] == 'timer':
        if len(argv) < 3:
            exit_with_usage()

        method = argv[2]
        repeat = int(argv[3]) if len(argv) > 3 else 1

        # Time for multiple scales
        S = [1, 2, 3, 5, 7, 9, 11, 15, 19]
        times = []

        for i, s in enumerate(S):
            t = 0

            for k in xrange(repeat):
                start = time()

                if method == '1d':
                    convolve1d(F, Gauss1(s), axis=0, mode='nearest')
                elif method == '2d':
                    convolve(F, Gauss(s), mode='nearest')

                t += time() - start

            times.append(t / repeat)

        xlim(S[0], S[-1])
        xlabel('s')
        ylabel('time (s)')
        plot(S, times, 'o-')
    elif argv[1] == 'diff':
        # Calculate and plot the convolution of the given scale
        if len(argv) < 3:
            exit_with_usage()

        s = float(argv[2])
        W = Gauss(s)
        G = convolve(F, W, mode='nearest')

        # Original image
        subplot(131)
        imshow(F, cmap='gray')

        # Gauss function (3D plot)
        plot_mask(W, subplot(132, projection='3d'), s / 4)

        # Convolution
        subplot(133)
        imshow(G, cmap='gray')

    show()
