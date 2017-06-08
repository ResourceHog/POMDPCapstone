import time
import random
import math
from collections import OrderedDict
from simulator import Simulator

class uniqueState(object):
    def __init__(self,statetype):
        self.statetype = statetype


class Environment(object):
    """Environment within which all agents operate."""

    valid_actions = ['left', 'right']
    
    valid_headings = [(1, 0), (0, -1), (-1, 0), (0, 1)]  # E, N, W, S
    hard_time_limit = -100  # Set a hard time limit even if deadline is not enforced.

    def __init__(self):
        self.states = OrderedDict()
        self.valid_inputs = {'state': self.states.keys()}
        self.agent_states = OrderedDict()
        self.states[0] = uniqueState('s1')
        self.states[1] = uniqueState('s2')
        self.states[2] = uniqueState('green')
        self.states[3] = uniqueState('s3')
        self.done = False
        self.primary_agent = None
        self.step_data = {}
        self.success = False
        

    def create_agent(self, agent_class, *args, **kwargs):
        """ When called, create_agent creates an agent in the environment. """

        agent = agent_class(self, *args, **kwargs)
        self.agent_states[agent] = {'location': random.choice(self.states.keys())}
        print "asigned agent to position {}".format(self.agent_states[agent]['location'])
        return agent

    def set_primary_agent(self, agent):
        """ When called, set_primary_agent sets 'agent' as the primary agent.
            The primary agent is the smartcab that is followed in the environment. """
        self.primary_agent = agent
        agent.primary_agent = True

    def reset(self, testing=False):
        start = random.choice(self.states.keys())
        self.success = False
        self.done = False
        for agent in self.agent_states.iterkeys():
            if agent is self.primary_agent:
                self.agent_states[agent] = {'location': start}
                agent.reset()
        
        

    def step(self):
        prevlocation = self.agent_states[self.primary_agent]['location']
        if self.primary_agent is not None:
            self.primary_agent.update()
            
            
        self.step_data = {'state': prevlocation,}
        

    def sense(self, agent):
        state = self.agent_states[agent]
        return state['location']

    def get_deadline(self, agent):
        """ Returns the deadline remaining for an agent. """

        return None
    def act(self, agent, action):
        assert agent in self.agent_states, "unknown agent!"
        assert action in self.valid_actions, "invalid action!"
        
        reward = 0
        
        print action
        if action == self.valid_actions[0]: #left
            if self.agent_states[agent]['location'] == 1:
                self.agent_states[agent]['location'] = 0
            elif self.agent_states[agent]['location'] == 2:
                print "SUCCESS!"
                self.success = True
                self.done = True
            elif self.agent_states[agent]['location'] == 3:
                self.agent_states[agent]['location'] = 2
                reward = 1
        elif action == self.valid_actions[1]: #right
            if self.agent_states[agent]['location'] == 1:
                self.agent_states[agent]['location'] = 2
                reward = 1
            elif self.agent_states[agent]['location'] == 2:
                print "SUCCESS!"
                self.success = True
                self.done = True
            elif self.agent_states[agent]['location'] == 0:
                self.agent_states[agent]['location'] = 1
        
        
        return reward

    def compute_dist(self, a, b):
        """ Compute the Manhattan (L1) distance of a spherical world. """

        dx1 = abs(b[0] - a[0])
        dx2 = abs(self.grid_size[0] - dx1)
        dx = dx1 if dx1 < dx2 else dx2

        dy1 = abs(b[1] - a[1])
        dy2 = abs(self.
            grid_size[1] - dy1)
        dy = dy1 if dy1 < dy2 else dy2

        return dx + dy


class Agent(object):
    """Base class for all agents."""

    def __init__(self, env):
        self.env = env
        self.state = None
        self.next_waypoint = None
        self.color = 'white'
        self.primary_agent = False

    def reset(self, destination=None, testing=False):
        pass

    def update(self):
        pass

    def get_state(self):
        return self.state

    def get_next_waypoint(self):
        return self.next_waypoint  
