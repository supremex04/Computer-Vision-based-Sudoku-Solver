import tkinter as tk
import copy
from tkinter import font
from main import validityCheck, solve, printBoard


root = tk.Tk()
root.title("Sudoku Grid")
root.geometry("378x440")

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

genesis = copy.deepcopy(board)
genesisMark = []   #mark all the empty cells in genesis board

boldFont = font.Font(family="Helvetica", size=20, weight="bold")
def sodukoLoader(board, pos:list):
    if len(pos) == 0:
        for row in range(9):
            for col in range(9):
                if board[row][col] !=0:
                    canvases[row][col].create_text(20, 25, text=str(board[row][col]),fill = "#a44648", font=boldFont, justify = "center")
                else:
                    genesisMark.append((row,col))
    else:
        for row in range(9):
            for col in range(9):
                if (row,col) in pos:
                    canvases[row][col].create_text(20, 25, text=str(board[row][col]),fill = "black", font=("Helvetica", 20), justify = "center")


def cell_clicked(event):
    #Get the clicked canvas
    clicked_canvas = event.widget

    #Deselect all cells
    for row in range(9):
        for col in range(9):
            boxX = row//3
            boxY = col//3
            if (boxX+boxY)%2 ==0:
                canvases[row][col].config(relief = "solid", bg="white", cursor ="hand2")
            else:
                canvases[row][col].config(relief = "solid", bg="#fffec8", cursor ="hand2")


    #Highlight the clicked cell
    clicked_canvas.config(relief = "groove", bg="lightblue",cursor = "hand2")

def key_pressed(event):
    #Get the pressed key
    pressed_key = event.char
    if pressed_key.isdigit():
        num = int(pressed_key)
        #Find the highlighted cell
        for row in range(9):
            for col in range(9):
                if canvases[row][col]["bg"] == "lightblue":
                    # Add the pressed key to the cell
                    if validityCheck(board,(row,col), num) == True and board[row][col]==0:
                        canvases[row][col].create_text(20, 25, text=pressed_key, font=("Helvetica", 20), justify = "center")
                        board[row][col] = num
                        return


def solver():
    solve(genesis)
    print("                          ")
    print("SOLVED:")
    printBoard(genesis)
    sodukoLoader(genesis, genesisMark)


canvases = []

for i in range(9):
    canvas_row = []
    for j in range(9):
        boxX = i//3
        boxY = j//3
        if (boxX+boxY)%2 ==0:
            canvas = tk.Canvas(root, width=40, height=40,bg="white", highlightthickness=0, borderwidth=1, relief="solid")
        else:
            canvas = tk.Canvas(root, width=40, height=40,bg="#fffec8", highlightthickness=0, borderwidth=1, relief="solid")
        canvas.grid(row=i, column=j)
        canvas.bind("<Button-1>", cell_clicked)
        canvas_row.append(canvas)
    canvases.append(canvas_row)

sodukoLoader(board, genesisMark)

infoCanvas = tk.Canvas(root,  bg = "#ffdab9", borderwidth=0)
canvases.append(infoCanvas)
infoCanvas.place(x=0,y = 377)


solveButton = tk.Button(root, text = "Solve!", command=solver)
solveButton.place(x =320, y= 400)

#Bind keyboard events
root.bind("<Key>", key_pressed)
root.mainloop()