# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 03:16:46 2017

@author: ECOWIZARD
"""


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
