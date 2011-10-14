from pylab import *
#Stop fucking around
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
Fy = -(B * W * sin(W * X))

FFx = -A * V ** 2 * sin(V * XX)  # this is soo wrong....

FFy = -B * W ** 2 * cos(W * YY) # this is also wrong
clf();
subplot(131)
imshow(F, cmap='gray', extent=(-100, 100, -100, 100));
quiver( yy, xx, FFy, -FFx, color='red')
subplot(132)
imshow(Fx, cmap='gray')
subplot(133)
imshow(Fy, cmap='gray')

#imshow(F, cmap=cm.gray)
show()
