# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 14:21:46 2017

@author: ECOWIZARD
"""
from collections import OrderedDict
import random as Random


class uniqueState(object):
    def __init__(self,statetype):
        self.statetype = statetype
        self.nodes = OrderedDict()
    def attachnode(self, action,state,probability):
        if action not in list(self.nodes.keys()):
            self.nodes[action] = OrderedDict()
        if state not in list(self.nodes[action].keys()):
            self.nodes[action][state] = OrderedDict()          
        self.nodes[action][state] = probability



class EnvironmentTiger(object):
    def __init__(self):
        self.valid_actions = ['left', 'right','up','down','listen']
        self.valid_observables = ['left', 'right','silence','tiger']
        self.states = OrderedDict()
        self.valid_inputs = {'state': list(self.states.keys())}
        self.agent_states = OrderedDict()
        
        
        # set up all the states and their relations with each other.
        
        #for the case where the tiger is on the right....
        
        #valid_observables determines what the agent will sense when it is in the state.
        self.states[0] = uniqueState(self.valid_observables[2]) #(the listening post)
        self.states[1] = uniqueState(self.valid_observables[0]) #it senses the tiger on the left
        self.states[2] = uniqueState(self.valid_observables[1]) # on th right right
        self.states[3] = uniqueState(self.valid_observables[2]) #this hallway looks the same as any other part of it.
       
        self.states[4] = uniqueState(self.valid_observables[2]) #freedom
        self.states[5] = uniqueState(self.valid_observables[3]) #tiger
        
        self.states[0].attachnode(self.valid_actions[0],0,1) #left
        self.states[0].attachnode(self.valid_actions[1],0,1)
        self.states[0].attachnode(self.valid_actions[2],3,1)
        self.states[0].attachnode(self.valid_actions[3],0,1)
        self.states[0].attachnode(self.valid_actions[4],1,.2)
        self.states[0].attachnode(self.valid_actions[4],2,.8)
        
        self.states[1].attachnode(self.valid_actions[0],1,1)
        self.states[1].attachnode(self.valid_actions[1],1,1)
        self.states[1].attachnode(self.valid_actions[2],3,1)
        self.states[1].attachnode(self.valid_actions[3],1,1)
        self.states[1].attachnode(self.valid_actions[4],1,.2)
        self.states[1].attachnode(self.valid_actions[4],2,.8)
        
        self.states[2].attachnode(self.valid_actions[0],2,1)
        self.states[2].attachnode(self.valid_actions[1],2,1)
        self.states[2].attachnode(self.valid_actions[2],3,1)
        self.states[2].attachnode(self.valid_actions[3],2,1)
        self.states[2].attachnode(self.valid_actions[4],1,.2)
        self.states[2].attachnode(self.valid_actions[4],2,.8)
        
        self.states[3].attachnode(self.valid_actions[0],5,1)
        self.states[3].attachnode(self.valid_actions[1],4,1)
        self.states[3].attachnode(self.valid_actions[2],3,1)
        self.states[3].attachnode(self.valid_actions[3],0,1)
        self.states[3].attachnode(self.valid_actions[4],3,1)

        self.states[4].attachnode(self.valid_actions[0],4,1)
        self.states[4].attachnode(self.valid_actions[1],4,1)
        self.states[4].attachnode(self.valid_actions[2],4,1)
        self.states[4].attachnode(self.valid_actions[3],4,1)
        self.states[4].attachnode(self.valid_actions[4],4,1)

        self.states[5].attachnode(self.valid_actions[0],5,1)
        self.states[5].attachnode(self.valid_actions[1],5,1)
        self.states[5].attachnode(self.valid_actions[2],5,1)
        self.states[5].attachnode(self.valid_actions[3],5,1)
        self.states[5].attachnode(self.valid_actions[4],5,1)

        #--------------End Case--------------------------#
        # for the case where the tiger is on the left
        
        self.states[6] = uniqueState(self.valid_observables[2]) #The tiger is actually on the right (the listening post)
        self.states[7] = uniqueState(self.valid_observables[0]) #The Tiger is heard on the left
        self.states[8] = uniqueState(self.valid_observables[1]) #the tiger is heard on the right
        self.states[9] = uniqueState(self.valid_observables[2]) #the agent is down the hallway and can't here the tiger.

        self.states[6].attachnode(self.valid_actions[0],6,1) #nothing happens when you move left
        self.states[6].attachnode(self.valid_actions[1],6,1) #nothing happens when you move right
        self.states[6].attachnode(self.valid_actions[2],9,1) #you move down the hallway if you move up
        self.states[6].attachnode(self.valid_actions[3],6,1) #nothing happens when you move down.
        self.states[6].attachnode(self.valid_actions[4],8,.2) #20% chance of hearing the tiger on the right after listening
        self.states[6].attachnode(self.valid_actions[4],7,.8) #80% chance of hearing the tiger on the left after listening
        
        self.states[7].attachnode(self.valid_actions[0],6,1) #you hear nothing if you move left
        self.states[7].attachnode(self.valid_actions[1],6,1) #you hear nothing if you move right
        self.states[7].attachnode(self.valid_actions[2],9,1) #you move to the hallway if you move up.
        self.states[7].attachnode(self.valid_actions[3],6,1) #you move to the listening post if you move down
        self.states[7].attachnode(self.valid_actions[4],8,.2) #20% chance of hearing the tiger on the right after listening
        self.states[7].attachnode(self.valid_actions[4],7,.8) #80% chance of hearing the tiger on the left after listening
        
        self.states[8].attachnode(self.valid_actions[0],6,1) 
        self.states[8].attachnode(self.valid_actions[1],6,1)
        self.states[8].attachnode(self.valid_actions[2],9,1)
        self.states[8].attachnode(self.valid_actions[3],6,1)
        self.states[8].attachnode(self.valid_actions[4],8,.2)
        self.states[8].attachnode(self.valid_actions[4],7,.8)
        
        self.states[9].attachnode(self.valid_actions[0],4,1)
        self.states[9].attachnode(self.valid_actions[1],5,1)
        self.states[9].attachnode(self.valid_actions[2],9,1)
        self.states[9].attachnode(self.valid_actions[3],6,1)
        self.states[9].attachnode(self.valid_actions[4],9,1)

        #---------------End Case-----------------------------#
        
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
        
        if self.agent_states[self.primary_agent]['location'] == 4 :
            self.success = 1
            self.trial_data['success'] = self.success
            self.done = True
        else:
            if  self.agent_states[self.primary_agent]['location'] == 5 or self.timelapsed >= self.TIMELIMIT:
                self.done = True
            
        
        
    def Transition(self,preState, action):
        answer = self.states[preState].nodes[action]
        return answer
    
    def administerReward(self):
        reward = 0
        if self.agent_states[self.primary_agent]['location'] == 4 :
            reward = 1
        else:
            reward = -0.05
        self.trial_data['net_reward'] += reward
        return reward
        
    
    def act(self,action):
        
        pcloud = self.Transition(self.agent_states[self.primary_agent]['location'],action)    #gets all the states and their probability of becoming the next state where the probability is greater than 0.
        self.collapse(pcloud)               #chooses one of the states at random with a bias dependent on the probability of it occuring. (states with higher prob will be more likely)
        return self.administerReward()             #administers reward based on new state.
    
    def collapse(self,pcloud):
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
            
        
    
    def create_agent(self,agentclass,*args, **kwargs):
        agent = agentclass(self,*args, **kwargs)
        print("when creating an agent the states are {}".format(list(self.states.keys())))
        self.agent_states[agent] = {'location': Random.choice(list(self.states.keys()))}
        print("print assigned agent to location: " + str(self.agent_states[agent]['location']))
        return agent
    
    def set_primary_agent(self,agent):
        
        self.primary_agent = agent
        self.agent_states[self.primary_agent]["location"] = self.randomlocation()
        
        
    def randomlocation(self):
        possibleStates = [0,1,2,3,6,7,8,9]
        location = Random.choice(possibleStates)
        if location in [0,1,2,3]:
            self.tigerlocation = 'left'
        else:
            self.tigerlocation = 'right'
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

    