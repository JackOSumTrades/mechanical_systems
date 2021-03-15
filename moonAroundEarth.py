from vpython import triangle, label, curve,simple_sphere ,box, rate, scene, vec, quad, vertex, sphere, vector, color # Textbook said to use 'visual' but this package no longer exists for python 3
import numpy as np
from math import pi, sqrt, sin, cos, radians, degrees, asin
import pandas as pd


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
        return position/10
        
    def getAcceleration(self, otherPoint):
        gravConst = 6.67430e-11
        
        direction =  otherPoint.position - self.position  
        
        dist = sqrt((self.position[0]-otherPoint.position[0])**2 + (self.position[1]-otherPoint.position[1])**2 + (self.position[2]-otherPoint.position[2])**2)
        
        F = gravConst*self.mass*otherPoint.mass/(dist**2)
        a = F/self.mass
        directionalAcceleration = a * (direction/dist)
        return directionalAcceleration
        
    
    def move(self, centerMass, deltaT):
        self.acceleration = self.getAcceleration(centerMass)
        self.position = self.position+ self.velocity*deltaT + self.acceleration*deltaT**2
        self.velocity = self.velocity + self.acceleration*deltaT
        # print(self.position, self.acceleration*deltaT**2)
        print(self.acceleration)
        self.ball.pos = vector(self.scaleSpace(self.position[0]),
                                                            self.scaleSpace(self.position[1]),
                                                            self.scaleSpace(self.position[2]))
        
        if abs(np.linalg.norm((centerMass.position - self.position))) - self.radius < centerMass.radius:
            print('Collision')
    def getNetAcceleration(self, particles):
        
        for particle in particles:
            netA += self.getAcceleration(particle)
        
        
        
centerMass = Particle(5.972e24,  [0,0,0],radius = 3e6,col=color.blue) 

satellite = Particle(0.07346e24, [0,384400e3,0],velocity=[1000,0,0], radius = 1.7e6)

print(sqrt(6.67430e-11*(5.972e24+1000)/(6.471e6)))
# print(satellite.getAcceleration(centerMass))

deltaT = 0
while True:
    deltaT = 10000
    centerMass.move(satellite,deltaT)
    satellite.move(centerMass,deltaT)
    rate(50)