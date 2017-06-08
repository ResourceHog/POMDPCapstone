# -*- coding: utf-8 -*-
"""
Created on Sun Apr 09 19:37:17 2017





@author: Travis Rivera
"""

#this is a bunch of classes that I use for 

import numpy as np
from collections import OrderedDict
#represents a line defined as two vectors (which are represented as a numpy aray.) getPoint()
# is used to also get arbitrary points on this line.
class vectorLine():
    def __init__(self,vector1,vector2):
        self.vector1 = vector1#this makes it so that the input for getPoint is a positive number representing the percentage of distance from vector1 to vector 2.
        self.vector2 = vector2
        
    def getPoint(self,point):                           #this function gets the point that is some fraction between the two vectors. where this fraction
                                                        #is determined by the point variable.

        y = np.subtract(self.vector1,self.vector2)
        y = np.multiply(y,point)                       
        y = np.add(y,self.vector1)                     
        return y
    
class Polygon():
    def __init__(self, coords):
        self.coords = coords
    #this algorithm should get the area of any polygon that does not intersect itself. Which is more than I need but there is no point in searching for a less general algorithm.
    def getArea(self):
        previous = len(self.coords) -1 
        i = 0
        area = 0
        while i < len(self.coords):
            area = area + ( self.coords[i][0]+ self.coords[previous][0] ) * (self.coords[i][1] - self.coords[previous][1])
            previous = i
            i += 1
        area = abs(area)
        return area/2

        
class Triangle(Polygon): #inherits getArea from polygon.
    def __init__(self,point,point2,centroid):
        coords = [point,point2,centroid]
        Polygon.__init__(self,coords)
        

#this converts a any POMDP (that uses a certain interface) into a CO-MDP then converts this CO-MDP to an MDP that can be arbitrarily close as the resolution is higher
#as the resolution gets higher it gets harder to compute a solution because the amount of states it needs to acount for explodes.
#after it is converted to an MDP i can throw Q-learning at it and it will find a useful policy.
class POMDPEnvironmentConverter():
    def __init__(self, env, Resolution):
        self.States = env.getStates() # an ordered dictionary
        self.Resolution = Resolution # integer value
        self.pomdpStates = self.generateMDPfromPOMDP(len(self.States))
        self.environment = env
        self.reset()
            
    def getState(self):
        for state in self.pomdpStates:
            triangles = self.getTriangles(state.coords,self.currentBelief)
            sumtriangles = 0
            for triangle in triangles:
                sumtriangles += triangle.getArea()
            if state <= sumtriangles:
                return state
            
        return None #if this gets executed something went wrong.
    
    # this defines how an agent should change its belief about which state it is in given an observation after taking some action.
    def Transition(self, Action,Observation ):
        newBelief = []
        for state in self.States:
            newBelief.append(self.StateEstimator(state,Action,Observation,self.currentBelief))
        sumofbeliefs  = 0
        for belief in newBelief:
            sumofbeliefs += belief
        if sumofbeliefs != 1:
            print "uh oh invalid belief"
        else:
            print "VALID BELIEF"
        print newBelief
        self.currentBelief = newBelief
        return newBelief
    def reset(self):
        prior = float(1)/len(self.States)
        self.currentBelief = []
        for state in self.States:
            self.currentBelief.append(prior)
    
    #estimates the probability of being in some state given an action, observation, and what the previous probability of being in that state was.
    def StateEstimator(self,state,Action,Observation,previousBelief):
        numerator = self.Observation(Action,state,Observation)
        sumofT = 0.0
        for s in self.States.keys():
            sumofT += self.ETransition(s,Action,state) * previousBelief[s] # times the estimated probability of this state in the previous belief... also this will fail.
        numerator = numerator * sumofT
        if state == 2 and Action == 'right' and Observation == 'green':
            pass
        #if numerator == 0.0:
        #    numerator answer
        denominator = 0
        
        for s1 in self.States:
            sum1 = self.Observation(Action,s1,Observation)
            sumofT = 0.0
            for s in self.States.keys():
                sumofT += self.ETransition(s,Action,s1) * previousBelief[s] # times the estimated probability of this state in the previous belief... also this will fail.
            sum1 = sum1 * sumofT
            denominator = denominator + sum1
        answer = numerator/denominator
        print "The Probability of being in state {} after Observing {} after taking action {} when the previous prob was {} is {}".format(state,Observation, Action,previousBelief[state],answer)
        return answer
    #checks the model of the environment for a probability distribution of states it could enter.
    def ETransition(self,preState, Action, postState):
        pcloud = self.environment.Transition(preState, Action)
        for state in pcloud:
            if state == postState:
                return pcloud[state]
        return 0.0
    #checks the chance of observing observation given that it took an action and was in some state.
    def Observation(self, action,state,observation):
        if state == 2 and action == 'right' and observation == 'green':
            pass
        pcloud = self.environment.Transition(state,action)
        observationcloud = OrderedDict()
        
        #sum up the probabilities.
        for s in pcloud.keys():
            actualobservation = self.environment.sense(s)
            #if this is a never before seen observation add it to the observationcloud dictionary else add the probability to the existing one
            if actualobservation in observationcloud:
                observationcloud[actualobservation] += pcloud[s]
            else:
                observationcloud[actualobservation] = pcloud[s] #default value is 0 so just setting it to the value of pcloud is the same as 0 + pcloud[s]
        #then if observation is still not in observationcloud. then the probability is 0.0 else 
        if observation in observationcloud:
            return observationcloud[observation]
        else:
            return float(0)
        
        
        
        
    
    def generateMDPfromPOMDP(self, States):
        maximumUncertainty = float(1)/States
        #number of points is the number of states*(Resolution+1)
        PointVectors = []
        #Center of the two dimentional polygon this represents the point at which any state is equally likely.
        centroid = []
        #number of lines in the polygon.
        PrimaryPolygon = []
        for State in range(0,States):
             centroid.append(maximumUncertainty)
        for vector in range(0,States):#create a vector representation for each state.
            coordinate = []
            for State in range(0,States):
                if State == vector:
                    coordinate.append(1)
                else:
                    coordinate.append(0)
            PointVectors.append(coordinate)
    
        PrimaryPolygon = self.getPolygonFrom(PointVectors) #this is the space that contains the entire co-MDP
        polypoints = self.getPolypoints(PrimaryPolygon) #this splits each line in the polygon into a number of line segments eqaul to the resolution
        triangles =  self.getTriangles(polypoints,centroid) #this takes the line segments and creates a triangle by adding a centroid to each segment.
        
        #at this point it should be a co-mdp. This next line then turns this space of infinite states into a finite space.                              
        ApproximatePOMDP = self.getBaseStates(triangles) #this splits each trangle into a number of polygons eqaul to resolution. Each of these polygons represents a State the Agent can be in.
        return ApproximatePOMDP
    
    def getPolygonFrom(self, PointVectors): #list of lists containing floats
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
    #
    def getPolypoints(self, PrimaryPolygon): #list of vector lines, int
        polypoints = []
        for line in PrimaryPolygon:
            polypoints.append(line.vector1)
            for i in range(1,self.Resolution): 
                polypoints.append(line.getPoint(float(-i)/self.Resolution))            
            #polypoints.append(line.vector2)
            
        #polypoints.remove(polypoints[len(polypoints)-1])
        return polypoints
    
    def getTriangles(self,polypoints,centroid):
        triangles = []
        inx = 0
        while inx < len(polypoints)-1:
            triangle = Triangle(polypoints[inx],polypoints[inx+1],centroid)
            triangles.append(triangle)
            inx += 1
        triangle = Triangle(polypoints[len(polypoints)-1],polypoints[0],centroid)
        triangles.append(triangle);

        return triangles
    
    def getBaseStates(self, triangles):
        States = []
        
        for triangle in triangles: #format assumed is [x1,x2,centroid] for all triangles the Triangle class should help reduce the chance of any errors in implementation.

            line1 = vectorLine(triangle.coords[2],triangle.coords[0])
            line2 = vectorLine(triangle.coords[2],triangle.coords[1])
            #first one is always a triangle
            States.append( Polygon([triangle.coords[2],line1.getPoint(float(-1)/self.Resolution),line2.getPoint(float(-1)/self.Resolution) ]))
            #then all the filling which is always a quadrilateral
            for i in range(1,self.Resolution-1): #create all quadrilaterals between the first and last one.
                point1 = line1.getPoint(float(-(1+1)) / self.Resolution)
                point2 = line2.getPoint(float(-(i+1))/self.Resolution)
                point3 = line1.getPoint(float(-(i+2))/self.Resolution)
                point4 = line2.getPoint(float(-(i+2))/self.Resolution)
                shape = Polygon([point1,point2,point3,point4])
                States.append(shape)
                #print "added a meat quad."
            #the last quadrilateral
            point1 = line1.getPoint(float(-(self.Resolution-1))/self.Resolution)
            point2 = line2.getPoint(float(-(self.Resolution-1))/self.Resolution)
            point3 = triangle.coords[0]
            point4 = triangle.coords[1]
            States.append( Polygon([point1,point2,point3,point4]))
            
        return States
            

line1 = [0,1,0]
line2 = [1,0,0]
vectorline = vectorLine(line1,line2)
print vectorline.getPoint(-.3)