from vpython import box, rate, scene, vec, quad, vertex, sphere, vector, color # Textbook said to use 'visual' but this package no longer exists for python 3
import numpy as np
from math import pi, sqrt

class subscriptableArr:
    def __init__(self,arr):
        self.arr =arr
    def __getitem__(self, k):
        return self.arr[k]
    def __add__(self,otherBall):
        return self.arr + otherBall
class ball:
    def __init__(self, position,velocity, acceleration = np.array([0,-2*9.81,0]), col=color.blue):
        
        self.radius = 1 #m
        self.density = 8050 #kg/m^3 steel density
        self.youngs = 190 #GPa steel 
        self.poisson = 0.27 # steel 
        self.viscDamp = 1e-4 #http://help.solidworks.com/2016/english/solidworks/cworks/r_viscous_damping_ratios.htm
        
        self.acceleration = acceleration
        self.velocity = np.array(velocity)
        
        self.ball = sphere(radius=self.radius, pos=vector(position[0],position[1],position[2]),color=col)
        self.position = np.array(position)
        
    @property
    def position(self):
        return self._position
        
    @position.setter
    def position(self,val):
        val = np.array(val)
        self._position = val
        self.ball.pos = vector(val[0],val[1],val[2])
        
    def show(self):
        return self.ball
    
    def volume(self):
        return pi*self.radius**3
        
    def mass(self):
        return self.volume()*self.density
       
    def move(self, deltaT):
        # print(self.velocity*deltaT)
        self.position = self.position + self.velocity*deltaT + 0.5*self.acceleration*deltaT**2
        
        self.velocity = self.acceleration*deltaT + self.velocity
        
        # print(self.position, self.velocity)
        
        ## ADD MOVEMENT CONSTRAINTS - like gravity
        
    def idealCollision(self, otherBall):
        if ( np.linalg.norm(self.position)+np.linalg.norm(otherBall.position)- (self.radius+otherBall.radius)<= 0.0001):
            self.otherBall.color = color.blue
    
            collision_unit = (self.velocity-otherBall.velocity)/(np.linalg.norm(self.velocity-otherBall.velocity))
            a = 2*collision_unit*(self.velocity-otherBall.velocity)/((1/self.mass()+1/otherBall.mass()))
            #https://www.sjsu.edu/faculty/watkins/collision.htm
            self.velocity = self.velocity-a*collision_unit/(self.mass())
            otherBall.velocity = (otherBall.velocity-a*collision_unit/(-otherBall.mass()))
            
        return otherBall
class thick_plane:
    def __init__(self, position, length, height, width, col=color.blue):
        self.position = position
        self.length = length
        self.height = height
        self.width = width
        self.box = box(pos=vector(self.position[0], self.position[1], self.position[2]), length=self.length, height=self.height, width=self.width, color=col)
    def show(self):
        return self.box
    def idealMomentum(self, otherBall):
       
        newVal = abs(0.85*otherBall.velocity[1])
        if abs(newVal) >=0.2 :
           
            otherBall.velocity[1] = newVal
        else:
            otherBall.velocity[1] = 0
        
        return otherBall      
    def detectCollision(self,otherBall):
        # simplified cuz we know its only in y movement (as of this creation)
        # print(type(otherBall.position))
        # print(otherBall.position)
        
        ball_bottom = otherBall.position[1]-otherBall.radius
        plane_top  = self.position[1] + self.height/2
        
        plane_right = self.position[0]+self.length/2
        ball_mid_plane = otherBall.position[0]
        # print(plane_right, ball_mid_plane)
        # print(otherBall.position, plane_top)
        
        # Inside plane
        if plane_right >= ball_mid_plane: 
            if ball_bottom<plane_top :
                #collision detected
                #move ball to touch edge
                newPos = np.around(otherBall.position,5) # rounding errors removed
                newPos[1] = plane_top+otherBall.radius
                otherBall.position = newPos
                
                # deal with vertical momentum
                
                otherBall= self.idealMomentum(otherBall)
        
        return otherBall
        
       
from_floor = thick_plane([-4,4,0], length=8, height=16, width=4, col=color.blue)
   
   
to_floor = thick_plane([50,0,0], length=100, height=8, width=4, col=color.blue)

b1 = ball([0,13,0], [2,0,0],col=color.green)
b1.show()

for t in range(0,100000):
    rate(1000)
    b1.move(.001)
    b1 = from_floor.detectCollision(b1)
    b1 = to_floor.detectCollision(b1)
    print(b1.position[0])
    