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
    
    objects = []
    mass = 1
    radius = 1
    mass = radius*radius*20
    objects.append(Circle(Vec2d(-1, 0), Vec2d(0,0), mass, radius, random_bright_color()))
    objects.append(Circle(Vec2d(4, -2), Vec2d(-5,2), mass, radius, random_bright_color()))


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
    
            
        # Move each object according to physics
        for obj in objects:
            obj.update(dt)
        m1 = objects[0].mass
        m2 = objects[1].mass
        r = objects[0].pos - objects[1].pos 
        u = 1/((1/m1) + (1/m2))
        v1 = objects[0].vel
        v2 = objects[1].vel
        
        if r.mag() < (objects[0].radius + objects[1].radius):
            J = 1.5*u*(v2 - v1)
            objects[0].mom += J
            objects[1].mom -= J
        

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

