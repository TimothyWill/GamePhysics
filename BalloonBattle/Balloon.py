import pygame
from vec2d import Vec2d

class Balloon:
    
    def __init__(self, pVel, pMass, pPos, pRadius, pColor, pHeat, pUpKey):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("hotairballoon.png")
        self.image = pygame.transform.scale(self.image, (130, 170))
        self.pos = Vec2d(pPos.x - (65/200), pPos.y - (85/200))
        self.vel = pVel
        self.mass = pMass
        self.mom = pMass * pVel
        self.color = pColor
        self.heat = pHeat
        self.heatLoss = 3;
        self.upKey = pUpKey
        self.radius = pRadius
        
    def update(self, dt):
        #print("HEAT: " + str(self.heat))
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
        screen.blit(self.image,coords.pos_to_screen(self.pos).int())