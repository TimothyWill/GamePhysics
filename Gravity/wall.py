# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd
"""
import pygame
from vec2d import Vec2d

class Wall:
    def __init__(self, pos1, pos2, vel, color):
        self.pos1 = pos1
        self.pos2 = pos2
        self.vel = vel
        self.color = color
        self.force = Vec2d(0,0)  
        self.normal = self.makeNormal(self.pos1, self.pos2)

    def update(self, dt):
        self.mom += self.force*dt
        self.vel.copy_in(self.mom/self.mass)
        self.pos += self.vel*dt
                
    def draw(self, screen, coords):
        screenPos1 = coords.pos_to_screen(self.pos1)
        screenPos2 = coords.pos_to_screen(self.pos2)
        pygame.draw.polygon(screen, self.color, [[screenPos1.x, screenPos1.y], [screenPos2.x, screenPos2.y]], 5)
        
   
    def makeNormal(self, pos1, pos2):
        return Vec2d(pos1.x-pos2.x, pos1.y-pos2.y).perpendicular().normalized()
 