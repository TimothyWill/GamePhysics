# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:30:05 2018

@author: Student
"""

import pygame
from vec2d import Vec2d

class Cannon(pygame.sprite.Sprite):
    def __init__(self, pos, vel, mass, radius, color):
        super().__init__()
        self.image = pygame.image.load("cannonball.png")
        self.image = pygame.transform.scale(self.image, (15, 15))
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
        screen.blit(self.image,coords.pos_to_screen(self.pos).int())