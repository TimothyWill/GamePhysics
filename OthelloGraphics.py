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
TAN      = ( 210, 180, 140)

grid = []

class Pair:
    def __init__(self, pX, pY):
        self.x = pX
        self.y = pY

def main():
    pygame.init()
    font = pygame.font.SysFont('Calibri', 25, True, False)
 
    width = 255
    height = 255
    screen = pygame.display.set_mode([width,height])

    for row in range(8):
        grid.append([])
        for column in range(8):
            grid[row].append(" ")
    grid[3][3] = "B"
    grid[3][4] = "W"
    grid[4][3] = "W"
    grid[4][4] = "B"
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # -------- Main Program Loop -----------\
    numberPassed = 0
    whiteScore = 0
    blackScore = 0
    done = False
    player = "Black"
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
            # Player clicks a square
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[1] // 25
                row = pos[0] // 25
                if row < 8 and column < 8:
                    if player == "White":
                        if checkPoint(row, column, "W", "B"):
                            numberPassed = 0
                            player = "Black"
                            addToGrid(row, column, "W")
                        elif (checkAvailableMoves("W", "B") == 0):
                            print("White Turn Forfeited")
                            player = "Black"
                            numberPassed += 1
                    else:
                        if checkPoint(row, column, "B", "W"):
                            numberPassed = 0
                            player = "White"
                            addToGrid(row, column, "B")
                        elif (checkAvailableMoves("W", "B") == 0):
                            print("Black Turn Forfeited")
                            player = "White"
                            numberPassed += 1
                    
                    print("You have clicked the square:",row + 1,",",column + 1)
                    
                    # Update score
                    for x in range(0, 8):
                        for y in range(0, 8):
                            if getFromGrid(x, y) == "W":
                                whiteScore += 1
                            elif getFromGrid(x, y) == "B":
                                blackScore += 1
                        
                    # Check for game over
                    if numberPassed == 2:
                        print("\nGame Over")
                        print("")
                        done = True
                        
                        if blackScore > whiteScore:
                            print("\033[4m\nBlack Wins!\n\033[0m")
                        elif whiteScore > blackScore:
                            print("\033[4m\nWhite Wins!\n\033[0m")
                        else:
                            print("\033[4m\nTie\033[0m")
        
        """ State Checking """
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            print("SPACEBAR!!!")
            background_color = BLACK
        else:
            background_color = BLACK
        
        # --- Drawing code should go here
        # First, clear the screen
        screen.fill(background_color) 
        # Now, do your drawing.
        
        #text = font.render(str(pygame.mouse.get_pos()),True, BLACK)
        #screen.blit(text, [0,0])
        
        

                
        for row in range(8):
            for column in range(8):
                color = TAN
                if grid[row][column] == "W":
                    color = WHITE
                elif grid[row][column] == "B":
                    color = BLACK
                pygame.draw.rect(screen, TAN, [(5+20) * column + 5, 
                                               (5+20) * row + 5,
                                               20, 20])
                pygame.draw.circle(screen, color, [(5+10) * column + (10 * column) + 15,
                                                   (5+10) * row + (10 * row) + 15]
                                                    ,10)
        
        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second
        clock.tick(60)
        
    pygame.quit()

def getFromGrid(rows, columns):
    return grid[columns][rows]

def addToGrid(x, y, icon):
    grid[y][x] = icon
    
def checkAvailableMoves(icon, opponentIcon):
    
    possibleMoves = 0

    # Loop through entire grid
    for x in range(0, 8):
        for y in range(0, 8):
            validMove = False
            
            if getFromGrid(x, y) == " ":
    
                # Check for Flipping
                
                # Check to the Right
                FlipList = []
                for i in range(1, 8 - x):
                    # If the tile has your opponent's icon
                    if getFromGrid(x + i, y) == opponentIcon:
                        FlipList.append(Pair(x + i, y))
                    # If the tile has your own icon
                    elif getFromGrid(x + i, y) == icon:
                        # Check valid move        
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
            
                # Check to the Left
                FlipList = []
                for i in range(1, x + 1):
                    # If the tile has your opponent's icon
                    if getFromGrid(x - i, y) == opponentIcon:
                        FlipList.append(Pair(x - 1, y))
                    # If the tile has your own icon
                    elif getFromGrid(x - i, y) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
         
                # Check Down
                FlipList = []
                for i in range(1, 8 - y):
                    # If the tile has your opponent's icon
                    if getFromGrid(x, y + i) == opponentIcon:
                        FlipList.append(Pair(x, y + i))
                    # If the tile has your own icon
                    elif getFromGrid(x, y + i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
                
                # Check Up
                FlipList = []
                for i in range(1, y + 1):
                    # If the tile has your opponent's icon
                    if getFromGrid(x, y - i) == opponentIcon:
                        FlipList.append(Pair(x, y - i))
                    # If the tile has your own icon
                    elif getFromGrid(x, y - i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
   
                # Check Up-Right             
                FlipList = []

                distY = y + 1
                distX = 8 - x
                minimumDistance = 0
                
                if distY < distX:
                    minimumDistance = distY
                else:
                    minimumDistance = distX
                
                for i in range(1, minimumDistance):
                    # If the tile has your opponent's icon
                    if getFromGrid(x + i, y - i) == opponentIcon:
                        FlipList.append(Pair(x + i, y - i))
                    # If the tile has your own icon
                    elif getFromGrid(x + i, y - i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break

                # Check Up-Left               
                FlipList = []

                distY = y + 1
                distX = x + 1
        
                if distY < distX:
                    minimumDistance = distY
                else:
                    minimumDistance = distX
                
                for i in range(1, minimumDistance):
                    # If the tile has your opponent's icon
                    if getFromGrid(x - i, y - i) == opponentIcon:
                        FlipList.append(Pair(x - i, y - i))
                    # If the tile has your own icon
                    elif getFromGrid(x - i, y - i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
  
                # Check Down-Left              
                FlipList = []

                distY = 8 - y
                distX = x + 1
                
                if distY < distX:
                    minimumDistance = distY
                else:
                    minimumDistance = distX
                
                for i in range(1, minimumDistance):
                    # If the tile has your opponent's icon
                    if getFromGrid(x - i, y + i) == opponentIcon:
                        FlipList.append(Pair(x - i, y + i))
                    # If the tile has your own icon
                    elif getFromGrid(x - i, y + i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
    
                # Down-Right            
                FlipList = []
                    
                distY = 8 - y
                distX = 8 - x
                
                if distY < distX:
                    minimumDistance = distY
                else:
                    minimumDistance = distX
                
                for i in range(1, minimumDistance):
                    # If the tile has your opponent's icon
                    if getFromGrid(x + i, y + i) == opponentIcon:
                        FlipList.append(Pair(x + i, y + i))
                    # If the tile has your own icon
                    elif getFromGrid(x + i, y + i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                        break
                    else:
                        break
                
                FlipList = []
                
                if validMove:
                    #print(y,x)
                    possibleMoves += 1
    
    return possibleMoves

def checkPoint(x, y, icon, opponentIcon):
    # print("X: " + str(x) + "Y: " + str(y))
    
    validMove = False
    
    if getFromGrid(x, y) == " ":

        # Check for Flipping
        
        # Check to the right
        FlipList = []
        for i in range(1, 8 - x):
            # If the tile has your opponent's icon
            if getFromGrid(x + i, y) == opponentIcon:
                FlipList.append(Pair(x + i, y))
                # print(str(i)+", "+str(x)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x + i, y) == icon:
                # print(str(x)+", "+str(i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    # Grid[j.x][j.y] = icon
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(i)+", "+str(x)+" is blank")
                break
        
        # List of disks to be flipped
        FlipList = []
        # Check to the left
        for i in range(1, x + 1):
            # If the tile has your opponent's icon
            if getFromGrid(x - i, y) == opponentIcon:
                FlipList.append(Pair(x - i, y))
                # print(str(i)+", "+str(x)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x - i, y) == icon:
                # print(str(x)+", "+str(i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    # Grid[j.x][j.y] = icon
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(i)+", "+str(x)+" is blank")
                break
        
        FlipList = []
        # Check Down
        for i in range(1, 8 - y):
            # If the tile has your opponent's icon
            if getFromGrid(x, y + i) == opponentIcon:
                FlipList.append(Pair(x, y + i))
                # print(str(y)+", "+str(i)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x, y + i) == icon:
                # print(str(y)+", "+str(i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(y)+", "+str(i)+" is blank")
                break
            
        FlipList = []
        # Check Up
        for i in range(1, y + 1):
            # If the tile has your opponent's icon
            if getFromGrid(x, y - i) == opponentIcon:
                FlipList.append(Pair(x, y - i))
                # print(str(y)+", "+str(i)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x, y - i) == icon:
                # print(str(y)+", "+str(i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(y)+", "+str(i)+" is blank")
                break
        
        FlipList = []
        
        # Check Down-Right
        
        distY = 8-y
        distX = 8-x
        
        minimumDistance = 0
        
        if distY < distX:
            minimumDistance = distY
        else:
            minimumDistance = distX
        
        
        for i in range(1, minimumDistance):
             # If the tile has your opponent's icon
            if getFromGrid(x + i, y + i) == opponentIcon:
                FlipList.append(Pair(x + i, y + i))
                # print(str(i + y)+", "+str(i + x)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x + i, y + i) == icon:
                # print(str(i + y)+", "+str(i + x)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(i + y)+", "+str(i + x)+" is blank")
                break
        
        FlipList = []
        
        
        # Up-right
        distY = y + 1
        distX = 8 - x
        if distY < distX:
            minimumDistance = distY
        else:
            minimumDistance = distX
        
        
        for i in range(1, minimumDistance):
             # If the tile has your opponent's icon
            if getFromGrid(x + i, y - i) == opponentIcon:
                FlipList.append(Pair(x + i, y - i))
                # print(str(i + y)+", "+str(x - i)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x + i, y - i) == icon:
                # print(str(i + y)+", "+str(x - i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(i + y)+", "+str(x - i)+" is blank")
                break
        
        FlipList = []
        
        # Up-Left
        distY = y + 1
        distX = x + 1
        if distY < distX:
            minimumDistance = distY
        else:
            minimumDistance = distX
        
        
        for i in range(1, minimumDistance):
             # If the tile has your opponent's icon
            if getFromGrid(x - i, y - i) == opponentIcon:
                FlipList.append(Pair(x - i, y - i))
                # print(str(y - i)+", "+str(x - i)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x - i, y - i) == icon:
                # print(str(y - i)+", "+str(x - i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(y - i)+", "+str(x - i)+" is blank")
                break
        
        FlipList = []
            
        
        # Down-left
        distY = 8 - y
        distX = x + 1
        if distY < distX:
            minimumDistance = distY
        else:
            minimumDistance = distX
        
        
        for i in range(1, minimumDistance):
             # If the tile has your opponent's icon
            if getFromGrid(x - i, y + i) == opponentIcon:
                FlipList.append(Pair(x - i, y + i))
                # print(str(y - i)+", "+str(x + i)+" is your opponent's icon")
            # If the tile has your own icon
            elif getFromGrid(x - i, y + i) == icon:
                # print(str(y - i)+", "+str(x + i)+" is your icon")
                # Flip the disks
                for j in FlipList:
                    addToGrid(j.x, j.y, icon)
                if len(FlipList) > 0:
                    validMove = True
                break
            else:
                # print(str(y - i)+", "+str(x + i)+" is blank")
                break
        
        FlipList = []
    else:
        print("Occupied Space")
        return False
    #Break out of the loop if the input is valid
    if validMove:
        return True
    else:
        print("\033[4m\nInvalid Move\033[0m")
        print("Possible Moves: ", checkAvailableMoves(icon, opponentIcon))
        return False
if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise


