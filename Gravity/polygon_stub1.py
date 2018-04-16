# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:26:03 2018

@author: sinkovitsd
"""

from math import sin, cos, degrees
from vec2d import Vec2d
import pygame

class Polygon:
    def __init__(self, pos, vel, density, points, color, angle=0, angvel=0):
        self.pos = pos
        self.vel = vel
        self.color = color
        self.angle = angle
        self.angvel = angvel
        self.force = Vec2d(0,0)
        self.torque = 0

        # Set origpoints
        self.origpoints = []
        for p in points:
            self.origpoints.append(p.copy())
        pp = self.origpoints # pp as an alternate label for this function

        # Tally area, moment, and center of mass
        self.area = 0
        self.moment = 0
        center = Vec2d(0,0)
        for i in range(len(pp)):
            #> area of triangle, and add to total area
            a = pp[i].cross(pp[i-1])/2
            self.area += a
            #> moment of triange about vertex
            #> add center of mass of triange to center of mass of shape
            center += a*(pp[i] + pp[i-1])/3
            pass
        center *= 1/self.area
        self.mass = density*self.area
        print("center =", center)
        print("area =", self.area)
        print("mass =", self.mass)

        # Shift self.origpoints to be centered on center of mass
        for p in self.origpoints:
            p -= center
        self.pos += center
        
        #> Shift moment to be about center of mass (parallel axis theorem)

        print("moment =", self.moment)
        #print(pp)

        # Recalculate moment around the center of mass as a check
        moment = 0
        for i in range(len(pp)):
            #> same as above loop to tally moment of each triangle about vertex
            pass
        print("moment =", moment)
        
        # Calculate normals to each points
        self.orignormals = []
        for i in range(len(pp)):
            #> calculate normal here and append to orignormals
            pass
        #print("orignormals =", self.orignormals)
        
        # Calculate rotated points and normals
        self.points = []
        for p in self.origpoints:
            self.points.append(None)
        self.normals = []
        for n in self.orignormals:
            self.normals.append(None)
        self.update_points_normals()
                
        self.mom = self.mass*self.vel
        self.angmom = self.moment*self.angvel
        #print("points =", self.points)
        #print("normals =", self.normals)
        
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
        if self.angvel*dt != 0:
            self.update_points_normals()
            
    def update_points_normals(self):
        c = cos(self.angle)
        s = sin(self.angle)
        #> use s and c to calculate points and normals rotated

    def update(self, dt):
        self.update_mom(dt)
        self.update_pos(dt)
                
    def impulse(self, imp, point=None):
        self.mom += imp
        self.update_vel()
        if point is not None:
            self.angmom += (point - self.pos).cross(imp)  
            self.update_angvel()
 
    def draw(self, screen, coords):
        # Draw polygon
        points = []
        for p in self.points:
            points.append(coords.pos_to_screen(self.pos + p))
        pygame.draw.polygon(screen, self.color, points)
        if True:
            for i in range(len(points)):
                length = 50
                n = coords.unitvec_to_other(self.normals[i])
                p = (points[i] + points[i-1])/2
                pygame.draw.line(screen, (0,0,0), p, p + length*n)
    
    def check_collision(self, other, result=[]):
        result.clear() # See polygon_collision_test.py in check_collision()
        overlap = 1e99
        if other.type == "polygon":            
            """ Self supplies the vertices.  Other provides the sides (walls).
                For each wall, find the point that penetrates the MOST, 
                and record the magnitude of penetration.  If for one wall, 
                no point penetrates, there is no overlap; return False.
                Otherwise, find which wall is LEAST penetrated, and pass back,
                via result.extend(), the overlap, point and normal involved; 
                return True. """
            for i in range(len(other.normals)):
                # Fill in
                pass
                for j in range(len(self.points)):
                    # Fill in
                    pass
            result.extend([self, other, overlap, normal, point])
            return True

    