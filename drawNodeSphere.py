from vpython import curve,simple_sphere ,box, rate, scene, vec, quad, vertex, sphere, vector, color # Textbook said to use 'visual' but this package no longer exists for python 3
import numpy as np
from math import pi, sqrt, sin, cos, radians, degrees, asin




class Node:

    def __init__(self,r,theta,azimuth, col=color.blue):
        self.r = r
        self.theta = (theta) 
        self.azimuth = (azimuth)
        
        self.x = r*sin(self.theta)*cos(self.azimuth)
        self.y = r*sin(self.theta)*sin(self.azimuth)
        self.z = r*cos(self.theta)
        
        self.position = [self.x,self.y,self.z]
        
        self.vector = vector(self.x,self.y,self.z)
            
        # self.ball = simple_sphere(radius=0.01, pos=vector(self.x,self.y,self.z), color=col)
    def calcDist(self,otherNode):
        dist = 2*self.r*asin((sqrt( (self.x-otherNode.x)**2 + (self.y-otherNode.y)**2 + (self.z-otherNode.z)**2))/(2*self.r))
        if otherNode.azimuth == self.azimuth:
            thisType = 'onPlane'
        else:
            thisType = 'outPlane'
        
        return dist,thisType
    
    def __str__(self):
        return str(hash(self))
    def __repr__(self):
        # return '(%f, %f)'%( degrees(self.theta), degrees(self.azimuth))
       return str(hash(self))
    def __hash__(self):
        s = (str(degrees(self.theta))+"-"+str(degrees(self.azimuth)))
        return int.from_bytes(s.encode(), 'little')
        
class Graph:
    def __init__(self):
        self.adjacencylist= {}
        self.edges = []
    def add_node(self, node):
        if str(hash(node)) in self.adjacencylist:
            pass
        else:
            self.adjacencylist[str(hash(node))] = [node]
    
    def add_neighbors(self,thisNodeKey, otherNodeKeys):
    
        otherNodeKeys = [otherNodeKeys[0]['key'],otherNodeKeys[1]['key'],otherNodeKeys[2]['key'],otherNodeKeys[3]['key'] ]
        
        thisNode=self.adjacencylist[thisNodeKey][0]
        for idx, key in enumerate(otherNodeKeys):
            if self.adjacencylist[key][0] not in self.adjacencylist[thisNodeKey]:
                self.adjacencylist[thisNodeKey].append(self.adjacencylist[key][0])
            if self.adjacencylist[thisNodeKey][0] not in self.adjacencylist[key]:
                self.adjacencylist[key].append(self.adjacencylist[thisNodeKey][0])
            
            otherNode = self.adjacencylist[key][0]
            if idx>1:
                 self.edges.append(curve(thisNode.vector,otherNode.vector, color=color.blue))
            else:
                self.edges.append(curve(thisNode.vector,otherNode.vector))
            
    def make_edges(self):
        for nodeKey in self.adjacencylist:
            closestNodes = []
            for otherNodeKey in self.adjacencylist:
                if hash(nodeKey) == hash(otherNodeKey):
                    pass # this is the same node
                else:
                    dist,thisType = self.adjacencylist[nodeKey][0].calcDist(self.adjacencylist[otherNodeKey][0])
                    
                    closestNodes.append({'dist':dist,'key':otherNodeKey, 'type':thisType})
                    
            closestNodes = sorted(closestNodes, key=lambda i : (i['type'], i['dist']))     
            
            closestNodeInplane = [node for node in closestNodes if node['type'] =='onPlane']
            closestNodeOutplane = [node for node in closestNodes if node['type'] =='outPlane']
            self.add_neighbors(nodeKey,[closestNodeInplane[0], closestNodeInplane[1], closestNodeOutplane[0], closestNodeOutplane[1]])
            
r = 0.25
g = Graph()
for theta in np.linspace(0,2*pi, 11):#needs be odd
    for azimuth in np.linspace(0,pi,7): #needs be odd
        if theta == 0.0 or azimuth == 0.0:
            pass
        else:
        # peek at other nodes
            n1 = Node(r,theta,azimuth)
            g.add_node(n1) 
        
g.make_edges()  
quads =[]      
for i in g.adjacencylist:
    thisQuad =[]
    for idx, j in enumerate(g.adjacencylist[i]):
        
        if idx == 0:
            continue
        thisQuad.append(vertex(pos=j.vector, color=color.blue, shininess=0))
    if len(thisQuad)>4:
        continue
    quads.append(quad(vs=thisQuad))    
        # edges.append(curve(v1,v2))
quads[10].vs[0].color = color.red     
quads[10].vs[1].color = color.red    
quads[10].vs[2].color = color.red    
quads[10].vs[3].color = color.red    