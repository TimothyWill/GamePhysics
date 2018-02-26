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
    
    #Import background
    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, (800, 600))
 
    #Initialize screen and coords
    width = 800
    height = 600
    screen = pygame.display.set_mode([width,height])
    screen_center = Vec2d(width/2, height/2)
    coords = Coords(screen_center.copy(), 1, True)
    # ^ Center of window is (0,0), scale is 1:1, and +y is up
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Initialize menu
    startButton = pygame.Rect(250, 300, 300, 50)
    quitButton = pygame.Rect(250, 400, 300, 50)
    
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    title = myfont.render('BALLOON FORCE', False, (0, 0, 0))
    play = myfont.render('Play', False, (0, 0, 0))
    quitGame = myfont.render('Quit', False, (0, 0, 0))

    # Initialize the balloons
    LeftBalloon  = Balloon(Vec2d(0, 0), 30, Vec2d(-1.5, 1), 0.05, BLUE, 9.8, pygame.K_w)
    RightBalloon = Balloon(Vec2d(0, 0), 30, Vec2d(1.5, 1), 0.05, BLUE, 9.8, pygame.K_i)
    RightBalloon.image = pygame.transform.flip(RightBalloon.image, True, False)

    #Cannon ball collector
    objects = []

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
        
    # Main game loop
    exitGame = False
    while not exitGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button
                if quitButton.collidepoint(mouse_pos):
                    exitGame = True
                if startButton.collidepoint(mouse_pos):
                    done = False
                    while not done:
                        # --- Main event loop
                        for event in pygame.event.get(): 
                            if event.type == pygame.QUIT: # If user clicked close
                                done = True
                                exitGame = True
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
                    
                        # Draw background
                        screen.blit(background, (0,0))
                        
                        # Draw cannon balls
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
              
        # Draw background
        screen.blit(background, (0,0))
            
        # Draw buttons
        pygame.draw.rect(screen, GRAY, startButton)
        pygame.draw.rect(screen, GRAY, quitButton)
    
        # Draw Text
        screen.blit(title, (275,100))
        screen.blit(play, (380,300))
        screen.blit(quitGame, (380,400))
        
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
