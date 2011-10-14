# This is a program that executes either a affine or a perspective 
# transformation on a image.
#
# Authors: Jayke Meijer (6049885) and Richard Torenvliet (6138861)
from pylab import array, lstsq, imread, imshow, show, zeros, inv, dot, \
    subplot, plot, svd, shape
from interpolation import *

def affineTransform(image, x1, y1, x2, y2, x3, y3, M, N):
    # Construct the matrix M
    mat_M = array([[x1, y1, 1, 0, 0, 0], \
                   [0, 0, 0, x1, y1, 1], \
                   [x2, y2, 1, 0, 0, 0], \
                   [0, 0, 0, x2, y2, 1], \
                   [x3, y3, 1, 0, 0, 0], \
                   [0, 0, 0, x3, y3, 1]])
                   
    # Construct vector q
    q = array([[0], [0], [M], [0], [M], [N]])
    
    p = lstsq(mat_M, q)
    a, b, c, d, e, f =  p[0][0][0], \
                        p[0][1][0], \
                        p[0][2][0], \
                        p[0][3][0], \
                        p[0][4][0], \
                        p[0][5][0]
    
    # A is the resulting matrix that describes the transformation
    A = array([[a, b, c], \
               [d, e, f], \
               [0, 0, 1]])
    
    # Create the new image
    b = array([zeros(N, float)] * M)    
    for i in range(0, M):
        for j in range(0, N):
            old_coor = dot(inv(A),([[i],[j],[1]]))
            b[i][j] = pV(image, old_coor[0][0], old_coor[1][0], 'linear')
    
    return b
    
def perspectiveTransform(image, x1, y1, x2, y2, x3, y3, x4, y4, M, N):
    # Construct the matrix M
    x1_a, y1_a = 0, 0
    x2_a, y2_a = M, 0
    x3_a, y3_a = M, N
    x4_a, y4_a = 0, N
    
    mat_M = array([[x1, y1, 1, 0,  0,  0, -x1_a * x1, -x1_a * y1, -x1_a], \
                   [0,  0,  0, x1, y1, 1, -y1_a * x1, -y1_a * y1, -y1_a], \
                   [x2, y2, 1, 0,  0,  0, -x2_a * x2, -x2_a * y2, -x2_a], \
                   [0,  0,  0, x2, y2, 1, -y2_a * x2, -y2_a * y2, -y2_a], \
                   [x3, y3, 1, 0,  0,  0, -x3_a * x3, -x3_a * y3, -x3_a], \
                   [0,  0,  0, x3, y3, 1, -y3_a * x3, -y3_a * y3, -y3_a], \
                   [x4, y4, 1, 0,  0,  0, -x4_a * x4, -x4_a * y4, -x4_a], \
                   [0,  0,  0, x4, y4, 1, -y4_a * x4, -y4_a * y4, -y4_a]])
    
    # Get the vector p and the values that are in there by taking the SVD. 
    # Since D is diagonal with the eigenvalues sorted from large to small on
    # the diagonal, the optimal q in min ||Dq|| is q = [[0]..[1]]. Therefore, 
    # p = Vq means p is the last column in V.
    U, D, V = svd(mat_M)
    p = V[8][:]                
    a, b, c, d, e, f, g, h, i = p[0], \
                                p[1], \
                                p[2], \
                                p[3], \
                                p[4], \
                                p[5], \
                                p[6], \
                                p[7], \
                                p[8]
    
    # P is the resulting matrix that describes the transformation
    P = array([[a, b, c], \
               [d, e, f], \
               [g, h, i]])
    
    # Create the new image
    b = array([zeros(M, float)] * N)
    for i in range(0, M):
        for j in range(0, N):
            or_coor = dot(inv(P),([[i],[j],[1]]))
            or_coor_h = or_coor[1][0] / or_coor[2][0], \
                      or_coor[0][0] / or_coor[2][0]
            b[j][i] = pV(image, or_coor_h[0], or_coor_h[1], 'linear')
    
    return b

def test_affine():
    # Defining the points to use. The first 3 are entered in the affineTransform
    # function, the last 2 are just used for the drawing of the yellow lines
    points_x = [0, 100, 200, 100, 0]    
    points_y = [100, 0, 100, 200, 100]

    # Get the image
    a = imread('cameraman.png')
    subplot(121)

    # Draw the lines
    plot(points_x, points_y, 'y-')
    imshow(a,vmin=0,vmax=1,cmap="gray")

    # Calculate and show the new image
    subplot(122)
    b = affineTransform(a, points_x[0], points_y[0], 
                           points_x[1], points_y[1], 
                           points_x[2], points_y[2], 50, 50)
    imshow(b,vmin=0,vmax=1,cmap="gray")
    show()
    
def test_perspective():
    # Defining the points to use. The first 4 are entered in the 
    # persectiveTransform function, the last is just used for the drawing of
    # the yellow lines, and is the same as the first
    points_x = [147, 100, 300, 392, 147]    
    points_y = [588, 370, 205, 392, 588]
    #points_x = [570, 821, 590, 346, 570]    
    #points_y = [186, 170, 590, 558, 186]

    # Get the image
    a = imread('flyeronground.png')
    a = rgb2gray(a)
    subplot(121)

    # Draw the lines
    plot(points_x, points_y, 'y-')
    imshow(a,vmin=0,vmax=1,cmap="gray")

    # Calculate and show the new image
    subplot(122)
    b = perspectiveTransform(a, points_x[0], points_y[0], 
                                points_x[1], points_y[1], 
                                points_x[2], points_y[2],
                                points_x[3], points_y[3], 300, 200)
    imshow(b,vmin=0,vmax=1,cmap="gray")
    show()
    
def rgb2gray(im):
	return ((im[:,:,0]+im[:,:,1]+im[:,:,2])/3)

#test_affine()
test_perspective()
