from vpython import vec, quad, vertex, sphere, vector, color # Textbook said to use 'visual' but this package no longer exists for python 3
import numpy as np


class node:
    def __init__(self, position):
        self.col = color.blue
        self.vert = vertex(pos=vector(position[0], position[1], position[2]), normal=vector(0,0,1), color=self.col, shininess=0)
        
    
# make a square WxH divided into squares

H = W = 1
w =1
h = 50
dx = W/w
dy = H/h

verts = []
for y in range(h+1):
    verts.append([])
    for x in range(w+1):
        verts[y].append(node([-0.5+x*dx,-0.5+y*dy,0]))
        
        
for y in range(h):
    for x in range(w):
        quad(vs=[verts[y][x].vert, verts[y][x+1].vert, verts[y+1][x+1].vert, verts[y+1][x].vert])
