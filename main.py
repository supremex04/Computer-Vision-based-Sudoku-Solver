import numpy as np

board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

def printBoard(board):
    
    for i in range(len(board)):
        if (i%3) == 0 and i !=0:
            print("- - - - - - - - - - - - ")
        for j in range(len(board[0])):
            if (j%3) == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(str(board[i][j]) + " ")
            else:
                print(str(board[i][j]) + " ", end ="")

def solve(board):
    find =findEmpty(board)
    if not find:
        return True
    else:
        row, column = find
    for num in range(1,10):
        if validityCheck(board, (row, column), num):
            board[row][column] = num
            if solve(board):
                return True
            
            board[row][column] = 0
    return False




def findEmpty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i,j)
    return False

def validityCheck(board, position, guess):
    x, y = position
    #row check
    for i in range(len(board)):
        if board[x][i] == guess and x != i:
            pass
            return False
    #column check
    for i in range(len(board)):
        if board[i][y] == guess and  y != i:
            pass
            return False
    #box check
    boxX = x//3
    boxY = y//3
    matrix = np.matrix(board)
    subMatrix = matrix[boxX*3:(boxX*3)+3, boxY*3:(boxY*3)+3]
    conv = subMatrix.tolist()
    for i in range(3):
        for j in range(3):
            if conv[i][j] == guess and not(np.array_equal(np.array([x,y]), np.array([boxX*3+3, boxY*3+3]))):
                return False
    
    return True


print("ORIGINAL:")
printBoard(board)
solve(board)
print("                          ")
print("SOLVED:")
printBoard(board)