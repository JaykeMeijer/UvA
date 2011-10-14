# This is the final part of exercise 3 of 'Beeldbewerken'.
#
# This program highlights the spots where Waldo is most likely to be in an
# image. To do this, it uses the so called "Backprojection" algorithm, as
# described in "Indexing Via Color Histograms" by Michael J. Swain and Dana
# H. Ballard.
#
# Authors: Jayke Meijer (6049885) and Richard Torenvliet (6138861)
from create_hist import colHist, col2bin
from pylab import imread, show, imshow, subplot, ceil, zeros
from scipy.ndimage import correlate
from sys import argv

bins = 64
radius = 10

def convolution(radius, image):
    '''Apply convolution to the image.'''  
    radius_sq = radius ** 2
    filt = zeros((radius * 2 + 1, radius * 2 + 1), dtype='int')
    
    for i in range(filt.shape[0]):
        for j in range(filt.shape[1]):
            if (i - radius) ** 2 + (j - radius) ** 2 < radius_sq:
                filt[i][j] = 1
    
    return correlate(image, filt.astype(float) / filt.sum(), mode='nearest')

def calculate_R(I, M, bins):
    '''Calculate histogram R from the histogram of the original and the image 
    to find.'''
    R = zeros((bins, bins, bins))
    for r in range(bins):
        for g in range(bins):
            for b in range(bins):
                if I[r][g][b] != 0:
                    R[r][g][b] = float(M[r][g][b]) / I[r][g][b]
    return R
    
def create_b(original, R):
    '''Create image b from the histogram R and the original image.'''
    b = zeros(original.shape[:2])

    for x in range(original.shape[0]):
        for y in range(original.shape[1]):
            b[x][y] = min(R[col2bin(original[x][y], (bins,bins,bins))], 1)
    return b

# Determine color model
if len(argv) <= 1 or (len(argv) > 1 and argv[1] not in('RGB', 'HSV', 'HSL')):
    print "No valid color model provided, choosing RGB"
    colormodel = 'RGB'
else:
    print "Color model %s provided" % (argv[1])
    colormodel = argv[1]

original = imread('waldo/waldo_env.tiff') / 255.0
to_find = imread('waldo/waldo.tiff') / 255.0

print "Calculating Histograms"
I = colHist(original, (bins, bins, bins), colormodel)
M = colHist(to_find, (bins, bins, bins), colormodel)
R = calculate_R(I, M, bins)

print "Creating Backprojection"
b = create_b(original, R)

print "Applying Convolution."
b = convolution(radius, b)

subplot(121)
imshow(original,vmin=0,vmax=1, origin='lower')
subplot(122)
imshow(b,vmin=0,vmax=1, origin='lower')
show()
