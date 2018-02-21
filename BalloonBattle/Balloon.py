import pygame
from vec2d import Vec2d

class Balloon:
    
    def __init__(self, pVel, pMass, pPos, pRadius, pColor, pHeat, pUpKey):
        self.pos = pPos
        self.vel = pVel
        self.mass = pMass
        self.mom = pMass * pVel
        self.color = pColor
        self.heat = pHeat
        self.heatLoss = 3;
        self.upKey = pUpKey
        self.radius = pRadius
        
    def update(self, dt):
        print("HEAT: " + str(self.heat))
        # lose heat
        self.heat -= self.heatLoss * dt
        # add heat
        keys = pygame.key.get_pressed()
        if keys[self.upKey]:
            print("Button Pressed")
            self.heat += dt * 6;
        else:
            self.heat -= dt;

        # Check heat amount
        if self.heat <= 7:
            self.heat = 7  
        elif self.heat >= 13:
            self.heat = 13
        
        # Calculate force from the heat
        self.force = Vec2d(0, self.heat)
        
        # Apply Gravity
        self.force += Vec2d(0, -9.8)
        
        # Apply Air Resistance
        self.force -= (100 * self.vel.get_length() ** 2) * self.vel.normalized();
        
        self.mom += self.force*dt
        self.vel.copy_in(self.mom/self.mass)
        self.pos += self.vel*dt
        
        
        
    def draw(self, screen, coords):
        pygame.draw.circle(screen, self.color, 
                           coords.pos_to_screen(self.pos).int(), 
                           int(coords.scalar_to_screen(self.radius)), 0)