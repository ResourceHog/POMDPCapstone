# -*- coding: utf-8 -*-
"""
Created on Sat Jul 08 10:39:16 2017

@author: ECOWIZARDc

"""
from tigersimulater import TigerSimulator
from simulator import Simulator4x1
from EnvironmentTiger import EnvironmentTiger
from Environment4x1 import Environment4x1
from pomdpagent import LearningAgent
from agent import LearningAgent as Qlearner

TIGERSIM = False

def run():
    """ Driving function for running the simulation.
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    env = None
    if TIGERSIM:
        env = EnvironmentTiger()
    else:
        env = Environment4x1()
    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha - continuous value for the learning rate, default is 0.5
    isLearning = True
    wepsilon = 0.9999
    walpha = 0.3
    wresolution = 4
    agent = env.create_agent(LearningAgent,learning = isLearning, epsilon = wepsilon, alpha=walpha,resolution=wresolution)
    #agent4x1 = env.create_agent(LearningAgent, learning = isLearning, epsilon = wepsilon,alpha = walpha,resolution=wresolution)
    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent)
    #env.set_primary_agent(agent4x1)
    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    isLogging = True
    isOptimised = False
    delay = 0.01
    sim = None
    if TIGERSIM:
        sim = TigerSimulator(env,update_delay = delay,log_metrics=isLogging    ,optimized=isOptimised)
    else:
        sim = Simulator4x1(env,update_delay = delay,log_metrics=isLogging    ,optimized=isOptimised)

    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05
    #   n_test     - discrete number of testing trials to perform, default is 0
    #sim.run(n_test = 50)
    print("starting second sim")
    #sim4x1 = Simulator4x1(env,update_delay = delay,log_metrics=isLogging,optimized=isOptimised)
    sim.run(n_test = 2)


    print("starting control.")
    #agent = env.create_agent(Qlearner,learning = isLearning, epsilon = wepsilon, alpha=walpha)
    agent = env.create_agent(Qlearner,learning = isLearning, epsilon = wepsilon, alpha = walpha)
    #sim = env.set_primary_agent(agent)
    env.set_primary_agent(agent)



    if TIGERSIM:
        sim = TigerSimulator(env,update_delay = delay,log_metrics=isLogging    ,optimized=isOptimised,vanilla = True)
    else:
        sim = Simulator4x1(env,update_delay = delay,log_metrics=isLogging    ,optimized=isOptimised,vanilla = True)
    sim.run(n_test = 2)
    #sim = TigerSimulator(env,update_delay = delay ,log_metrics = isLogging,optimized=isOptimised,vanilla = True)
    #sim.run(n_test = 50)



    print("starting second sim")
    # sim = Simulator4x1(env,update_delay = delay,log_metrics=isLogging    ,optimized=isOptimised,vanilla = True)
    # sim.run(n_test = 2)

if __name__ == '__main__':
    run()
