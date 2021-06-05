from vpython import triangle, label, curve,simple_sphere ,box, rate, scene, vec, quad, vertex, sphere, vector, color # Textbook said to use 'visual' but this package no longer exists for python 3
import numpy as np
from math import pi, sqrt, sin, cos, radians, degrees, asin
import pandas as pd



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
        if abs(np.round(self.z, 2)) == r:
            self.endpoint = True
            #End node
        else:
            self.endpoint = False
        # self.label = label( pos=self.vector, text=str(np.around(degrees(self.theta),2))+" "+str(degrees(self.azimuth)) ) 
        # self.label = label( pos=self.vector, text=str(hash(self)) ) 
        # self.label = label( pos=self.vector, text=str(np.round(self.z,8)) ) 
        # self.ball = simple_sphere(radius=0.01, pos=vector(self.x,self.y,self.z), color=col)
    def calcDist(self,otherNode):
        dist = 2*self.r*asin((sqrt( (self.x-otherNode.x)**2 + (self.y-otherNode.y)**2 + (self.z-otherNode.z)**2))/(2*self.r))
       
        if np.round(otherNode.z,8) == np.round(self.z,8):
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
        if (degrees(self.theta) == 0.) or (degrees(self.theta) ==360.):
            sTh = str(degrees(360))
        else:
            sTh = str(degrees(self.theta))
            
        s = sTh+"-"+str(degrees(self.azimuth))
        return int.from_bytes(s.encode(), 'little')
        
class Graph:
    def __init__(self, N_step_Az,N_step_Th):
        self.adjacencylist= {}
        self.edges = []
        self.quads = []
        self.triags = []
        self.N_step_Az = N_step_Az
        self.N_step_Th = N_step_Th
    def add_node(self, node):
        
        if str(hash(node)) in self.adjacencylist:
            newNode = True
            for prevNode in self.adjacencylist:
                if degrees(prevNode[0].theta) == degrees(node.theta) and degrees(prevNode[0].azimuth) == degrees(node.azimuth) :
                    newNode = False
                    del node
                    break
            if newNode:
                self.adjacencylist[str(hash(node))] = [node]
        
        else:
            # print(degrees(node.theta), degrees(node.azimuth))
            self.adjacencylist[str(hash(node))] = [node]
    
    def add_neighbors(self,thisNodeKey, otherNodeKeys):
    
        otherNodeKeys = [otherNodeKeys[0]['key'],otherNodeKeys[1]['key'],otherNodeKeys[2]['key'],otherNodeKeys[3]['key'] ]
        
        thisNode=self.adjacencylist[thisNodeKey][0]
        for idx, key in enumerate(otherNodeKeys):
            if self.adjacencylist[key][0] not in self.adjacencylist[thisNodeKey]:
                self.adjacencylist[thisNodeKey].append(self.adjacencylist[key][0])
                
            if self.adjacencylist[thisNodeKey][0] not in self.adjacencylist[key]:
                self.adjacencylist[key].append(self.adjacencylist[thisNodeKey][0])
                
    def add_edge_neighbors(self,thisNodeKey, otherNodeKeys):
    
  
        thisNode=self.adjacencylist[thisNodeKey][0]
        for idx, key in enumerate(otherNodeKeys):
            if self.adjacencylist[key][0] not in self.adjacencylist[thisNodeKey]:
                self.adjacencylist[thisNodeKey].append(self.adjacencylist[key][0])
                
            if self.adjacencylist[thisNodeKey][0] not in self.adjacencylist[key]:
                self.adjacencylist[key].append(self.adjacencylist[thisNodeKey][0])
                    
        # print((self.adjacencylist))
    def make_edges(self):
        for nodeKey in self.adjacencylist:
            closestNodes = []
            for otherNodeKey in self.adjacencylist:
                if hash(nodeKey) == hash(otherNodeKey):
                    pass # this is the same node
                else:
                    dist,thisType = self.adjacencylist[nodeKey][0].calcDist(self.adjacencylist[otherNodeKey][0])
                    
                    closestNodes.append({'dist':dist,'key':otherNodeKey, 'type':thisType, 'z':self.adjacencylist[otherNodeKey][0].z })
                    
            closestNodes = sorted(closestNodes, key=lambda i : (i['type'], i['dist']))     
            
            closestNodeInplane = [node for node in closestNodes if node['type'] =='onPlane']
            closestNodeOutplane = [node for node in closestNodes if node['type'] =='outPlane']
            # self.add_neighbors(nodeKey,[closestNodeInplane[0], closestNodeInplane[1], closestNodeOutplane[0], closestNodeOutplane[1]])
            # print(closestNodeInplane)
            # print(closestNodeOutplane)
            #End Node
            if len(closestNodeInplane) == 0 :
                # print(closestNodeInplane)
                # print(nodeKey)
                otherNodeKeys = [node['key'] for node in closestNodeOutplane]
                otherNodeKeys = otherNodeKeys[0:2*self.N_step_Az]
                
                self.add_edge_neighbors(nodeKey,otherNodeKeys)
                # input()
            else: #interior node
                self.add_neighbors(nodeKey,[closestNodeInplane[0], closestNodeInplane[1], closestNodeOutplane[0], closestNodeOutplane[1]])

    def draw_edges(self):
    
        lines_drawn = []
        for nodeKey in self.adjacencylist:
            thisNode=self.adjacencylist[nodeKey][0]
            # print(self.adjacencylist[nodeKey])

            for idx,otherNodeKey in enumerate(self.adjacencylist[nodeKey]):
                if idx == 0:
                    continue
                    
                thisLine = tuple(sorted([otherNodeKey, nodeKey], key=lambda i: str(i)))
                
                if thisLine in lines_drawn:
                    continue
                lines_drawn.append(thisLine)
                # if idx>1:
                     # self.edges.append(curve(thisNode.vector,otherNode.vector, color=color.blue))
                # else:
                otherNode = self.adjacencylist[str(otherNodeKey)][0]
                self.edges.append(curve(thisNode.vector,otherNode.vector))
                    
    def get_fourth_vert(self, centerNodeKey, leftNodeKey, rightNodeKey):
        rightKeys = self.adjacencylist[str(rightNodeKey)]
        leftKeys = self.adjacencylist[str(leftNodeKey)]
        
        toReturn = list((set(rightKeys) & set(leftKeys)))
        toReturn.remove(centerNodeKey)
                
        return ( toReturn )
                    
    def draw_quads(self):
    
        # self.get_fourth_vert(self.adjacencylist[nodeKey][0],self.adjacencylist[nodeKey][3],self.adjacencylist[nodeKey][2])
        visited = []
        visited_triags = []
        for idx_1, nodeKey in enumerate(self.adjacencylist):
            
            if self.adjacencylist[str(nodeKey)][0].endpoint:
                thisNodeList = self.adjacencylist[(nodeKey)]
                thisNodeList = sorted(thisNodeList, key = lambda n: (n.theta, n.azimuth))
                # sorted_thet = sorted(self.adjacencylist[(nodeKey)], key=lambda n: n.
                # print('This is an endpoint')
                for idx_2 in range(1,len(thisNodeList)):
                    # for idx_3 in range(idx_2,len(thisNodeList)):
                    if idx_2 == len(thisNodeList)-1:
                        next = 1
                    else:
                        next = idx_2+1
                    points = [self.adjacencylist[str(nodeKey)][0],thisNodeList[idx_2], thisNodeList[next]]
                    points = tuple(sorted(points, key=lambda i: str(i)))
                    
                    if points in visited:
                        # print('continuing')
                        continue
                    visited_triags.append(points)
                    a=vertex(pos=self.adjacencylist[str(nodeKey)][0].vector, color=color.red)
                    b=vertex(pos=self.adjacencylist[str(nodeKey)][idx_2].vector)
                    c=vertex(pos=self.adjacencylist[str(nodeKey)][next].vector)
                    self.triags.append(triangle(vs=[b,a,c]))
                    # input()
                
                continue
            for idx_2 in range(1,len(self.adjacencylist[(nodeKey)])):
                
                if self.adjacencylist[str(nodeKey)][idx_2].endpoint:
                    # print('This is an endpoint')
                    continue
                
                for idx_3 in range(idx_2,len(self.adjacencylist[(nodeKey)])):
                    if self.adjacencylist[str(nodeKey)][idx_3].endpoint:
                        # print('This is an endpoint')
                        continue
                    thirdNeighbors = self.get_fourth_vert(self.adjacencylist[str(nodeKey)][0],self.adjacencylist[str(nodeKey)][idx_2],self.adjacencylist[str(nodeKey)][idx_3])
                    if len(thirdNeighbors)==1:
                        
                        for item in thirdNeighbors:
                            if item.endpoint:
                                # print('This is an endpoint')
                                continue
                                
                            points = [item,self.adjacencylist[str(nodeKey)][0],self.adjacencylist[str(nodeKey)][idx_2], self.adjacencylist[str(nodeKey)][idx_3]]
                            points = tuple(sorted(points, key=lambda i: str(i)))
                            
                            if points in visited:
                                # print('continuing')
                                continue
                            
                            # print(points)   
                            visited.append(points)
                            a=vertex(pos=self.adjacencylist[str(nodeKey)][0].vector, color=color.red)
                            b=vertex(pos=self.adjacencylist[str(nodeKey)][idx_2].vector)
                            c=vertex(pos=self.adjacencylist[str(nodeKey)][idx_3].vector)
                            d=vertex(pos=self.adjacencylist[str(item)][0].vector)
                            
                            det= np.array([self.adjacencylist[str(nodeKey)][0].position,
                                      self.adjacencylist[str(nodeKey)][idx_2].position,
                                      self.adjacencylist[str(nodeKey)][idx_3].position,
                                      self.adjacencylist[str(item)][0].position])
                            
                            det = np.append(det, np.array([1,1,1,1])).reshape((4,4))
                            # print(det)
                            
                            # print(det.size)
                            # print(np.linalg.det(det))
                            # visited.append(item)
                            self.quads.append(quad(vs=[b,a,c,d]))
                            print(self.adjacencylist[str(nodeKey)][0], self.adjacencylist[str(nodeKey)][idx_2], self.adjacencylist[str(nodeKey)][idx_3],self.adjacencylist[str(item)][0] )
                            # input()
                            
                            
    def delete(self, key):
        if hasattr(self.adjacencylist[key][0], 'label'):
            self.adjacencylist[key][0].label.visible = False
            del self.adjacencylist[key][0].label
        del self.adjacencylist[key]
    
    def remove_duplicates(self):
        
        nodes = [self.adjacencylist[node][0] for node in self.adjacencylist]
        
        nodes_obj = sorted(nodes, key=lambda node: ((node.x), (node.y), (node.z)))
        
        nodes = [((node.x), (node.y), (node.z)) for node in nodes_obj ]
        nodes = np.round(nodes,8)
        nodes[nodes==0.] = 0.
        
        validPositions = []
        idices_to_delete = []
        for idx, node in enumerate(nodes):
            node = tuple(node)
            if node in validPositions:
                idices_to_delete.append(idx)
                continue
            validPositions.append(node)
        idices_to_delete.sort(reverse=True)
        
        
        # out =pd.DataFrame(nodes)
        # out.columns = ['x','y','z']
        # out.sort_values(by=['x', 'y'])
        # print(out)
        
        for idx in idices_to_delete:
            self.delete(str(nodes_obj[idx]))
        
        nodes = [self.adjacencylist[node][0] for node in self.adjacencylist]
        nodes_obj = sorted(nodes, key=lambda node: ((node.x), (node.y), (node.z)))
        nodes = [((node.x), (node.y), (node.z)) for node in nodes ]
        out =pd.DataFrame(nodes)
        out.columns = ['x','y','z']
        out.sort_values(by=['x', 'y'])
        out['name']=nodes_obj
        print(out)
r = 0.25
N_step_Az = 20
N_step_Th = 20

g = Graph(N_step_Az,N_step_Th)
for idx,theta in enumerate(np.linspace(0,2*pi, N_step_Th+1)):#needs be odd [will generate (Nsteps-1) points on azimuth line
    if idx ==0 :
        continue
    for idy, azimuth in enumerate(np.linspace(0,pi,N_step_Az+1)): #needs be odd   (will generate 2*(Nsteps-1) lines from the poles
        if idy ==0 :
            continue
   
        g.add_node(Node(r,theta,azimuth)) 
            
g.remove_duplicates()
g.make_edges()  
g.draw_edges()
# print(g.adjacencylist['160472915'])
g.draw_quads()

# quads[10].vs[0].color = color.red     
# quads[10].vs[1].color = color.red    
# quads[10].vs[2].color = color.red    
# quads[10].vs[3].color = color.red    