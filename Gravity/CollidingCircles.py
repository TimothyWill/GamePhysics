# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd
"""
import pygame
from vec2d import Vec2d
from coords import Coords
#from circle import Circle
from rotating_circle import RotatingCircle
from random import randint, random
from wall import Wall

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

# apply gravity between the two objects
def gravity_force(obj1, obj2):
    """ compute the force on each object
        add to each, equal and opposite """
    r = obj1.pos - obj2.pos # distance between two objects
    m1 = obj1.mass # mass of 1st object
    m2 = obj2.mass # mass of 2nd object
    G = 1 #6.67384*(10**(-11)) # gravitational constant
    force = -((G*m1*m2)/r.mag2())*r.hat() # this is the formula for gravity
    #force = 1*(r.mag()-obj1.radius)*r.hat() # repulsion force
    
    obj1.force += force
    obj2.force -= force

def collides(obj1, obj2):
    if (obj1.pos.get_distance(obj2.pos) < obj1.radius + obj2.radius):
        e = 0.5
        m1 = obj1.mass
        m2 = obj2.mass
        r = obj2.pos - obj1.pos
        u = 1/((1/m1) + (1/m2))
        v1 = obj1.vel
        v2 = obj2.vel
        n = (obj2.pos - obj1.pos).normalized()
        J = (1 + e)*u*((v2 - v1).dot(n))
        d = obj1.radius + obj2.radius - (obj1.pos - obj2.pos).mag()
        L = u*r.cross(v2 - v1)
        Jang = -d*L/(r.mag()*(r.mag()+d)) * n.perpendicular()
        obj1.mom -= Jang
        obj2.mom += Jang
        obj1.pos = obj1.pos - (u/m1)*d*n
        obj2.pos = obj2.pos + (u/m2)*d*n
        if (J < 0):
            obj1.mom += J * n
            obj2.mom -= J * n
            obj1.update_vel()
            obj2.update_vel()
            
def collideWithWalls(obj, wall):
    R = obj.radius
    n = wall.normal
    d = R - (n.dot(obj.pos - wall.pos1))
    tangent = n.perpendicular_normal()
    if (d > 0):
        m = obj.mass
        #r = obj.pos - wall.pos1
        u = m
        v1 = obj.vel
        J = 1.6*u*((v1).dot(n))
        #d = obj.radius - (r).dot(n.hat())
        #L = u*r.cross(v1)
        #Jang = -d*L/(r.mag()*(r.mag()+d)) * n.perpendicular()
        #obj.mom -= Jang
        obj.pos = obj.pos + (u/m)*d*n
        if (J < 0):
            obj.mom -= J * n
            
        Fric = -obj.mass * obj.vel.dot(tangent)
        cf = 0.75 # Coefficient of Friction
        
        if (abs(Fric) > cf * J):
            ratio = cf * J/abs(Fric)
            Fric *= ratio
        else:
            ratio = 1
        
        ratio *= obj.vel.dot(tangent)/obj.vel.dot(n)
       # obj.pos -= (obj.radius - d) * ratio * tangent
        
        obj.mom -= Fric * tangent
            
# Add a new circle to the scene
def addNewBall(width, height, objects, zoom, position, coords, velocity):
    # Get the radius of the ball from the slider
    radius = randint(5,20)*.1
    # Calculate the mass based on the radius
    mass = radius
    # Add the circle to the array
    objects.append(RotatingCircle(coords.pos_to_coords(position), velocity,
                              mass, radius, random_bright_color(),BLACK, random()*2*3.14))

def main():
    # Variable where the position where the new ball will be placed is stored
    mouseDownPosition = Vec2d(-1, -1);
    
    pygame.init()
 
    width = 800
    height = 600
    screen = pygame.display.set_mode([width,height])
    screen_center = Vec2d(width/2, height/2)
    coords = Coords(screen_center.copy(), 1, True)
    zoom = 30
    coords.zoom_at_coords(Vec2d(0,0), zoom) 
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    objects = []
    walls = []
    #mass = 1
    #radius = 1
    #mass = radius*radius*20
    #objects.append(Circle(Vec2d(-5, 5), Vec2d(0,0), 2*mass, 2*radius, random_bright_color()))
    #objects.append(Circle(Vec2d(2, 0), Vec2d(0, 0), mass, radius, random_bright_color()))
    #objects.append(Circle(Vec2d(2, 4), Vec2d(0, 0), mass/3, radius/3, random_bright_color()))
    #objects.append(Circle(Vec2d(0, -2), Vec2d(0, 0), mass/2, radius/2, random_bright_color()))
    #objects.append(Circle(Vec2d(2, 0), Vec2d(-1, 0), 4*mass, 4*radius, random_bright_color()))
    
    walls.append(Wall(Vec2d(10,0), Vec2d(0,-10), 0, BLACK))
    walls.append(Wall(Vec2d(0,-10), Vec2d(-10,-2), 0, BLACK))


    # -------- Main Program Loop -----------\
    frame_rate = 60
    playback_speed = 1 # 1 is real time, 10 is 10x real speed, etc.
    dt = playback_speed/frame_rate
    print("timestep =", dt)

    done = False
    while not done:
        # --- Main event loop
        if pygame.mouse.get_pressed()[0] and mouseDownPosition.x == -1:
            # Set mouseDownPosition to the currernt position
            mouseDownPosition = Vec2d(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        # When the user releases the mouse button
        elif pygame.mouse.get_pressed()[0] == False and mouseDownPosition.x != -1:
            # Calculate the velocity based on the distance between the two mouse positions
            newVelocityX = (mouseDownPosition.x - pygame.mouse.get_pos()[0]) * -0.05
            newVelocityY = (mouseDownPosition.y - pygame.mouse.get_pos()[1]) * 0.05
            # Create the new ball
            addNewBall(width, height, objects, zoom, mouseDownPosition, coords, Vec2d(newVelocityX, newVelocityY))
            mouseDownPosition = Vec2d(-1, -1)
            
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # If user clicked close
                done = True
               
        for obj in objects:
            obj.force.zero()
            obj.force -= Vec2d(0,60)                        
            
        # Move each object according to physics
        for obj in objects:
            obj.update(dt)
            
        maxCollisions = 50
        
        for i in range(maxCollisions):
            collided = False
            for i1, obj1 in enumerate(objects):
                for i2, obj2 in enumerate(objects):
                    if i1 < i2:
                        collides(obj1, obj2)
                        collided = True
                if not collided:
                    break
                
        #for i in range(maxCollisions):
         #   collided = False
          #  for i1 in range(len(objects)):
           #     for i2 in range(i1):
            #        collides(objects[i1], objects[i2])
             #   if not collided:
              #      break
        
        for i1, obj1 in enumerate(objects):
            for i2, wall1 in enumerate(walls):
                collideWithWalls(obj1,wall1)

        # Drawing
        screen.fill(WHITE) # wipe the screen
        for obj in objects:
            obj.draw(screen, coords) # draw object to screen
        
        for wall in walls:
            wall.draw(screen, coords)
            
        #pygame.draw.lines(screen, BLACK, False, [coords.pos_to_screen(Vec2d(1,1)), coords.pos_to_screen(Vec2d(1,2))], 1)
            
        L = 0
        for obj in objects:
            L += obj.pos.cross(obj.mom)
        print(L)
        
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

