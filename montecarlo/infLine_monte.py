import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image as im
from math import cos, sin, pi, radians

class triggerLine():

    def __init__(self, bounds, length=5):
        self.collide = False
        self.color = (0,255, 0)
        
        self.x1 = random.uniform(0,bounds)
        self.y1 = random.uniform(0,bounds)
        
        self.start = (int(self.x1), int(self.y1))
        
        self.ang = random.uniform(0,360)
        
        self.x2 = self.x1+length*cos(radians(self.ang))
        self.y2 = self.y1+length*sin(radians(self.ang))
        
        self.end = (int(self.x2), int(self.y2))
        
        
    def __str__(self):
        return "<(%f, %f) -> ang: %f -> (%f, %f)>" % (self.x1, self.y1, self.ang, self.x2, self.y2)
        
    def draw(self, img, thickness =  1):    
        cv2.line(img, self.start, self.end, self.color,thickness)
    
    def isCollision(self, intersect_line):
        deltaX = self.x2-self.x1
        vals_greater = (intersect_line.vert_lines >= np.full(len(intersect_line.vert_lines),self.x1)  )
        vals_less =  ( intersect_line.vert_lines <= np.full(len(intersect_line.vert_lines),self.x2))
        # print(vals_greater)
        # print(vals_less)
        # print(intersect_line.vert_lines-np.full(len(intersect_line.vert_lines),self.x2))
        all_intersects = np.logical_xor(vals_greater,vals_less) #intersects are false
        
        self.collide =  not np.all(all_intersects) #if not all true then return that 'its true theres a collision'
        if self.collide:
            self.color = (0,0,255)
        
        return self.collide
class intersectLine():
    def __init__(self, bounds=500, n_lines=100):
        self.vert_lines = [int(x) for x in range(0,bounds, int(bounds/n_lines))]
        self.bounds = bounds
        
    def draw(self, img):
        for x in self.vert_lines:
            cv2.line(img, (x,self.bounds), (x,0), color=(255,0,0), thickness=1)
        

img = np.full((500,500,3), 255, dtype="uint8")

vertical_lines = intersectLine()


totalToss = 1000000
bars = [triggerLine(500) for x in range(0,totalToss)] # create tosses

numberIntersects = [bar.isCollision(vertical_lines) for bar in bars] # are there collision


numCollisions = sum(numberIntersects)
probCollide = numCollisions/totalToss
probMiss = 1- probCollide
print("Total number intersections: %d, total number tosses:%d" % (numCollisions, totalToss))
print("Probability of intersection: %f, probability of miss: %f" % (probCollide, probMiss))
vertical_lines.draw(img)

for bar in bars:
    bar.draw(img)

# img = im.fromarray(img,'RGB')
# img = cv2.imread(img)
#cv2.imwrite("results_%d.jpg"%(totalToss), img)
cv2.imshow("image",img)

cv2.waitKey()