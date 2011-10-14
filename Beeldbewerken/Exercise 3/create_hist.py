from pylab import zeros
from colorsys import rgb_to_hsv, rgb_to_hls

def colHist(image, bins, model):
    '''Create a histogram of an image in a specified colormodel.'''
    histogram = zeros(bins, dtype=int)
    
    if model == 'RGB':
        pass
    elif model == 'HSV' or model == 'HSL':
        for i in range(0, len(image)):
            for j in range(0, len(image[0])):
                if model == 'HSV':
                    func = rgb_to_hsv
                else:
                    func = rgb_to_hls
                    
                new_color = func(image[i][j][0],\
                                 image[i][j][1],\
                                 image[i][j][2])
                image[i][j] = new_color
    else:
        print "Error: Invalid model"
        return
        
    for i in range(0, len(image)):
        for j in range(0, len(image[0])):
            bin1, bin2, bin3 = col2bin(image[i][j], bins)
            histogram[bin1][bin2][bin3] += 1
    return histogram
    
def col2bin(color, bins):
    '''Return the data for bin in which the colorvalue should be stored.'''
    bin1 = int(color[0] * (bins[0] - 1))
    bin2 = int(color[1] * (bins[1] - 1))
    bin3 = int(color[2] * (bins[2] - 1))
    return (bin1, bin2, bin3)
