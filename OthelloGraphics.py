 # -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd
"""
import pygame

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
GRAY     = ( 127, 127, 127)

def main():
    pygame.init()
    font = pygame.font.SysFont('Calibri', 25, True, False)
 
    width = 255
    height = 255
    screen = pygame.display.set_mode([width,height])
    grid = []
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # -------- Main Program Loop -----------\
    done = False
    while not done:
        # --- Main event loop
        """ Event Handling """
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # If user clicked close
                done = True
            elif event.type == pygame.KEYDOWN:
                #print(event.key, event.mod, event.unicode)
                if event.key == pygame.K_ESCAPE:
                    print("Escape key pressed.")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // 25
                row = pos[1] // 25
                if row < 8 and column < 8:
                    grid[row][column] = 1
                    print(row, column)
                    if grid[row][column] == 1:
                        print("You have clicked the square:",row,",",column)
        
        """ State Checking """
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            print("SPACEBAR!!!")
            background_color = BLACK
        else:
            background_color = WHITE 
        
        # --- Drawing code should go here
        # First, clear the screen
        screen.fill(background_color) 
        # Now, do your drawing.
        
        #text = font.render(str(pygame.mouse.get_pos()),True, BLACK)
        #screen.blit(text, [0,0])
        
        
        for row in range(8):
            grid.append([])
            for column in range(8):
                grid[row].append(0)
                
        for row in range(8):
            for column in range(8):
                color = RED
                if grid[row][column] == 1:
                    color = BLUE
                pygame.draw.rect(screen, color, [(5+20) * column + 5, 
                                               (5+20) * row + 5,
                                               20, 20])
        
        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise
