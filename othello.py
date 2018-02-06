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
        "\n1","| ","| ","| ","| ","| ","| ","| ","| ","|",
        "\n2","| ","| ","| ","| ","| ","| ","| ","| ","|",
        "\n3","| ","| ","| ","| ","| ","| ","| ","| ","|",
        "\n4","| ","| ","| ","| ","| ","| ","| ","| ","|",
        "\n5","| ","| ","| ","| ","| ","| ","| ","| ","|",
        "\n6","| ","| ","| ","| ","| ","| ","| ","| ","|",
        "\n7","| ","| ","| ","| ","| ","| ","| ","| ","|",
        "\n8","| ","| ","| ","| ","| ","| ","| ","| ","|","\033[0m"]

#prints gameboard grid
def printGrid():
    print(*grid, sep = '')

grid[35] = "|B"
grid[36] = "|W"
grid[45] = "|W"
grid[46] = "|B"


def addToGrid(rows, columns, icon):    
    grid[10*(rows-1)+columns+1] = "|" + str(icon)

def getFromGrid(rows, columns):
    position = 10*(rows-1) + columns+1
    
    gridElement = grid[position]
    
    if (position % 10 == 0):
        return gridElement[3]
    else:
        return gridElement[1]
    
def checkAvailableMoves(icon, opponentIcon):
    
    possibleMoves = 0

    # Loop through entire grid
    for x in range(1, 9):
        for y in range(1, 9):
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
                for i in reversed(range(1, x)):
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
                    #print(y,x)
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
            print("")
            printGrid()
            print("\033[4m\n",player,"Turn\033[0m")
            
            # Get player input
            newLocation = input("Location as x,y:\n\t:")
            
            if newLocation == "quit":
                sys.exit()
            
            x = int(newLocation[2])
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
                for i in reversed(range(1, x)):
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
                print("\033[4m\nInvalid Move\033[0m")
                print("Possible Moves: ", checkAvailableMoves(icon, opponentIcon))
        except SystemExit:
            print("Goodbye")
            sys.exit()
        except:
            print("\033[4m\nInvalid Input\033[0m")

    
    addToGrid(x, y, icon)
    
    
# Main Game Loop
    
print("\033[4m\nOTHELLO\033[0m")
print("")
print("Goal: The winner is the player who has more discs of his colour than his ",
      "opponent at the end of the game. ",
      "This will happen when neither of the two players has a legal move. ")
print("")
print("Rules: Black always moves first.\n", 
      "A move is made by placing a disc of the player's color on the board in a position that ",
      "out-flanks one or more of the opponent's discs.\n",
      "A disc or row of discs is outflanked when it is surrounded at the ends by discs of the opposite color.\n",
      "A disc may outflank any number of discs in one or more rows in any direction ",
      "(horizontal, vertical, diagonal). \n",
      "All the discs which are outflanked will be flipped, even if it is to the player's advantage not to flip ",
      "them.\n",
      "Discs may only be outflanked as a direct result of a move and must fall in the direct line of the ",
      "disc being played. \n",
      "If you can't outflank and flip at least one opposing disc, you must pass your turn. \n",
      "However, if a move is available to you, you can't forfeit your turn. ")
print("")
print("Input: Location to place a piece on your turn is input as 'x,y'.\n", 
      "If you wish to exit the game early input 'quit'")



while True:
    numberPassed = 0
    whiteScore = 0
    blackScore = 0
    
    if (checkAvailableMoves("B", "W")):
        takeTurn("Black")
        numberPassed = 0
    else:
        print("Black Turn Forfeited")
        numberPassed += 1
        if numberPassed == 2:
            print("\nGame Over")
            print("")
            
            for x in range(1, 9):
                for y in range(1, 9):
                    if getFromGrid(x, y) == "W":
                        whiteScore += 1
                    elif getFromGrid(x, y) == "B":
                        blackScore += 1
            
            if blackScore > whiteScore:
                print("\033[4m\nBlack Wins!\n\033[0m")
            elif whiteScore > blackScore:
                print("\033[4m\nWhite Wins!\n\033[0m")
            else:
                print("\033[4m\nTie\033[0m")
                
            print(blackScore, ":", whiteScore)
            print("")
            printGrid()
            break
    if (checkAvailableMoves("W", "B")):
        takeTurn("White")
        numberPassed = 0
    else:
        print("White Turn Forfeited")
        numberPassed += 1
        if numberPassed == 2:
            print("\nGame Over")
            print("")
            
            for x in range(1, 9):
                for y in range(1, 9):
                    if getFromGrid(x, y) == "W":
                        whiteScore += 1
                    elif getFromGrid(x, y) == "B":
                        blackScore += 1
            
            if blackScore > whiteScore:
                print("\033[4m\nBlack Wins!\n\033[0m")
            elif whiteScore > blackScore:
                print("\033[4m\nWhite Wins!\n\033[0m")
            else:
                print("\033[4m\nTie\033[0m")
                
            print(blackScore, ":", whiteScore)
            print("")
            printGrid()
            break
    
