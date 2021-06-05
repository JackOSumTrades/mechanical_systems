import cv2
import numpy as np
from math import pi,sqrt

# The purpose of this file is to crate a simulation of a bacterium that exhibits all 7 traits of life to serve as a thought experiment regarding what it means to be alive
# MUST INCLUDE:
    # Growth and Development
    # Response to the environment
    # Reproduce offspring
    # Heredity of traits
    # Homeostasis (stable inner conditions)
    # Metabolism (energy from chemical reactions)
    # Cellular structure and composition
    # Adaption through evolution
    
class Bacteria:
    def __init__(self, start_x=int(512/2), start_y=int(512/2), radius=10, maxMovement=10, color=(255,0,0)):
        
        self.x = start_x
        self.y = start_y
        self.radius = radius
        
        self.movementDrive = [0,0]
        self.maxMovement = maxMovement
        self.col = color
        
        self.exists = True
    def live(self, environment):
        for var in environment:
            if self is var:  
                continue  
            if var.radius < self.radius:
                
                self.considerMovement(var)
        self.move()    
        environment = self.detectOverlap(environment)
        environment = self.cleanEnvironment(environment)
        
        return environment
    def considerMovement(self, environmentVariable):
        print('Considering movement')
        self.movementDrive[0] += environmentVariable.x - self.x 
        self.movementDrive[1] += environmentVariable.y - self.y
        # print(self.movementDrive)
        
    def move(self):
        print('Moving')
        normMovDrive = [0,0]
        for idx, val in enumerate(self.movementDrive):
            
            if abs(val) > self.maxMovement:
                normMovDrive[idx] = np.sign(val)*self.maxMovement
            else:
                normMovDrive[idx] = val
                
        self.x += int(normMovDrive[0])
        self.y += int(normMovDrive[1])
        self.movementDrive = [0,0]
        
    def isOverlap(self, environmentVariable):
        squaredDist = (self.x - environmentVariable.x)**2 +(self.y - environmentVariable.y)**2
        # print(squaredDist, (self.radius + environmentVariable.radius)**2)
        if squaredDist == (self.radius + environmentVariable.radius)**2:
            # circles touch
            return False
        elif squaredDist > (self.radius + environmentVariable.radius)**2:
            # not touching
            return False
        else:
            return True #intersection
            
    def getVolume(self):
        return pi*self.radius**2    
        
    def draw(self, img):
        if self.exists:
            img = cv2.circle(img, (self.x, self.y), int(self.radius), self.col,-1)
        return img
    
    def detectOverlap(self, environment):
        for var in environment:
            if self is var:  
                continue 
            if self.isOverlap(var):
                if self.radius>var.radius:
                    self.radius = sqrt((self.getVolume()+var.getVolume())/(pi))
                    var.exists = False
                else:
                    var.radius = sqrt((self.getVolume()+var.getVolume())/(pi))
                    self.exists = False
        return environment           
     
    def cleanEnvironment(self,environment):
        environment = sorted(environment, key=lambda x: x.exists, reverse=True)
        environment = [x for x in environment if x.exists]
        return environment
def main(): 
    environment = []

    b1 = Bacteria()
    environment.append(b1)

    b2 = Bacteria(start_x = 100, start_y = 100,radius=5, color=(0,255,0))
    environment.append(b2)

    while True:
        img = np.full((512,512,3), 255, np.uint8)
        environment = b1.live(environment)
        for i in environment:
            img = i.draw(img)
        
        cv2.imshow('image', img)
        k = cv2.waitKey(0)
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()
            break
            
            
if __name__ == '__main__':
    main()