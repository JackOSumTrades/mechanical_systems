from vpython import triangle, label, curve,simple_sphere ,box, rate, scene, vec, quad, vertex, sphere, vector, color # Textbook said to use 'visual' but this package no longer exists for python 3
import numpy as np
from math import pi, sqrt, sin, cos, radians, degrees, asin
import pandas as pd
import random


# If i decide to convert this to matplotlib, I can keep track of every previous position through chains of linkedlist and if they are one of the remaining N satellites, then I can draw the tails

class Particle:
    def __init__(self, mass, position, velocity=[0,0,0], radius = 3e6, col=color.white):
        self.radius = radius
        self.mass = mass
        self.position = np.array(position)
        
        self.acceleration = np.array([0,0,0])
        self.velocity = np.array(velocity)
        
        self.ball = simple_sphere(radius=radius, pos=vector(self.scaleSpace(self.position[0]),
                                                            self.scaleSpace(self.position[1]),
                                                            self.scaleSpace(self.position[2])), color=col)
    
    def scaleSpace(self, position):
        return position/250
        
        
    def dist(self, otherPoint):
        dist = sqrt((self.position[0]-otherPoint.position[0])**2 + (self.position[1]-otherPoint.position[1])**2 + (self.position[2]-otherPoint.position[2])**2)

        return dist
    def getAcceleration(self, otherPoint):
        gravConst = 6.67430e-11
        
        direction =  otherPoint.position - self.position  
        dist = self.dist(otherPoint)
        
        F = gravConst*self.mass*otherPoint.mass/(dist**2)
        a = F/self.mass
        directionalAcceleration = a * (direction/dist)
        return directionalAcceleration
        
    
    def move(self, centerMass, deltaT):
        self.acceleration = self.getAcceleration(centerMass)
        self.position = self.position+ self.velocity*deltaT + self.acceleration*deltaT**2
        self.velocity = self.velocity + self.acceleration*deltaT
        
        
            
        # print(self.position, self.acceleration*deltaT**2)
        # print(self.acceleration)
        self.ball.pos = vector(self.scaleSpace(self.position[0]),
                                                            self.scaleSpace(self.position[1]),
                                                            self.scaleSpace(self.position[2]))
        
        if np.linalg.norm(centerMass.position) + np.linalg.norm(self.position) - self.radius - centerMass.radius < 20000000:
            # print('Collision')
            self.velocity = (self.mass*self.velocity + centerMass.mass*centerMass.velocity)/(self.mass+centerMass.mass)
            self.mass += centerMass.mass
            centerMass.delete()
        return centerMass
    def distCheck(self, otherPoint):
        if self.dist(otherPoint)>10000e9:
            otherPoint.delete()
    def delete(self):
        self.mass = 0
        self.ball.visible = False
        
    def getNetAcceleration(self, particles):
        
        for particle in particles:
            netA += self.getAcceleration(particle)
        
        
        
sun = Particle(1.989e30,  [0,0,0],radius = 696.34e6,col=color.yellow) 

bodies = []
#make n planets
for body in range(0,1000):
    #mass mercury to Jupiter
    mass = random.uniform(3.285e23, 1.90e27)
    velocity = random.uniform(-48.87e3,48.87e3) - random.uniform(-3.7e3,3.7e3)
    velocity2 = velocity- random.uniform(-velocity,velocity)
    
    position = random.uniform(-3674.6e9, 3674.6e9) - random.uniform(-57.9e9,57.9e9)
    position2 = random.uniform(-3674.6e9, 3674.6e9) - random.uniform(-57.9e9,57.9e9)
    bodies.append(Particle(mass, [position,position2,0],velocity=[velocity,velocity2,0], radius = 300e6))

# print(sqrt(6.67430e-11*(5.972e24+1000)/(6.471e6)))
# print(satellite.getAcceleration(centerMass))

# deltaT = 0
while True:
    deltaT = 1000000
    # scene.capture("sun")  
    # centerMass.move(satellite,deltaT)
    for idx,body in enumerate(bodies):
        if body.mass == 0:
            continue
        for i in range(idx, len(bodies)):
            if bodies[i].mass == 0:
                continue
            if i == idx:
                continue
            # print(bodies[i].position,body.position)
            bodies[i] = body.move(bodies[i], deltaT)
        
        body.move(sun,deltaT)   
        sun.distCheck(body)
    num =0
    for body in bodies:
        if body.mass >0 :
            num += 1
     
    if num < 10:
        rate(100)
    elif num<20:
        rate(10000)
    else:
        rate(1000000)
      