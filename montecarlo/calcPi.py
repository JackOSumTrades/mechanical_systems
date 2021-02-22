import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image as im
from math import cos, sin, pi, radians, sqrt

img = np.full((500,500,3), 255, dtype="uint8")
circR = 100
circ = cv2.circle(img,(250,250), circR, (0,0,255), 2)
# circ = cv2.rectangle(img,(150,150), (350,350), (255,0,0), 2)


n_points = 1000
nIn = 0
nOut =0 
for toss in range(0,n_points):
    x = random.uniform(150,350)
    y = random.uniform(150,350)
    dist = sqrt((x-250)**2+(y-250)**2)
    if dist < circR: # in circle
        (cv2.circle(img, (int(x),int(y)), 2, (255,0,0),-1))
        nIn +=1
    else:
        (cv2.circle(img, (int(x),int(y)), 2, (0,255,0),-1))
        nOut +=1
        
# circArea = pi*circR**2 # num in circle
# squareArea = 2**2*circR**2 # Num points
print(4*nIn/n_points)
cv2.imwrite("pi_calc_%d.jpg"%(n_points), img)

cv2.imshow("image",img)
cv2.waitKey()
