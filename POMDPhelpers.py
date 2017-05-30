# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 13:00:23 2017

@author: ECOWIZARD
"""
import numpy as np
import math


class vectorLine():
    def __init__(self,vector1,vector2):
        self.vector1 = vector1
        self.vector2 = vector2
        
    def getPoint(self,point):
        print self.vector1
        print self.vector2
        print " ___"
        y = np.subtract(self.vector1,self.vector2)
        y = np.multiply(y,point)
        y = np.add(y,self.vector1)
        return y
       

def generateMDPfromPOMDP(States,Resolution):
    maximumUncertainty = 1/States
    #number of points is the number of states*(Resolution+1)
    PointVectors = []
    #Center of the two dimentional polygon this represents the point at which any state is equally likely.
    centroid = []
    #number of lines in the polygon.
    PrimaryPolygon = []
    for vector in range(0,States):#create a vector representation for each state.
        coordinate = []
        for State in range(0,States):
            centroid.append(maximumUncertainty) #create a centroid
            if State == vector:
                coordinate.append(1)
            else:
                coordinate.append(0)
        PointVectors.append(coordinate)
    
    PrimaryPolygon = getPolygonFrom(PointVectors) #this is the space that contains the entire co-MDP
    polypoints = getPolypoints(PrimaryPolygon,Resolution) #this splits each line in the polygon into a number of line segments eqaul to the resolution
    #print polypoints
    triangles =  getTriangles(polypoints,centroid) #this takes the line segments and creates a triangle by adding a centroid to each segment.
    ApproximatePOMDP = getBaseStates(triangles,Resolution) #this splits each trangle into a number of polygons eqaul to resolution. Each of these polygons represents a State the Agent can be in.
    return ApproximatePOMDP

def getPolygonFrom(PointVectors): #list of lists containing floats
    PrimaryPolygon = []
    for indx, point in enumerate(PointVectors):
        futurepoint = []
        if(indx >= len(PointVectors)-1):
            futurepoint = PointVectors[0]
        else:
            futurepoint = PointVectors[indx+1]
        vl = vectorLine(point,futurepoint)
        PrimaryPolygon.append(vl)
    return PrimaryPolygon
    

def getPolypoints(PrimaryPolygon,resolution): #list of vector lines, int
    polypoints = []
    for line in PrimaryPolygon:
        polypoints.append(line.vector1)
        for i in range(1,resolution): 
            polypoints.append(line.getPoint(i/resolution))            
        polypoints.append(line.vector2)
        
    return polypoints
def getTriangles(polypoints,centroid): #if the implementation of this changes it might affect getBaseStates creating a Triangle class would probably fix this
    triangles = []
    #print polypoints
    for inx, point in enumerate(polypoints):
        if inx == len(polypoints)-1:
            triangle = [point,polypoints[0],centroid]
        else:
            triangle = [point,polypoints[inx+1],centroid]
        triangles.append(triangle)
        
    #polytris = []
    #for pointtri in triangles:
     #   polytris.append(getPolygonFrom(pointtri))
    return triangles

def getBaseStates(triangles,resolution):#current implementation assumes that triangles are in a certain format. But the adherants of this format isn't gauranteed.
    States = []
    for triangle in triangles: #format assumed is [x1,x2,centroid] for all triangles
        print "error?"
        print triangle[2]
        line1 = vectorLine(triangle[2],triangle[0])
        line2 = vectorLine(triangle[2],triangle[1])
        States.append( [triangle[2],line1.getPoint(1/resolution),line2.getPoint(1/resolution) ])
        for i in range(1,resolution-2):
            States.append([line1.getPoint((i+1)/resolution),line2.getPoint((i+1)/resolution),line1.getPoint((i+2)/resolution),line2.getPoint((i+2)/resolution)])
        States.append( [line1.getPoint((resolution-1)/resolution),line2.getPoint((resolution-1)/resolution),triangle[0],triangle[1]])
        

def getpolygons(PrimaryPolygon, centroid,resolution):
    polypoints = getPolypoints(PrimaryPolygon,resolution)
    triangles = getTriangles(polypoints, centroid)
    baseStates = getBaseStates(triangles,resolution)
    return baseStates
 
def translateto2D(approximatePOMDP):
    newPOMDP = []
    for stateindx, state in enumerate(approximatePOMDP):
        for pointindx, point in enumerate(state):
            newPOMDP[stateindx,pointindx] = translateNDpointto2D(point)
    return newPOMDP

def translateNDpointto2D(point):
    centroid = getCentroidFromPoint(point)
    states = len(centroid)
    baserad = 2/states
    xcoord = ycoord = centroid[0]
    axis = []
    for axis in range(1,states+1):
        axis.append(baserad*axis)    
    for axis, probability in (axis,point):
        xcoord = xcoord + (probability - centroid[0]) * math.cos(axis*math.pi)
        ycoord = ycoord + (probability - centroid[0]) * math.sin(axis*math.pi)
    return [xcoord,ycoord]

def geCentroidFromPoint(point):
    return 1/len(point)
    
def isPointInside(convexPolygon,point): #assumes convexpolygon has already been transformed
    xypoint = translateNDpointto2D(point)
    triangles = getTriangles(convexPolygon,xypoint)
    tarea = 0
    area = getArea(convexPolygon)
    for triangle in triangles:
        tarea = tarea + getArea(triangle)
    if tarea > area:
        return False
    else:
        return True
    
def getArea(polygon):
    previous = len(polygon) -1 
    i = 0
    area = 0
    while i < len(polygon):
        area = area + (polygon[previous][0] + polygon[i][0]) * (polygon[previous][1] - polygon[previous][1])
        previous = i
        i += 1
    area = abs(area)
    return area/2




test = generateMDPfromPOMDP(4,3)
print test
    
    
    