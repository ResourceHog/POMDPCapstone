# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 14:21:46 2017

@author: ECOWIZARD
"""
from collections import OrderedDict
import random as Random
import copy


class uniqueState(object):
    def __init__(self,statetype :str):
        self.statetype = statetype



class Environment4x1(object):
    def __init__(self):
        self.valid_actions = ['left', 'right']
        self.valid_observables = ['blue', 'green']
        self.states = dict()
        self.valid_inputs = {'state': list(self.states.keys())}
        self.agent_states = dict()
        self.states[0] = uniqueState(self.valid_observables[0]) #blue state
        self.states[1] = uniqueState(self.valid_observables[0]) #blue state
        self.states[2] = uniqueState(self.valid_observables[1]) #green state
        self.states[3] = uniqueState(self.valid_observables[0]) #blue state
        self.done = False
        self.primary_agent = None
        self.step_data = {}
        self.success = 0
        self.TIMELIMIT = 10
        self.timelapsed = 0

        
        self.trial_data = {
            'testing': False, # if the trial is for testing a learned policy
            'net_reward': 0.0,  # total reward earned in current trial
            'success': 0,  # whether the agent reached the destination in time
            'age' : 0
        }

    @classmethod
    def copy(cls,env):
        newenv = cls()
        newenv.valid_actions = copy.copy(env.valid_actions)
        newenv.valid_observables = copy.deepcopy(env.valid_observables)
        newenv.states = copy.deepcopy(env.states)
        newenv.valid_inputs = copy.copy(env.valid_inputs)
        newenv.agent_states = copy.copy(env.agent_states)
        newenv.done = copy.deepcopy(env.done)
        newenv.primary_agent = copy.deepcopy(env.primary_agent)
        newenv.step_data = copy.deepcopy(env.step_data)
        newenv.success = copy.deepcopy(env.success)
        newenv.TIMELIMIT = copy.deepcopy(env.TIMELIMIT)
        newenv.timelapsed = copy.deepcopy(env.timelapsed)
        newenv.trial_data = copy.deepcopy(env.trial_data)
        return newenv
        
        
    def getStates(self):
        return self.states
    
    def sense(self,state=None):
        if state == None:
            return self.states[self.agent_states[self.primary_agent]["location"]].statetype #returns the color of the tile (in this case either blue or green depending on what state the agent is in..)
        else:
            #print "state is {}".format(state)
            if state == -1:
                pass
           # print "the observation was {}".format(self.states[state].statetype)
            return self.states[state].statetype
    

    def step(self):
        self.primary_agent.update() #this is the correct place to put this. It feels weird that the existence of the agents update function causes time to progress.
                                    #I think this weirdness comes from the fact that it is not a "physical" agent. (It's not a computer emedded inside the environment that runs the code.)
                                    #what I mean is that the rules of the environment are not the same rules that govern the execution of its code.
        print("agent is in state {}".format(self.agent_states[self.primary_agent]['location']))
        self.trial_data['age'] += 1
        self.timelapsed += 1
        if self.agent_states[self.primary_agent]['location'] == 2:
            self.success = 1
            self.trial_data['success'] = self.success
            self.done = True
        else:
            if self.timelapsed >= self.TIMELIMIT:
                self.done = True
            
        
        
    def Transition(self,preState, action):
        answer = OrderedDict()
        location = preState
        #print "in environment transition states are {}".format(self.states.keys())
        for state in list(self.states.keys()):
            if state == -1:
         #       print "what have we here {}".format(self.states.keys())
                pass
            answer[state] = 0
        if action in self.valid_actions:            
            if action == self.valid_actions[0]:
                action = -1
            if action == self.valid_actions[1]:
                action = 1
        location += action
        if location < 0:
            location = 0
        if location > 3:
            location = 3
        answer[location] = float(1) #this environment's transition function in particular is deterministic. The starting point is the only stochastic variable.
        
       # print "after transition pcloud is {}".format(answer.keys())
        return answer
    
    def administerReward(self):
        reward = 0.0
        if self.agent_states[self.primary_agent]['location'] == 2:
            reward =  1.0
        else:
            reward =  -0.05
        self.trial_data['net_reward'] += reward
        return reward
    
    def act(self,action):
        pcloud = self.Transition(self.agent_states[self.primary_agent]['location'],action)    #gets all the states and their probability of becoming the next state where the probability is greater than 0.
        self.collapse(pcloud)               #chooses one of the states at random with a bias dependent on the probability of it occuring. (states with higher prob will be more likely)
        return self.administerReward()             #administers reward based on new state.
    
    def collapse(self,pcloud): #needs to be implemented.
        randomnum  = Random.uniform(0,1)
        threshold = 0
        
        for indx , probability in pcloud.items():
            threshold += probability
            if randomnum <= threshold:
                self.agent_states[self.primary_agent]['location'] = indx
                return
        raise ValueError("For some reason the probabilities can't be compared with the <= operator.")
        #it should never get here.
        return
            
        
    
    def create_agent(self,agent_class,*args, **kwargs):
        agent = agent_class(self, Environment4x1, *args, **kwargs)
        keys = list(self.states.keys())
        print("when creating an agent the states are {}".format(keys))
        self.agent_states[agent] = {'location': Random.choice(keys)}
        print("print assigned agent to location: " + str(self.agent_states[agent]['location']))
        return agent
    
    def set_primary_agent(self,agent):
        
        self.primary_agent = agent
        self.agent_states[self.primary_agent]["location"] = self.randomlocation()
        
        
    def randomlocation(self):
        location = Random.choice([0,1,3])
        return location
    
    def reset(self,testing):
        self.primary_agent.reset(testing)
        location = self.randomlocation()
        print("New Starting location is {}".format(location))
        self.agent_states[self.primary_agent]['location'] = location
        self.reward = 0
        self.success = 0
        self.done = False
        self.timelapsed = 0
        
        
        # Reset metrics for this trial (step data will be set during the step)
        self.trial_data['testing'] = testing
        self.trial_data['net_reward'] = 0.0
        self.trial_data['parameters'] = {'e': self.primary_agent.epsilon, 'a': self.primary_agent.alpha}
        self.trial_data['success'] = 0
        self.trial_data['age'] = 0

    