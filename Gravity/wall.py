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
        self.normal = self.makeNormal(self.pos1, self.pos2)

    def draw(self, screen, coords):
        pos1 = coords.pos_to_screen(self.pos1)
        normal = coords.unitvec_to_other(self.normal)
        X = screen.get_width()-1
        Y = screen.get_height()-1
        perp = normal.perpendicular()
        if perp.x == 0:
            start = Vec2d(pos1.x, 0)
            end   = Vec2d(pos1.x, Y)
        elif perp.y == 0:
            start = Vec2d(0, pos1.y)
            end   = Vec2d(X, pos1.y)
        else:
            s = []
            s.append((0-pos1.x)/perp.x)                
            s.append((0-pos1.y)/perp.y)                
            s.append((X-pos1.x)/perp.x)                
            s.append((Y-pos1.y)/perp.y)
            s.sort()
            start = pos1 + perp*s[1]
            end   = pos1 + perp*s[2]
        pygame.draw.line(screen, self.color, start, end, 1)
   
    def makeNormal(self, pos1, pos2):
        return Vec2d(pos1.x-pos2.x, pos1.y-pos2.y).perpendicular().normalized()
 