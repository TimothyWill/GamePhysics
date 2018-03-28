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
                
    def draw(self, screen, coords, width, height):
        
        screenPos1 = coords.pos_to_screen(self.pos1)
        screenPos2 = coords.pos_to_screen(self.pos2)
        
        slope = (screenPos1.y - screenPos2.y) / (screenPos1.x - screenPos2.x)
        
        extendedPos1 = Vec2d(screenPos1.x, screenPos1.y)
        extendedPos2 = screenPos2
        
        if self.pos1.x < self.pos2.x:
            extendedPos1.x = 0
            extendedPos1.y = (0 - screenPos1.x) * slope + screenPos1.y
            extendedPos2.x = width
            extendedPos2.y = (width - screenPos2.x) * slope + screenPos2.y
        else:
            extendedPos2.x = 0
            extendedPos2.y = (0 - screenPos2.x) * slope + screenPos2.y
            extendedPos1.x = width
            extendedPos1.y = (width - screenPos1.x) * slope + screenPos1.y
        
        
        if self.normal.x > 0:
            if self.normal.y > 0:
                lastPoint = Vec2d(width, 0)
            else:
                lastPoint = Vec2d(width, height)
        else:
            if self.normal.y > 0:
                lastPoint = Vec2d(0, 0)
            else:
                lastPoint = Vec2d(0, height)
                
        
        print(lastPoint)
        
        pygame.draw.polygon(screen, self.color, [[extendedPos1.x, extendedPos1.y], [screenPos2.x, screenPos2.y], [lastPoint.x, lastPoint.y]], 0)
    
    
    def makeNormal(self, pos1, pos2):
        return Vec2d(pos1.x-pos2.x, pos1.y-pos2.y).perpendicular().normalized()
 