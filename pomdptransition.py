# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 16:12:22 2017

@author: ECOWIZARD
"""

def transition(States, Action,Observation, previousBelief): # this is the transition function for the co-mdp derived from the environment.
    newBelief = []
    for state in States:
        newBelief.append(StateEstimator(States,state,Action,Observation,previousBelief))
    return newBelief

def StateEstimator(States,state,Action,Observation,previousBelief):
    answer = Observation(Action,state,Observation)
    sumofT = 0.0
    for s in States:
        #TODO: make this compile
        sumofT += Transition(s,Action,state) * previousBelief[s] # times the estimated probability of this state in the previous belief... also this will fail.
    answer = answer * sumofT
    
    denominator = 0
    sum1 = 0
    sum2 = 0
    for s in States:
        sum1 +=Observation(Action,s,Observation)
        sum2 +=Transition(s,Action,state)*previousBelief[s]
    denominator = sum1*sum2
    answer = answer/denominator
    return answer
    
def Observation(action,state,observation): #what's the probability of observerving "observation" after taking action "action" while in state "state"
    #run the transition function
    #add up the states with the same observation.
    #return the desired data
    #if it doesn't exist in the data assume 0% chance
    pass


def Transition(preState,Action,postState): #this is the transition function for the environment
    #create an environment with initial state 'preState'
    #run the environment transition function with the Action as the input.
    #return the desired data
    #if it doesn't exist in the data assume 0%
    pass