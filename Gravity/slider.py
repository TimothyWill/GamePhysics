import pygame
import math

class Slider:
    def __init__(self, minValue, maxValue, startValue, position, size):
        self.maxValue = maxValue
        self.minValue = minValue
        self.value = startValue
        self.sliderBar = (position, size)
        self.dialPositionY = position[1] + size[1]/2
        self.dialPositionX = position[0]
        self.barColor = (0, 0, 0)
        self.dialColor = (50, 50, 50)
        self.sliding = True
        self.dialRadius = 17
        self.position = position
        self.size = size
        
        self.sliderBar = pygame.Rect(position, size)
        
    def update(self):
        # Check for user clicking on the dial
        if pygame.mouse.get_pressed()[0] and self.mouseOverlapWithDial():
            self.sliding = True
        elif pygame.mouse.get_pressed()[0] == False:
            self.sliding = False
                
        # if it's sliding, move the dial
        if self.sliding:
            # if the cursor is to the left of the slider
            if pygame.mouse.get_pos()[0] <= self.position[0]:
                self.dialPositionX = self.position[0]
            # if the cursor is to the right of the slider
            elif pygame.mouse.get_pos()[0] >= self.position[0] + self.size[0]:
                self.dialPositionX = self.position[0] + self.size[0]
            # Base Case
            else:
                self.dialPositionX = pygame.mouse.get_pos()[0]

        
        
        
    def draw(self, screen):
        # Draw the slider bar
        pygame.draw.rect(screen, self.barColor, self.sliderBar)
        # Draw the slider dial
        pygame.draw.circle(screen, self.dialColor, (int(self.dialPositionX), int(self.dialPositionY)), self.dialRadius)
        
    def mouseOverlapWithDial(self):
        # Calculate the distance between the mouse and the center of the dial
        xDistance = self.dialPositionX - pygame.mouse.get_pos()[0]
        yDistance = self.dialPositionY - pygame.mouse.get_pos()[1]

        hypDistance = math.hypot(xDistance, yDistance)
        
        if hypDistance <= self.dialRadius:
            return True
        return False
    
    def getValue(self):
        # Get the slider's position as a value between 0 and 1
        relativePosition = (self.dialPositionX - self.position[0]) / self.size[0]
        print("Relative Position: " + str(relativePosition))
        value = relativePosition * (self.maxValue - self.minValue) + self.minValue
        print("Value: " + str(value))
        return value

       