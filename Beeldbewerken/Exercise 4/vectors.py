# Authors: Jayke Meijer (6049885) and Richard Torenvliet (6138861)
from pylab import *
x = arange(-100,101)
y = arange(-100,101)

xx = arange(-100,101,10)
yy = arange(-100,101,10);

Y,X = meshgrid(x,y)

YY, XX = meshgrid(yy,xx);

A = 1; B = 2; V = 6*pi/201; W = 4*pi/201;

F = A*sin(V*X) + B*cos(W*Y)
#f(x,y)=Asin(Vx)+Bcos(Wy)
Fx = A * V * cos(V * X)
Fy = -(B * W * sin(W * Y))

FFx = -A * V ** 2 * sin(V * XX)

FFy = -B * W ** 2 * cos(W * YY)
clf();
subplot(133)
imshow(F, cmap='gray', extent=(-100, 100, -100, 100));
quiver( yy, xx, FFy, -FFx, color='red')
subplot(131)
imshow(Fx, cmap='gray')
subplot(132)
imshow(Fy, cmap='gray')

#imshow(F, cmap=cm.gray)
show()
