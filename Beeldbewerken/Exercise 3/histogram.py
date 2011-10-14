# This is the first part of exercise 3 of 'Beeldbewerken'.
#
# This program calculates histograms for several colormodels and then 
# intersects the histograms of 10 images to find out how much some images are
# alike.
#
# Authors: Jayke Meijer (6049885) and Richard Torenvliet (6138861)
from pylab import imread, ceil, zeros
from sys import argv
from create_hist import colHist

binsize = 16
no_images = 20

def histogramIntersect(h1, h2):
    '''Calculate the intersection of two histograms. It uses an algorithm
    described in "Indexing Via Color Histograms" by Michael J. Swain and Dana
    H. Ballard.'''
    intersection = 0
    normalizer = 0
    no_bins = len(h1)
    for r in range(0, no_bins):
        for g in range(0, no_bins):
            for b in range(0, no_bins):
                intersection += min(h1[r][g][b], h2[r][g][b])
                normalizer += h2[r][g][b]
    
    return float(intersection) / normalizer

# Determine color model
if len(argv) <= 1 or (len(argv) > 1 and argv[1] not in('RGB', 'HSV', 'HSL')):
    print "No valid color model provided, choosing RGB"
    colormodel = 'RGB'
else:
    print "Color model %s provided" % (argv[1])
    colormodel = argv[1]
    
# Get the images
images = []
for i in range(0, no_images):
    images.append(imread('amsterdamdb/%s.png' % (str(i))))
    #images.append(imread('TenImages/%s.png' % (str(i))))

# Calculate the number of bins
no_bins = ceil(255/binsize)

# Get the histograms
print "Calculating histograms, please wait..."
histograms = []
for i in images:
    histograms.append(colHist(i, (no_bins, no_bins, no_bins), colormodel))
    print "Calculated histogram."
print "Done calculating the histograms. Now intersecting."
    
# Intersect all the histograms
result = zeros((no_images,no_images))
for i in range(0,no_images):
    for j in range(0,no_images):
        result[i][j] = histogramIntersect(histograms[i], histograms[j])       
print result

# Find the best and worst match
mi = 1
ma = 0
pos_mi = (0, 0)
pos_ma = (0, 0)
for i in range(0, no_images):
    for j in range (0,no_images):
        if mi > result[i][j]:
            mi = result[i][j]
            pos_mi = (i,j)
        
        if ma < result[i][j] and result[i][j] != 1:
            ma = result[i][j]
            pos_ma = (i,j)
print "Best match %f for images %d and %d"  % (ma, pos_ma[0], pos_ma[1])
print "Worst match %f for images %d and %d" % (mi, pos_mi[0], pos_mi[1])
