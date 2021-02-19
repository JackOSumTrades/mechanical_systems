from vpython import box, rate, scene, vec, quad, vertex, sphere, vector, color # Textbook said to use 'visual' but this package no longer exists for python 3
import numpy as np
from math import pi, sqrt

class ball:
    def __init__(self, position,velocity, col=color.blue):
        self.velocity = velocity
        self.radius = 1 #m
        self.density = 8050 #kg/m^3 steel density
        self.youngs = 190 #GPa steel 
        self.poisson = 0.27 # steel 
        self.viscDamp = 1e-4 #http://help.solidworks.com/2016/english/solidworks/cworks/r_viscous_damping_ratios.htm
        self.position = position
        self.ball = sphere(radius=self.radius, pos=vector(self.position[0],self.position[1],self.position[2]),color=col)
    def show(self):
        return self.ball
    
    def volume(self):
        return pi*self.radius**3
        
    def mass(self):
        return self.volume()*self.density
       
    def move(self, deltaT):
        self.position = self.position+self.velocity*deltaT
        self.ball.pos = vector(self.position[0],self.position[1],self.position[2])
        
    def idealCollision(self, ball):
        if ( np.linalg.norm(self.position)+np.linalg.norm(ball.position)- (self.radius+ball.radius)<= 0.0001):
            self.ball.color = color.blue
    
            collision_unit = (self.velocity-ball.velocity)/(np.linalg.norm(self.velocity-ball.velocity))
            a = 2*collision_unit*(self.velocity-ball.velocity)/((1/self.mass()+1/ball.mass()))
            #https://www.sjsu.edu/faculty/watkins/collision.htm
            self.velocity = self.velocity-a*collision_unit/(self.mass())
            ball.velocity = (ball.velocity-a*collision_unit/(-ball.mass()))
            
        return ball
        
b1 = ball(np.array([-2,0,0]), np.array([1,0,0]),col=color.green)
b1.show()

b2= ball(np.array([2,2,0]), np.array([-1,-1,0]),col=color.red)
b2.show()
#b2 = ball([1,0,0], [-1,0,0]).show()
for deltT in np.linspace(0,5,10000):
    scene.waitfor('redraw')
    b1.move(deltT)
    b2.move(deltT)
    b2 = b1.idealCollision(b2)
    
    if (np.linalg.norm(b1.position)+np.linalg.norm(b2.position) > 6):
        break