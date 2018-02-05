# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 14:47:36 2018

@author: Student
"""

import sys

# =============================================================
# Just testing to make sure I know how Pushing and Pulling work
# Three Cheers for GitHub!
# =============================================================

class Pair:
    def __init__(self, pX, pY):
        self.x = pX
        self.y = pY


#array for gameboard grid
#spaces 1,9,17,25,33,41,49,57 follow the format: "\n|[letter]"
#spaces 8,16,24,32,40,48,56,64 follow the format: "|[letter]|"
#all blank spaces follow the format: "|[blank space]"
grid = ["\033[4m  1 2 3 4 5 6 7 8 ",
        "\n1","| ","| ","| ","| ","| ","| ","| ","| |",
        "\n2","| ","| ","| ","| ","| ","| ","| ","| |",
        "\n3","| ","| ","| ","| ","| ","| ","| ","| |",
        "\n4","| ","| ","| ","| ","| ","| ","| ","| |",
        "\n5","| ","| ","| ","| ","| ","| ","| ","| |",
        "\n6","| ","| ","| ","| ","| ","| ","| ","| |",
        "\n7","| ","| ","| ","| ","| ","| ","| ","| |",
        "\n8","| ","| ","| ","| ","| ","| ","| ","| |",]

#prints gameboard grid
def printGrid():
    print(*grid, sep = '')

grid[32] = "|B"
grid[33] = "|W"
grid[41] = "|W"
grid[42] = "|B"


def addToGrid(rows, columns, icon):    
    grid[9*(rows-1)+columns+1] = "|" + str(icon)

def getFromGrid(rows, columns):
    position = 9*(rows-1) + columns+1
    
    gridElement = grid[position]
    
    if (position % 9 == 0):
        return gridElement[3]
    else:
        return gridElement[1]
    
def checkAvailableMoves(icon, opponentIcon):
    
    possibleMoves = 0

    # Loop through entire grid
    for x in range(1, 8):
        for y in range(1, 8):
            validMove = False
            
            if getFromGrid(x, y) == " ":
    
                # Check for Flipping
                
                # Check to the Right
                FlipList = []
                for i in range(y + 1, 8):
                    # If the tile has your opponent's icon
                    if getFromGrid(x, i) == opponentIcon:
                        FlipList.append(Pair(x, i))
                    # If the tile has your own icon
                    elif getFromGrid(x, i) == icon:
                        # Check valid move        
                        if len(FlipList) > 0:
                            validMove = True
                            break
                        else:
                            break
            
                # Check to the Left
                FlipList = []
                for i in reversed (range(0, y)):
                    # If the tile has your opponent's icon
                    if getFromGrid(x, i) == opponentIcon:
                        FlipList.append(Pair(x, i))
                    # If the tile has your own icon
                    elif getFromGrid(x, i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                            break
                        else:
                            break
         
                # Check Down
                FlipList = []
                for i in range(x + 1, 8):
                    # If the tile has your opponent's icon
                    if getFromGrid(i, y) == opponentIcon:
                        FlipList.append(Pair(i, y))
                    # If the tile has your own icon
                    elif getFromGrid(i, y) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                            break
                        else:
                            break
                
                # Check Up
                FlipList = []
                for i in reversed(range(0, x)):
                    # If the tile has your opponent's icon
                    if getFromGrid(i, y) == opponentIcon:
                        FlipList.append(Pair(i, y))
                    # If the tile has your own icon
                    elif getFromGrid(i, y) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                            break
                        else:
                            break
   
                # Check Up-Right             
                FlipList = []

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
                        FlipList.append(Pair(x + i, i + y))
                    # If the tile has your own icon
                    elif getFromGrid(x + i, y + i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                            break
                        else:
                            break

                # Check Up-Left               
                FlipList = []

                distY = 8-y
                distX = x
        
                if distY < distX:
                    minimumDistance = distY
                else:
                    minimumDistance = distX
                
                for i in range(1, minimumDistance):
                    # If the tile has your opponent's icon
                    if getFromGrid(x - i, y + i) == opponentIcon:
                        FlipList.append(Pair(x - i, i + y))
                    # If the tile has your own icon
                    elif getFromGrid(x - i, y + i) == icon:
                        #Check valid move
                        if len(FlipList) > 0:
                            validMove = True
                            break
                        else:
                            break
  
                # Check Down-Left              
                FlipList = []

                distY = y
                distX = x
                
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
    
                # Down-Right            
                FlipList = []
                    
                distY = y
                distX = 8 - x
                
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
                
                FlipList = []
                
                if validMove:
                    print(x, y)
                    possibleMoves += 1
    
    return possibleMoves

def takeTurn(player):
    
    icon = ' '
    
    if player == "Black":
        icon = 'B'
        opponentIcon = 'W'
    else:
        icon = 'W'
        opponentIcon = 'B'
    
    while True:
        try:
            printGrid()
            # Get player input
            newLocation = input("\n\nLocation as x, y:\n\t:")
            
            if newLocation == "quit":
                sys.exit()
            
            x = int(newLocation[3])
            y = int(newLocation[0])
            
            # print("X: " + str(x) + "Y: " + str(y))
            
            validMove = False
            
            if getFromGrid(x, y) == " ":
    
                # Check for Flipping
                
                # Check to the right
                FlipList = []
                for i in range(y + 1, 8):
                    # If the tile has your opponent's icon
                    if getFromGrid(x, i) == opponentIcon:
                        FlipList.append(Pair(x, i))
                        # print(str(i)+", "+str(x)+" is your opponent's icon")
                    # If the tile has your own icon
                    elif getFromGrid(x, i) == icon:
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
                for i in reversed (range(0, y)):
                    # If the tile has your opponent's icon
                    if getFromGrid(x, i) == opponentIcon:
                        FlipList.append(Pair(x, i))
                        # print(str(i)+", "+str(x)+" is your opponent's icon")
                    # If the tile has your own icon
                    elif getFromGrid(x, i) == icon:
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
                for i in range(x + 1, 8):
                    # If the tile has your opponent's icon
                    if getFromGrid(i, y) == opponentIcon:
                        FlipList.append(Pair(i, y))
                        # print(str(y)+", "+str(i)+" is your opponent's icon")
                    # If the tile has your own icon
                    elif getFromGrid(i, y) == icon:
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
                for i in reversed(range(0, x)):
                    # If the tile has your opponent's icon
                    if getFromGrid(i, y) == opponentIcon:
                        FlipList.append(Pair(i, y))
                        # print(str(y)+", "+str(i)+" is your opponent's icon")
                    # If the tile has your own icon
                    elif getFromGrid(i, y) == icon:
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
                
                # Check Up-Right
                
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
                        FlipList.append(Pair(x + i, i + y))
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
                
                
                # Up-Left
                distY = 8-y
                distX = x
                if distY < distX:
                    minimumDistance = distY
                else:
                    minimumDistance = distX
                
                
                for i in range(1, minimumDistance):
                     # If the tile has your opponent's icon
                    if getFromGrid(x - i, y + i) == opponentIcon:
                        FlipList.append(Pair(x - i, i + y))
                        # print(str(i + y)+", "+str(x - i)+" is your opponent's icon")
                    # If the tile has your own icon
                    elif getFromGrid(x - i, y + i) == icon:
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
                
                # Down-Left
                distY = y
                distX = x
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
                    
                
                # Down-Right
                distY = y
                distX = 8 - x
                if distY < distX:
                    minimumDistance = distY
                else:
                    minimumDistance = distX
                
                
                for i in range(1, minimumDistance):
                     # If the tile has your opponent's icon
                    if getFromGrid(x + i, y - i) == opponentIcon:
                        FlipList.append(Pair(x + i, y - i))
                        # print(str(y - i)+", "+str(x + i)+" is your opponent's icon")
                    # If the tile has your own icon
                    elif getFromGrid(x + i, y - i) == icon:
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
            #Break out of the loop if the input is valid
            if validMove:
                break
            else:
                print("Invalid Move")
                print("Possible Moves: ", checkAvailableMoves(icon, opponentIcon))
        except SystemExit:
            print("sys.exit() worked as expected")
            sys.exit()
        except:
            print("Invalid Input")

    
    addToGrid(x, y, icon)
    
    
# Main Game Loop
while True:
    takeTurn("Black")
    takeTurn("White")
    
