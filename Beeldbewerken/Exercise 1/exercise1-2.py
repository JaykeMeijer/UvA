from time import time
from pylab import *
from scipy.ndimage.interpolation import zoom;
import linfilters


# Time each version
results = [[zeros(9, float)], [zeros(9, float)], [zeros(9, float)], [zeros(9, float)]]
image = imread('cameraman.png')


# Time first filter
result = 0
#for i in range(3, 12):
for j in range(0,3):
    start = time()
    linfilters.linfilter1(image, ones((5,5))/25)
    result = result + time() - start
    print result / (j+1)
#results[1[i - 3]]
    
print results
