# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 14:39:31 2018

@author: Student
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd
"""
import pygame
import math
from vec2d import Vec2d
from circle import Circle

class RotatingCircle(Circle):
    def __init__(self, pos, vel, mass, radius, color, linecolor, angle=0, angvel=0):
        super().__init__(pos, vel, mass, radius, color)
        self.angle = angle
        self.angvel = angvel
        self.moment = 0.5*self.mass*self.radius*self.radius
        self.angmom = self.moment*self.angvel
        self.torque = 0
        self.linecolor = linecolor
    
    def update_mom(self, dt):
        self.mom += self.force*dt
        self.angmom += self.torque*dt
        self.update_vel()
        self.update_angvel()
        
    def set_vel(self, vel):
        self.vel.copy_in(vel)
        self.mom.copy_in(self.vel*self.mass)

    def update_vel(self):
        self.vel.copy_in(self.mom/self.mass)
    
    def update_angvel(self):
        self.angvel = self.angmom/self.moment

    def update_pos(self, dt):
        self.pos += self.vel*dt
        self.angle += self.angvel*dt

    def update(self, dt):
        self.update_mom(dt)
        self.update_pos(dt)
        
    def impulse(self, imp, point=None):
        self.mom +=imp
        self.update_vel()
        if point is not None:
            self.angmom += (point - self.pos).cross(imp)
            self.update_angvel()
                
    def draw(self, screen, coords):
        #print("radius", self.radius, coords.scalar_to_screen(self.radius))
        super().draw(screen, coords)
        vec = self.radius*Vec2d(math.cos(self.angle), math.sin(self.angle))
        pygame.draw.line(screen, self.linecolor, 
                           coords.pos_to_screen(self.pos).int(), 
                           coords.pos_to_screen(self.pos + vec).int())
 
