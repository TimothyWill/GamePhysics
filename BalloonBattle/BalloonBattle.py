# -*- coding: utf-8 -*-

import pygame
from vec2d import Vec2d
from coords import Coords
from circle import Circle
from Cannon import Cannon
from Balloon import Balloon

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
GRAY     = ( 127, 127, 127)

def main():
    pygame.init()
    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, (800, 600))
 
    width = 800
    height = 600
    screen = pygame.display.set_mode([width,height])
    draw_screen = screen.copy()
    draw_screen.fill(WHITE)
    draw_screen.set_alpha(64) # 64/255 is about 25% opaque
    screen_center = Vec2d(width/2, height/2)
    coords = Coords(screen_center.copy(), 1, True)
    # ^ Center of window is (0,0), scale is 1:1, and +y is up
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Initialize the balloons
    LeftBalloon  = Balloon(Vec2d(0, 0), 30, Vec2d(-1.5, 0), 0.05, BLUE, 9.8, pygame.K_w)
    RightBalloon = Balloon(Vec2d(0, 0), 30, Vec2d(1.5, 0), 0.05, BLUE, 9.8, pygame.K_i)
    RightBalloon.image = pygame.transform.flip(RightBalloon.image, True, False)

    objects = []
    #objects.append(Circle(Vec2d(-1.5,0), Vec2d(1, 1), 1, 0.05, BLUE))
    coords.zoom_at_coords(Vec2d(0,0), 200) 
    # ^ Zoom in 200x, so now the scale is 100 pixels per unit
    # -------- Main Program Loop -----------\
    frame_rate = 60
    playback_speed = 1 # 1 is real time, 10 is 10x real speed, etc.
    dt = playback_speed/frame_rate
    
    def cannon(position, direction):
        objects.append(Cannon(Vec2d(position), Vec2d(direction), 1, 0.05, RED))
        for obj in objects:
            
            #Air Resistance
            r = 0.1
            
            #Shoot Cannon
            obj.force = (r * obj.vel.get_length() ** 2) * obj.vel.normalized();   
            
            # Apply Gravity
            obj.force += Vec2d(0, -9.8);
        
    
    done = False
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # If user clicked close
                done = True
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]: #Press Space to shoot left cannon
                    cannon(Vec2d(LeftBalloon.pos.x + (65/200), LeftBalloon.pos.y - (140/200)), Vec2d(3, 3))
                if keys[pygame.K_u]:
                    cannon(Vec2d(RightBalloon.pos.x + (60/200), RightBalloon.pos.y - (140/200)), Vec2d(-3, 3))
                
                
        # Move each object according to physics
        for obj in objects:
            obj.update(dt)
            
            # Remove objects off the screen
            if (obj.pos.y < -2):
                objects.remove(obj)
                del obj
            
        # Update the balloons
        LeftBalloon.update(dt)
        RightBalloon.update(dt)

        # Drawing
        screen.fill(WHITE) # wipe the screen
        screen.blit(draw_screen, (0, 0)) # draw the trail semitransparent
        screen.blit(background, (0,0))
        for obj in objects:
            obj.draw(screen, coords) # draw object to screen
            #obj.draw(draw_screen, coords) # add object to trail in draw_screen
            
        # Draw the balloons
        LeftBalloon.draw(screen, coords)
        RightBalloon.draw(screen, coords)
        
        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second
        clock.tick(frame_rate)
        
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e
