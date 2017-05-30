# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 17:07:53 2017

@author: ECOWIZARD
"""

#pygame stuff
import random
import pygame
from pygame.locals import *

class Square():
    def __init__(self,x,y,width,height,color):
        self.rectangle = Rect(x,y,width,height)
        self.color = color
        
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rectangle)


class pygamewindow():
    def __init__(self,width,height):
        self.square = Square(20,20,50,50,(250,40,40))
        self.openwindow(width,height)
        
    def drawsquare(self):
        self.square.draw(self.screen)
    
    def openwindow(self,width,height):
        self.screen = pygame.display.set_mode((height,width))
        pygame.display.flip()
    
        running = True
        while running:
            self.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            x = random.randint(-1,1)
            y = random.randint(-1,1)
            self.movesquare(x,y)
        pygame.quit()
        
    def render(self):
        self.screen.fill((0,0,0))
        self.drawsquare()
        pygame.display.flip()

    def movesquare(self,x,y):
        screensize = self.screen.get_size()
        
        self.square.rectangle.x += x
        self.square.rectangle.y += y

        if self.square.rectangle.x < 0 or self.square.rectangle.x > screensize[0]:
            self.square.rectangle.x -= x
            
        if self.square.rectangle.y < 0 or self.square.rectangle.y > screensize[1]:
            self.square.rectangle.y -= y
            
                

window = pygamewindow(300,200)