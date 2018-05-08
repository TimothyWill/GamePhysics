# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd
"""
import pygame
from vec2d import Vec2d
from coords import Coords
from polygon_stub import Polygon
from wallPolygon import Wall
from math import sqrt, acos, degrees, sin, cos
from random import randint, random
from decimal import Decimal

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
GRAY     = ( 127, 127, 127)
CLEARGRAY     = ( 127, 127, 127, 10)

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

def make_polygon(radius, n, angle=0, factor=1, axis=Vec2d(1,0)):
    axis = axis.normalized()
    vec = Vec2d(0, -radius).rotated(180/n+angle)
    p = []
    for i in range(n):
        v = vec.rotated(360*i/n)
        v += v.dot(axis)*(factor-1)*axis
        p.append(v)
    #print(p)
    return p

def make_rectangle(length, height, angle=0):
    points = (Vec2d(-0.5,-0.5),
              Vec2d(+0.5,-0.5),
              Vec2d(+0.5,+0.5),
              Vec2d(-0.5,+0.5),
              )
    c = cos(angle)
    s = sin(angle)
    for p in points:
        p.x *= length
        p.y *= height
        x = p.x*c - p.y*s
        y = p.y*c + p.x*s
        p.x = x
        p.y = y
    return points
        
def check_collision(a, b, result=[]):
    result.clear()
    result1 = []
    result2 = []
    if a.check_collision(b, result1) and b.check_collision(a, result2):
        if result1[2] < result2[2]: # compare overlaps, which is smaller
            result.extend(result1)
        else:
            result.extend(result2)
        return True
    return False       
            
def resolve_collision(result):
    (a, b, d, n, pt) = result
    e = 0.5
    if a.type == "wall" or b.type == "wall":
        mu = 1.0
    else:
        mu = 0.4
    m = a.mass*b.mass/(a.mass + b.mass) # reduced mass
    
    # depenetrate
    a.pos += d*n*m/a.mass
    pt += d*n*m/a.mass
    b.pos -= d*n*m/b.mass
    
    # Initialize Some Variables
    tHat = n.perpendicular()
    nHat = n 
    
    ra = pt - a.pos
    rb = pt - b.pos
    ran = ra.dot(nHat)
    rat = ra.dot(tHat)
    rbn = rb.dot(nHat)
    rbt = rb.dot(tHat)
    
    Vrel = (a.vel + a.angvel * ra.perpendicular()
            - (b.vel + b.angvel * rb.perpendicular()))
    
    vn = Vrel.dot(nHat)
    vt = Vrel.dot(tHat)
    
    deltaVn = -(1 + e) * vn
    deltaVt = -vt

    A = 1/m + rat*rat/a.moment + rbt*rbt/b.moment
    B = -ran*rat/a.moment - rbn*rbt/b.moment
    C = B
    D = 1/m + ran*ran/a.moment + rbn*rbn/b.moment
    det = A*D - B*C

    Jn = (D*deltaVn - B*deltaVt)/det
    Jt = (-C*deltaVn + A*deltaVt)/det
    
    if deltaVn > 0:
        if abs(Jt) > mu * Jn:
            s = mu
            if Jt < 0:
                s *= -1
            Jn = deltaVn/(1/m + rat*(rat - s*ran)/a.moment
                              + rbt*(rbt - s*rbn)/b.moment)
            #Jn = (deltaVn + B*Jt)/A
            Jt = s*Jn
        
        PE = d*m*-10
        Ja = Jn*nHat + Jt*tHat - Vec2d(0,PE)
        Jb = Jn*nHat + Jt*tHat + Vec2d(0,PE)
        
        if a.type == "polygon" and b.type == "polygon":
            if not a.breakable and b.breakable:
                if Jb.x > 2 or Jb.x < -2 or Jb.y > 2 or Jb.y < -2:
                    b.destroyed = True
        
        a.impulse(Ja,pt)
        b.impulse(-Jb,pt)
    
def main():
    pygame.init()
    
    # Variable where the position where the new ball will be placed is stored
    mouseDownPosition = Vec2d(-1, -1);
    
    #Import images
    background = pygame.image.load("background.png")
    background = pygame.transform.scale(background, (1600, 600))
    
    background2 = pygame.image.load("background2.png")
    background2 = pygame.transform.scale(background2, (1600, 600))
 
    width = 800
    height = 600
    screen = pygame.display.set_mode([width,height])
    screen_center = Vec2d(width/2, height/2)
    coords = Coords(screen_center.copy(), 1, True)
    zoom = 100
    coords.zoom_at_coords(Vec2d(0,0), zoom) 
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    # Initialize menu
    startButton = pygame.Rect(250, 200, 300, 50)
    controlsButton = pygame.Rect(250, 300, 300, 50)
    quitButton = pygame.Rect(250, 400, 300, 50)
    backButton = pygame.Rect(250, 500, 300, 50)
    
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    title = myfont.render('GRUMPY LIZADS', False, (0, 0, 0))
    play = myfont.render('Play', False, (0, 0, 0))
    controls = myfont.render('Controls', False, (0, 0, 0))
    quitGame = myfont.render('Quit', False, (0, 0, 0))
    back = myfont.render('Back', False, (0, 0, 0))

    # -------- Main Program Loop -----------\
    frame_rate = 60
    n_per_frame = 10
    playback_speed = 1 # 1 is real time, 10 is 10x real speed, etc.
    dt = playback_speed/frame_rate/n_per_frame
    
    # Variable where the position where the new ball will be placed is stored
    mouseDownPosition = Vec2d(-1, -1);

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
                if controlsButton.collidepoint(mouse_pos):
                    fire = myfont.render('Fire:   Left Click and Drag', False, (0, 0, 0))
                    panRight = myfont.render('Pan Right:   Right Arrow Key', False, (0, 0, 0))
                    panLeft = myfont.render('Pan Left:   Left Arrow Key', False, (0, 0, 0))
                    controlsDone = False
                    while not controlsDone:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT: # If user clicked close
                                controlsDone = True
                                exitGame = True
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = event.pos
                                
                                if backButton.collidepoint(mouse_pos):
                                    controlsDone = True
                        # Draw
                        screen.blit(background, (0,0))
                        screen.blit(title, (275,100))
                        
                        pygame.draw.rect(screen, GRAY, backButton)
                        screen.blit(back, (370,500))
                        
                        screen.fill(CLEARGRAY, pygame.Rect(200, 200, 400, 50))
                        screen.fill(CLEARGRAY, pygame.Rect(200, 300, 400, 50))
                        screen.fill(CLEARGRAY, pygame.Rect(200, 400, 400, 50))
                        
                        screen.blit(fire, (225, 200))
                        screen.blit(panRight, (205, 300))
                        screen.blit(panLeft, (220, 400))
                        
                        # --- Update the screen with what we've drawn.
                        pygame.display.update()
                    
                        # This limits the loop to 60 frames per second
                        clock.tick(frame_rate)
                
                
                if startButton.collidepoint(mouse_pos):
                    # Create initial objects to demonstrate
                    objects = []
                    backgroundOffset = 0
                    mouseDownPosition = Vec2d(-1, -1)
                    score = 0
                    scoreText = myfont.render("Score = "+str(score), False, (255, 255, 255))
                
                    objects.append(Polygon(Vec2d(2,-1), Vec2d(0,0), 1, make_rectangle(2, 1), GRAY, 0, 0))
                    objects.append(Polygon(Vec2d(2, 1), Vec2d(0,0), 1, make_rectangle(0.1, 3), GRAY, 0, 0))
                    #objects.append(Polygon(Vec2d(-.75, .6), Vec2d(0,0), 1, make_rectangle(0.25, 1.5), GRAY, 0, 0))
                    #objects.append(Polygon(Vec2d(.75, .6), Vec2d(0,0), 1, make_rectangle(0.25, 1.5), GRAY, 0, 0))
                    #objects.append(Polygon(Vec2d(0, 1), Vec2d(0,0), 1, make_rectangle(0.5, 1.0), GRAY, 0, 0))
                    #objects.append(Polygon(Vec2d(0, 2), Vec2d(0,0), 1, make_rectangle(2.0, 1.0), GRAY, 0, 0))
                    #objects.append(Polygon(Vec2d(-0.5,1), Vec2d(0,0), 1, make_polygon(0.2,4,0,10), RED, 0, 1))
                    #objects.append(Polygon(Vec2d(1,0), Vec2d(0,0), 1, make_polygon(0.3,7,0,3), BLUE, 0, -0.4))
                    #objects.append(Polygon(Vec2d(-1,0), Vec2d(0,0), 1, make_polygon(1,3,0,0.5), GREEN, 0, 2))
                    
                    # Walls
                    objects.append(Wall(Vec2d(0,-2.25), Vec2d(0,1), BLACK))
                    objects.append(Wall(Vec2d(-4,0), Vec2d(1,0), BLACK))
                    objects.append(Wall(Vec2d(12,0), Vec2d(-1,0), BLACK))
    
                    done = False
                    lineDrawn = False
                    count = 0
                    max_collisions = 1
                    result = []
                    while not done:
                        # --- Main event loop
                        for event in pygame.event.get(): 
                            if event.type == pygame.QUIT: # If user clicked close
                                objects = []
                                exitGame = True
                                done = True
                            elif event.type == pygame.KEYDOWN: 
                                if event.key == pygame.K_ESCAPE:
                                    objects = []
                                    done = True
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if pygame.mouse.get_pressed()[0] and mouseDownPosition.x == -1:
                                    # Set mouseDownPosition to the currernt position
                                    mouseDownPosition = Vec2d(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                                    lineDrawn = True
                                    
                        # When the user releases the mouse button
                        if pygame.mouse.get_pressed()[0] == False and mouseDownPosition.x != -1:
                            # Calculate the velocity based on the distance between the two mouse positions
                            newVelocityX = (mouseDownPosition.x - pygame.mouse.get_pos()[0]) * 0.07
                            newVelocityY = (mouseDownPosition.y - pygame.mouse.get_pos()[1]) * -0.07
                            # Create the new ball
                            #cannon(Vec2d(-3, 0), Vec2d(newVelocityX,newVelocityY))
                            objects.append(Polygon(Vec2d(-3, 0), Vec2d(newVelocityX,newVelocityY), 1, make_polygon(0.3,8,0,1), BLACK, 0, 0, False))
                            count += 1
                            print(count)
                            mouseDownPosition = Vec2d(-1, -1)
                            lineDrawn = False

                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_RIGHT]:
                            if(backgroundOffset > -800):
                                coords.pan_in_coords(Vec2d(.1,0))
                                backgroundOffset -= 10
                        if keys[pygame.K_LEFT]:
                            if(backgroundOffset < 0):
                                coords.pan_in_coords(Vec2d(-.1,0))
                                backgroundOffset += 10
                        
                        for N in range(n_per_frame):
                            # Physics
                            # Calculate the force on each object
                            for obj in objects:
                                obj.force.zero()
                                obj.force += Vec2d(0,-10) # gravity
                       
                            # Move each object according to physics
                            for obj in objects:
                                obj.update(dt)
                                
                            for i in range(max_collisions):
                                collided = False
                                for i1 in range(len(objects)):
                                    for i2 in range(i1):
                                        if check_collision(objects[i1], objects[i2], result):
                                            resolve_collision(result)
                                            collided = True
                                            #print("Collision")
                                            #paused = True
                                if not collided: # if all collisions resolved, then we're done
                                    break
                 
                        # Draw background
                        screen.blit(background, (backgroundOffset,0))
                        
                        # Drawing
                        for obj in objects:
                            obj.draw(screen, coords) # draw object to screen
                            
                        for obj in objects:
                            obj.update(dt)
                            if obj.destroyed:
                                #Update Score
                                score += round(Decimal(obj.mass),2)
                                scoreText = myfont.render("Score = "+str(score), False, (255, 255, 255))
                                
                                #Delete destroyed objects
                                objects.remove(obj)
                                del obj
                                
                            if count > 3:
                                #>add reset for balls
                                count = 0
                        
                        screen.blit(background2, (backgroundOffset,0))
                        
                        # Draw score
                        screen.blit(scoreText, (50,50))
                        
                        if lineDrawn:
                            pygame.draw.line(screen, BLACK, mouseDownPosition, pygame.mouse.get_pos(), 1)
                        # --- Update the screen with what we've drawn.
                        pygame.display.update()
        
                        # This limits the loop to the specified frame rate
                        clock.tick(frame_rate)

        # Draw background
        screen.blit(background, (0,0))
            
        # Draw buttons
        pygame.draw.rect(screen, GRAY, startButton)
        pygame.draw.rect(screen, GRAY, controlsButton)
        pygame.draw.rect(screen, GRAY, quitButton)
    
        # Draw Text
        screen.blit(title, (275,100))
        screen.blit(play, (370,200))
        screen.blit(controls, (340,300))
        screen.blit(quitGame, (370,400))

        # --- Update the screen with what we've drawn.
        pygame.display.update()
        
        # This limits the loop to the specified frame rate
        clock.tick(frame_rate)
        
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise
