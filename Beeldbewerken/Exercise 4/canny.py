# This program is a canny edge detector.
# Authors: Jayke Meijer (6049885) and Richard Torenvliet (6138861)
from gaussian_functions import gauss1, f1_1, gD
from scipy.ndimage import convolve, convolve1d
from sys import argv, exit
from pylab import figure, subplot, imread, imshow, show, zeros, sqrt, \
    arctan2, pi

def canny(F, s, high_threshold, low_threshold):
    '''Apply a canny edge detector to the image.'''
    blurred = gD(F, s, 0, 0)

    filt = gauss1(1.4, f1_1)
    Gx = convolve1d(blurred, filt, axis=0, mode='nearest')
    Gy = convolve1d(blurred, filt, axis=1, mode='nearest')
    G = zeros(F.shape)
    angle = zeros(F.shape, dtype='int')
    after_nm = zeros(F.shape)
    
    # Finding intensity grade
    for x in xrange(len(G[0])):
        for y in xrange(len(G)):
            G[x][y] = sqrt(Gx[x][y] ** 2 + Gy[x][y] ** 2)
            angle[x][y] = int( \
                    round(arctan2(Gx[x][y], Gy[x][y]) * 4 / pi + 1)) % 4
    
    # Non-maximum suppression
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
                after_nm[x][y] = 0
            else:
                after_nm[x][y] = G[x][y]
    
    # Hysteresis thresholding
    high_threshold *= (after_nm.max() - after_nm.min()) / 255
    low_threshold *= (after_nm.max() - after_nm.min()) / 255
    after_threshold = zeros(after_nm.shape, dtype = int)
    
    def follow_edge(x, y):
        """Follow an edge by recursively checking if the neighbours are in 
        it."""
        after_threshold[x][y] = 1

        for x in xrange(-1, 2):
            for y in xrange(-1, 2):
                if (not x or not y):
                    if after_nm[x][y] >= low_threshold and not after_threshold:
                        follow_edge(x, y)
    
    # Make border pixels zero
    for i in xrange(len(after_nm[0])):
        after_nm[i][0] = 0
        after_nm[i][len(after_nm) - 1] = 0
        
    for i in xrange(len(after_nm) - 1):
        after_nm[0][i] = 0
        after_nm[len(after_nm[0]) - 1][i] = 0
    
    # Follow each line
    for x in xrange(len(after_nm[0])):
        for y in xrange(len(after_nm)):
            if after_nm[x][y] >= high_threshold and not after_threshold[x][y]:
                follow_edge(x, y)
    
    return after_threshold
    
def inImage(image, x, y):
    '''Return if a pixel is in the image.'''
    return (x > 0 and x < len(image) - 1 and y > 0 and y < len(image[0]) - 1)

if len(argv) != 4:
    print "Usage: python canny.py s Th Tl"
    exit(1)
    
s = float(argv[1])
Th = float(argv[2])
Tl = float(argv[3])
           
Image = imread('cameraman.png')
result = canny(Image, s, Th, Tl)

# Create image overlay
result2 = zeros((result.shape[0], result.shape[1], 3))
for x in xrange(len(result2[0])):
        for y in xrange(len(result2)):
            if result[x][y]:
                result2[x][y] = (1.0, 1.0, 0)
                result[x][y] = 0
            else:
                result2[x][y] = (Image[x][y], Image[x][y], Image[x][y])
                result[x][y] = 255
    
figure()
subplot(131)
imshow(Image, cmap='gray')
subplot(132)
imshow(result, cmap='gray')
subplot(133)
imshow(result2, cmap='rgb')
show()
