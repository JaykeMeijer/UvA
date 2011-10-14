from pylab import *

# Filter version 1
def linfilter1(f, w):
  g = empty(f.shape, dtype=f.dtype)  # the resulting image
  M,N = f.shape
  K,L = (array(w.shape)-1)/2

  def value(i,j):
    """The function returning the value f[i,j] in case
    (i,j) in an index 'in the image', otherwise it return 0"""
    if i<0 or i>=M or j<0 or j>=N:
      return 0
    return f[i,j]

  for j in xrange(N):
    for i in xrange(M):
      summed = 0
      for k in xrange(-K,K+1):
        for l in xrange(-L,L+1):
          summed += value(i+k,j+l) * w[k+K,l+L]
      g[i,j] = summed
  return g

# Filter version 2
def linfilter2(f, w):
  """Linear Correlation based on neigborhood processing without loops"""
  g = empty(f.shape, dtype=f.dtype)
  M,N = f.shape
  K,L = (array(w.shape)-1)/2

  for j in xrange(N):
    for i in xrange(M):
      ii = minimum(M-1, maximum(0, arange(i-K, i+K+1)))
      jj = minimum(N-1, maximum(0, arange(j-L, j+L+1)))
      nbh = f[ ix_(ii,jj) ]
      g[i,j] = ( nbh * w ).sum()
  return g

# Filter version 3
def linfilter3(f, w):
  """Linear Correlation using Translates of Images"""

  M,N = f.shape
  K,L = (array(w.shape)-1)/2

  di,dj = meshgrid(arange(-L,L+1), arange(-K,K+1))
  didjw = zip( di.flatten(), dj.flatten(), w.flatten() )
  
  def translate(di,dj):
    ii = minimum(M-1, maximum(0, di+arange(M)))
    jj = minimum(N-1, maximum(0, dj+arange(N)))
    return f[ ix_(ii, jj) ]

  r = 0*f;
  for di, dj, weight in didjw:
    r += weight*translate(di,dj)
  return r

# Filter version 4
def linfilter4(f, w):
  return correlate(f, w, mode='nearest')
