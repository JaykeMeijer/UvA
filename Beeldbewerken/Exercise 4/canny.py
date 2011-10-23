from gaussian_functions import gauss1, f1_1, gD
from scipy.ndimage import convolve, convolve1d
from sys import argv, exit
from pylab import figure, subplot, imread, imshow, show, zeros, sqrt, \
    arctan2, pi

def canny(F, s):
    '''Apply a canny edge detector to the image.'''
    blurred = gD(F, s, 0, 0)

    filt = gauss1(1.4, f1_1)
    Gx = convolve1d(blurred, filt, axis=0, mode='nearest')
    Gy = convolve1d(blurred, filt, axis=1, mode='nearest')
    G = zeros(F.shape)
    angle = zeros(F.shape, dtype='int')
    result = zeros(F.shape)
    
    for x in xrange(len(G[0])):
        for y in xrange(len(G)):
            G[x][y] = sqrt(Gx[x][y] ** 2 + Gy[x][y] ** 2)
            angle[x][y] = int(round(arctan2(Gx[x][y], Gy[x][y]) * 4 / pi + 1)) % 4
    
    for x in xrange(len(G[0])):
        for y in xrange(len(G)):
            if angle[x][y] == 0:
                side_one = G[x+1][y] if inImage(G, x+1, y) else 0
                side_two = G[x-1][y] if inImage(G, x-1, y) else 0
            elif angle[x][y] == 1:
                side_one = G[x-1][y-1] if inImage(G, x-1, y-1) else 0
                side_two = G[x+1][y+1] if inImage(G, x+1, y+1) else 0
            elif angle[x][y] == 2:
                side_one = G[x][y+1] if inImage(G, x, y+1) else 0
                side_two = G[x][y-1] if inImage(G, x, y-1) else 0
            elif angle[x][y] == 3:
                side_one = G[x-1][y+1] if inImage(G, x-1, y+1) else 0
                side_two = G[x+1][y-1] if inImage(G, x+1, y-1) else 0
            
            if not (G[x][y] > side_one and G[x][y] > side_two):
                result[x][y] = 255
            else:
                result[x][y] = 255 - G[x][y]
    
    return result
    
def inImage(image, x, y):
    return (x > 0 and x < len(image) - 1 and y > 0 and y < len(image[0]) - 1)

if len(argv) != 2:
    print "Usage: python canny.py [s]"
    exit(1)
    
s = float(argv[1])
           
Image = imread('cameraman.png')
result = canny(Image, s)


# Create image overlay
result2 = zeros((result.shape[0], result.shape[1], 3))
for x in xrange(len(result2[0])):
        for y in xrange(len(result2)):
            if result[x][y] < 250:
                result2[x][y] = (1.0, 1.0, 0)
            else:
                result2[x][y] = (Image[x][y], Image[x][y], Image[x][y])
                
figure()
subplot(131)
imshow(Image, cmap='gray')
subplot(132)
imshow(result, cmap='gray')
subplot(133)
imshow(result2, cmap='rgb')
show()
