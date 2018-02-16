# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd
"""
import pygame
from vec2d import Vec2d

class Circle:
    def __init__(self, pos, vel, mass, radius, color):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.radius = radius
        self.color = color
        self.mom = self.vel*self.mass
        self.force = Vec2d(0,0)
    
    def update_mom(self, dt):
        self.mom += self.force*dt
    def update_vel(self):
        self.vel.copy_in(self.mom/self.mass)
    def update_pos(self, dt):
        self.pos += self.vel*dt

    def update(self, dt):
        self.mom += self.force*dt
        self.vel.copy_in(self.mom/self.mass)
        self.pos += self.vel*dt
                
    def draw(self, screen, coords):
        pygame.draw.circle(screen, self.color, 
                           coords.pos_to_screen(self.pos).int(), 
                           int(coords.scalar_to_screen(self.radius)), 0)
 