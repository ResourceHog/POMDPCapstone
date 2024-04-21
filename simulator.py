# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 16:48:10 2017

@author: ECOWIZARD
"""

###########################################
# Suppress matplotlib user warnings
# Necessary for newer version of matplotlib
import warnings
warnings.filterwarnings("ignore", category = UserWarning, module = "matplotlib")
###########################################

import os
import time
import random
import importlib
import csv

class Simulator4x1(object):
    """Simulates agents in a dynamic smartcab environment.

    Uses PyGame to display GUI, if available.
    """

    colors = {
        'black'   : (  0,   0,   0),
        'white'   : (255, 255, 255),
        'red'     : (255,   0,   0),
        'green'   : (  0, 255,   0),
        'dgreen'  : (  0, 228,   0),
        'blue'    : (  0,   0, 255),
        'cyan'    : (  0, 200, 200),
        'magenta' : (200,   0, 200),
        'yellow'  : (255, 255,   0),
        'mustard' : (200, 200,   0),
        'orange'  : (255, 128,   0),
        'maroon'  : (200,   0,   0),
        'crimson' : (128,   0,   0),
        'gray'    : (155, 155, 155)
    }

    def __init__(self, env, size=None, update_delay=2.0, display=True, log_metrics=False, optimized=False,vanilla=False):
        self.env = env
        self.vanilla = vanilla
        self.blocksize = 100
        self.size = size if size is not None else (4 * self.blocksize,int(2.2*self.blocksize))
        self.width, self.height = self.size
        self.road_width = 44

        self.bg_color = self.colors['gray']
        self.line_color = self.colors['mustard']
        self.boundary = self.colors['black']
        self.stop_color = self.colors['crimson']

        self.quit = False
        self.start_time = None
        self.current_time = 0.0
        self.last_updated = 0.0
        self.update_delay = update_delay  # duration between each step (in seconds)

        self.display = display
        if self.display:
            try:
                self.pygame = importlib.import_module('pygame')
                self.pygame.init()
                self.screen = self.pygame.display.set_mode(self.size)
              
                self.frame_delay = max(1, int(self.update_delay * 1000))  # delay between GUI frames in ms (min: 1)
                #self.agent_sprite_size = (32, 32)
                self.primary_agent_sprite_size = (42, 42)
                self.agent_circle_radius = 20  # radius of circle, when using simple representation
                #if self.pygame.font != None:
                #   self.font = self.pygame.font.Font(None, 20)
                self.paused = False
            except ImportError as e:
                self.display = False
                print("Simulator.__init__(): Unable to import pygame; display disabled.\n{}: {}".format(e.__class__.__name__, e))
            except Exception as e:
                self.display = False
                print("Simulator.__init__(): Error initializing GUI objects; display disabled.\n{}: {}".format(e.__class__.__name__, e))

        # Setup metrics to report
        self.log_metrics = log_metrics
        self.optimized = optimized
        if self.log_metrics:
            a = self.env.primary_agent

            # Set log files
            if vanilla:
                
                if a.learning:
                    if self.optimized: # Whether the user is optimizing the parameters and decay functions
                        self.log_filename = os.path.join("logs", "qsim_improved-learning.csv")
                        self.table_filename = os.path.join("logs","qsim_improved-learning.txt")
                    else: 
                        self.log_filename = os.path.join("logs", "qsim_default-learning.csv")
                        self.table_filename = os.path.join("logs","qsim_default-learning.txt")

                    self.table_file = open(self.table_filename, 'w')
                else:
                    self.log_filename = os.path.join("logs", "qsim_no-learning.csv")
            else:
                if a.learning:
                    if self.optimized: # Whether the user is optimizing the parameters and decay functions
                        self.log_filename = os.path.join("logs", "sim_improved-learning.csv")
                        self.table_filename = os.path.join("logs","sim_improved-learning.txt")
                    else: 
                        self.log_filename = os.path.join("logs", "sim_default-learning.csv")
                        self.table_filename = os.path.join("logs","sim_default-learning.txt")

                    self.table_file = open(self.table_filename, 'w')
                else:
                    self.log_filename = os.path.join("logs", "sim_no-learning.csv")
                
            self.log_fields = ['trial', 'testing', 'parameters',  'net_reward', 'age', 'success']
            self.log_file = open(self.log_filename, 'w')
            self.log_writer = csv.DictWriter(self.log_file, fieldnames=self.log_fields)
            self.log_writer.writeheader()

    def run(self, tolerance=0.05, n_test=0):
        """ Run a simulation of the environment. 

        'tolerance' is the minimum epsilon necessary to begin testing (if enabled)
        'n_test' is the number of testing trials simulated

        Note that the minimum number of training trials is always 20. """

        self.quit = False

        # Get the primary agent
        a = self.env.primary_agent

        total_trials = 1
        testing = False
        trial = 1

        while True:

            # Flip testing switch
            if not testing:
                if total_trials > 20: # Must complete minimum 20 training trials
                    if a.learning:
                        print("epsilon = {}".format(a.epsilon))
                        print("tolerance = {}".format(tolerance))
                        if a.epsilon < tolerance: # assumes epsilon decays to 0
                            testing = True
                            trial = 1
                    else:
                        testing = True
                        trial = 1
                        
            # Break if we've reached the limit of testing trials
            else:
                if trial > n_test:
                    break



            # Pretty print to terminal
            print()
            print("/-------------------------")
            if testing:
                print("| Testing trial {}".format(trial))
            else:
                print("| Training trial {}".format(trial))

            print("\-------------------------")
            print() 

            self.env.reset(testing)
            self.current_time = 0.0
            self.last_updated = 0.0
            self.start_time = time.time()
            while True:
                try:
                    # Update current time
                    self.current_time = time.time() - self.start_time

                    # Handle GUI events
                    if self.display:
                        for event in self.pygame.event.get():
                            if event.type == self.pygame.QUIT:
                                self.quit = True
                            elif event.type == self.pygame.KEYDOWN:
                                if event.key == 27:  # Esc
                                    self.quit = True
                                elif event.unicode == u' ':
                                    self.paused = True

                        if self.paused:
                            self.pause()

                    # Update environment
                    if self.current_time - self.last_updated >= self.update_delay:
                        self.env.step()
                        self.last_updated = self.current_time
                    
                    # Render text
                    self.render_text(trial, testing)

                    # Render GUI and sleep
                    if self.display:
                        self.render(trial, testing)
                        self.pygame.time.wait(self.frame_delay)

                except KeyboardInterrupt:
                    self.quit = True
                finally:
                    if self.quit or self.env.done:
                        break

            if self.quit:
                break

            # Collect metrics from trial
            if self.log_metrics:
                self.log_writer.writerow({
                    'trial': trial,
                    'testing': self.env.trial_data['testing'],
                    'parameters': self.env.trial_data['parameters'],
                    'net_reward': self.env.trial_data['net_reward'],
                    'age' : self.env.trial_data['age'],
                    'success': self.env.trial_data['success']
                })

            # Trial finished
            if self.env.success == True:
                print("\nTrial Completed!")
                print("Agent reached the destination.")
            else:
                print("\nTrial Aborted!")
                print("Agent did not reach the destination.")

            # Increment
            total_trials = total_trials + 1
            trial = trial + 1

        # Clean up
        if self.log_metrics:

            if a.learning:
                f = self.table_file
                
                f.write("/-----------------------------------------\n")
                f.write("| State-action rewards from modified Q-Learning\n")
                f.write("\-----------------------------------------\n\n")

                for state in a.Q:
                    f.write("{}\n".format(state))
                    for action, reward in a.Q[state].items():
                        print("{} , {}".format(action,reward))
                        f.write(" -- {} : {:.2f}\n".format(action, reward))
                    f.write("\n")  
                self.table_file.close()

            self.log_file.close()

        print("\nSimulation ended. . . ")

        # Report final metrics
        
        
        
        
        if self.display:
            self.pygame.display.quit()  # shut down pygame

    def render_text(self, trial, testing=False):
        """ This is the non-GUI render display of the simulation. 
            Simulated trial data will be rendered in the terminal/command prompt. """

        status = self.env.step_data
        if status : # Continuing the trial

            # Previous State
            if status['state']:
                print("Agent previous state: {}".format(status['state']))
            else:
                print("!! Agent state not been updated!")

            
        # Starting new trial
        else:
            a = self.env.primary_agent
            print("Simulating trial. . . ")
            if a.learning:
                print("epsilon = {:.4f}; alpha = {:.4f}".format(a.epsilon, a.alpha))
            else:
                print("Agent not set to learn.")

    def renderMindState(self, xadjustment,yadjustment):
        if self.vanilla:
            return
        currentState = self.env.primary_agent.environmentmodel.getState()
        magnification = 50
        beliefstate = self.env.primary_agent.environmentmodel.currentBelief
        beliefstate = self.env.primary_agent.environmentmodel.translateNDpointto2D(beliefstate)
        beliefstate[0] = int((beliefstate[0]*magnification) + xadjustment)
        beliefstate[1] =int( (beliefstate[1]*magnification) + yadjustment)
        for state in self.env.primary_agent.environmentmodel.pomdpStates:
            coords = []
            for x,y in state.coords:
                coords.append([(x*magnification)+xadjustment,(y * magnification) + yadjustment])
            if  currentState == state:
                self.pygame.draw.polygon(self.screen,self.colors["red"],coords,0)
            else:
                self.pygame.draw.polygon(self.screen,self.colors["red"],coords,1)
            
        
        self.pygame.draw.circle(self.screen, self.colors["orange"],beliefstate,3,0)
                
    def render(self, trial, testing=False):
        """ This is the GUI render display of the simulation. 
            Supplementary trial data can be found from render_text. """
        
        # Reset the screen.
        self.screen.fill(self.bg_color)

        # Draw elements
        # * Static elements

        # Boundary
        screen_size = self.screen.get_size()
        self.pygame.draw.rect(self.screen,self.boundary,self.pygame.Rect(1,1,screen_size[0]-2,screen_size[1]-2))
        
        
        #
        for position, state in self.env.states.items():
            self.pygame.draw.rect(self.screen,self.colors['black'],self.pygame.Rect(position*self.blocksize,0,self.blocksize,self.blocksize))
            self.pygame.draw.rect(self.screen,self.colors['white'],self.pygame.Rect((position*self.blocksize)+2,2,self.blocksize - 4, self.blocksize -4))
            
            

            
        # * Dynamic elements
        #self.font = self.pygame.font.Font(None, 20)
        for agent, state in self.env.agent_states.items():
            # Compute precise agent location here (back from the intersection some)
            
            agent_pos = ((state['location'] * self.blocksize)+(self.blocksize/3), self.blocksize - (self.blocksize /2))
            agent_color = self.colors[agent.color]

            
            if state['location'] == 2:
                self.pygame.draw.rect(self.screen,self.colors['yellow'],self.pygame.Rect((2*self.blocksize)+2,2,self.blocksize - 4, self.blocksize -4))
                # Draw simple agent (circle with a short line segment poking out to indicate heading)
            self.pygame.draw.circle(self.screen, agent_color, agent_pos, self.blocksize/3)
            
        self.renderMindState(self.blocksize/2,1.4*self.blocksize)

        # Flip buffers
        self.pygame.display.flip()

    def pause(self):
        """ When the GUI is enabled, this function will pause the simulation. """
        
        abs_pause_time = time.time()
        self.font = self.pygame.font.Font(None, 30)
        pause_text = "Simulation Paused. Press any key to continue. . ."
        self.screen.blit(self.font.render(pause_text, True, self.colors['red'], self.bg_color), (400, self.height - 30))
        self.pygame.display.flip()
        print(pause_text)
        while self.paused:
            for event in self.pygame.event.get():
                if event.type == self.pygame.KEYDOWN:
                    self.paused = False
            self.pygame.time.wait(self.frame_delay)
        self.screen.blit(self.font.render(pause_text, True, self.bg_color, self.bg_color), (400, self.height - 30))
        self.start_time += (time.time() - abs_pause_time)
