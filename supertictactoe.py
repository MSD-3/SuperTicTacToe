import numpy as np
import os

#initialising unplayed spots as zeros
b_grid = np.zeros((3, 3), dtype=int)
s_grid = np.zeros((9, 3, 3), dtype=int)

# Plyer1 is 1, Player2 is 2
turn = 1
empty = 0

#First User can play anywhere on board so initialised i,j with -1
i, j = -1, -1
i_small, j_small = 0, 0

def gridUncaptured(i, j):       #checks if b_grid square is uncaptured or not
    return b_grid[i][j] == 0

def subGridUncaptured(k, i, j): #checks if sub grid square is uncaptured or not
    return s_grid[k][i][j] == 0

def checkWinSmall(k):       #checks win in subgrid
    board = s_grid[k]
    
    #Row check
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != 0:
            return True

    #Column check
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != 0:
            return True

    #Diagonal check
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        return True

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
        return True
    
    return False

#game win check
def checkWin():
    #row check
    for row in b_grid:
        if row[0] == row[1] == row[2] and row[0] != 0:
            return True

    #column check
    for col in range(3):
        if b_grid[0][col] == b_grid[1][col] == b_grid[2][col] and b_grid[0][col] != 0:
            return True

    #diagonal check
    if b_grid[0][0] == b_grid[1][1] == b_grid[2][2] and b_grid[0][0] != 0:
        return True

    if b_grid[0][2] == b_grid[1][1] == b_grid[2][0] and b_grid[0][2] != 0:
        return True

    return False

def print_grid():    # Function to print the current state of the grid
    os.system('cls' if os.name == 'nt' else 'clear')
    symbols = [' ', 'X', 'O']  # Mapping for empty, player1, player2

    def print_small_grid(grid):
        lines = []
        for row in grid:
            line = ' | '.join(symbols[cell] for cell in row)
            lines.append(line)
        return '\n'.join(lines)

    def print_row_of_grids(grids):
        rows = ['', '', '']
        for grid in grids:
            small_grid = print_small_grid(grid).split('\n')
            for i in range(3):
                rows[i] += '| ' + small_grid[i] + ' |'
        return '\n'.join(rows)

    def print_b_grid():
        lines = []
        for row in b_grid:
            line = ' || '.join(symbols[cell] for cell in row)
            lines.append(line)
            lines.append('============')
        return '\n'.join(lines)

    large_grid = [[], [], []]
    for k in range(9):
        large_grid[k // 3].append(s_grid[k])

    print('Grids:')
    print('======================================')
    print(print_row_of_grids(large_grid[0]))
    print('======================================')
    print(print_row_of_grids(large_grid[1]))
    print('======================================')
    print(print_row_of_grids(large_grid[2]))
    print('======================================')
    print()
    print()
    print('Super Grid Overview:')
    print('============')
    print(print_b_grid())
    print()

#main game loop
while True:
    print_grid()
    print(f"\n\nTurn of Player {turn}\n")
    
    #if last move was on a captured tile then choose any tile
    if (i == -1 and j == -1) or not gridUncaptured(i, j):
        while True:
            print("Choose a tile on the Super grid:")
            i = int(input("Enter row (1,2,3): ")) - 1
            j = int(input("Enter column (1,2,3): ")) - 1
            if 0 <= i <= 2 and 0 <= j <= 2:  # Check for out-of-bounds
                if gridUncaptured(i, j):
                    break
                else:
                    print("Tile already won, try again")
            else:
                print("Invalid Input! Try again")
    
    while True:  #input in s_grid
        print(f"Choose a move in in chosen grid: {i+1},{j+1}")
        i_small = int(input("Enter row (1,2,3): ")) - 1
        j_small = int(input("Enter column (1,2,3): ")) - 1
        k = 3 * i + j
        
        if 0 <= i_small <= 2 and 0 <= j_small <= 2:  # Check for out-of-bounds
            if subGridUncaptured(k, i_small, j_small):
                break
            else:
                print("\nTile already filled, try again\n")
        else:
            print("\nInvalid Input! Try again\n")

    s_grid[k][i_small][j_small] = turn
    
    #check if the small grid is won
    if checkWinSmall(k):
        b_grid[i][j] = turn
    
    #check if the entire board is won
    if checkWin():
        print_grid()
        print(f"Player {turn} won!")
        break

    
    if turn==1:
        turn=2
    else:
        turn=1
    
    # Set the next target small grid based on the last move
    i, j = i_small, j_small
