import pygame
from vec2d import Vec2d

class Balloon:
    
    def __init__(self, pVel, pMass, pPos, pRadius, pColor, pHeat, pUpKey):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("hotairballoon.png")
        self.image = pygame.transform.scale(self.image, (130, 170))
        self.fire = pygame.image.load("fire.png")
        self.fire = pygame.transform.scale(self.fire, (130, 170))
        self.pos = Vec2d(pPos.x - (65/200), pPos.y - (85/200))
        self.vel = pVel
        self.mass = pMass
        self.mom = pMass * pVel
        self.color = pColor
        self.airLoss = 3
        self.upKey = pUpKey
        self.radius = pRadius
        self.outsideTemp = 292
        self.insideTemp = 394
        self.heatLossConstant = 1
        self.densityConstant = 1
        self.insideDensity = 1
        self.outsideDensity = 1
        self.lampTemp = 100
        self.onFire = False
        
    def update(self, dt):
        # lose temp to heat
        self.loseHeat(dt)
        
        # add air
        keys = pygame.key.get_pressed()
        if keys[self.upKey]:
            #print("Button Pressed")
            self.addHeat(dt)
            self.onFire = True
        else:
            self.onFire = False
            
        # calculate density
        self.calculateDensity()

        
        self.calculateBuoyantForce()
        print(self.force)
        
        # Apply Gravity
        self.force += Vec2d(0, -9.8)
        
        self.mom += self.force*dt
        self.vel.copy_in(self.mom/self.mass)
        self.pos += self.vel*dt
        
    def loseHeat(self, dt):
        self.insideTemp -= -self.heatLossConstant * (self.outsideTemp - self.insideTemp) * dt
        #print ("Temperature: " + str(self.insideTemp))

    def addHeat(self, dt):
        self.insideTemp += self.lampTemp * dt
        
    def calculateDensity(self):
        self.insideDensity = self.outsideTemp * self.outsideDensity / self.insideTemp
        #print("Density: " + str(self.insideDensity))

    def calculateBuoyantForce(self):
        self.force = Vec2d(0, (self.outsideDensity - self.insideDensity) * 100)        
        
    def getHit(self):
        self.heatLossConstant += 1.0
        
    def draw(self, screen, coords):
        if self.onFire:
            screen.blit(self.fire,coords.pos_to_screen(self.pos).int())
        screen.blit(self.image,coords.pos_to_screen(self.pos).int())