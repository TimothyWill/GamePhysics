# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd
"""
import pygame
from vec2d import Vec2d
from coords import Coords
from circle import Circle
from random import uniform, randint, random

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
GRAY     = ( 127, 127, 127)

def random_color():
    return (randint(0,255), randint(0,255), randint(0,255))

def random_bright_color():
    i = randint(0,2)
    d = randint(1,2)
    c = int(256*random()**0.5)
    color = [0,0,0]
    color[i] = 255
    color[(i+d)%3] = c
    return color

def gravity_force(obj1, obj2):
    """ compute the force on each object
        add to each, equal and opposite """
    r = obj1.pos - obj2.pos # distance between two objects
    m1 = obj1.mass # mass of 1st object
    m2 = obj2.mass # mass of 2nd object
    G = 1 #6.67384*(10**(-11)) # gravitational constant
    if r.mag() > (obj1.radius + obj2.radius):
        force = -((G*m1*m2)/r.mag2())*r.hat() # this is the formula for gravity
    else:
        force = 1*(r.mag()-obj1.radius)*r.hat() # this is the formula for repulsion
    
    obj1.force += force
    obj2.force -= force

def main():
    pygame.init()
 
    width = 800
    height = 600
    screen = pygame.display.set_mode([width,height])
    screen_center = Vec2d(width/2, height/2)
    coords = Coords(screen_center.copy(), 1, True)
    zoom = 80
    coords.zoom_at_coords(Vec2d(0,0), zoom) 
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Create initial objects to demonstrate
    objects = []
    n = 20
    mass = 1
    radius = 0.2
    for i in range(n):
        radius = uniform(0.3, 0.8)
        mass = radius*radius*20
        objects.append(Circle(Vec2d(width/zoom*uniform(-0.5,0.5), 
                                    height/zoom*uniform(-0.5,0.5)),
                              2*Vec2d(uniform(-1,1), uniform(-1,1)),
                              mass, radius, random_bright_color()))

    # -------- Main Program Loop -----------\
    frame_rate = 60
    playback_speed = 1 # 1 is real time, 10 is 10x real speed, etc.
    dt = playback_speed/frame_rate
    print("timestep =", dt)
    done = False
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # If user clicked close
                done = True
               
        # Physics
        # Calculate the force on each object
        for obj in objects:
            obj.force.zero()
        for i1, obj1 in enumerate(objects):
            for i2, obj2 in enumerate(objects):
                if i1 < i2:
                    gravity_force(obj1, obj2)
        
        # Move each object according to physics
        for obj in objects:
            obj.update(dt)
        
        # Drawing
        screen.fill(WHITE) # wipe the screen
        for obj in objects:
            obj.draw(screen, coords) # draw object to screen

        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second
        clock.tick(frame_rate)
        
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise
