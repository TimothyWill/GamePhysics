# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 14:32:32 2018

@author: Student
"""

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
print(*grid, sep = '')

grid[32] = "|B"
grid[33] = "|W"
grid[41] = "|W"
grid[42] = "|B"

rows = int(8)
columns = int(6)

print(*grid, sep = '')

grid[9*(rows-1)+columns+1] = "|B"
print(*grid, sep = '')