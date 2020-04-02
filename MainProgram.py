# This is initial comment to start the project.
from tkinter import *
from tkinter import font
from tkinter import messagebox
import numpy as np
from functools import partial
from random import shuffle, randrange

class Maze:
    '''Maze class to create and solve Maze by DFS '''
    class Cell(object):
        ''' Class which represents cell of the grid '''
        def __init__(self, row, col):
            self.row = row
            self.col = col
        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self.row == other.row and self.col == other.col
            else:
                return False
    
    # Constants:
    Empty = 0
    Obstacle = 1
    Start = 2
    Target = 3

    def __init__(self, maze):
        ''' constructor of class '''
        self.rows = self.columns = 51  # Max size 
        self.solveMaze = False
        self.found = False
        self.searching = False
        self.endOfSearch = False
        self.grid = [[]]    # Empty grid

        self.array = np.array([0] * (self.rows*self.columns))
        self.rowsVar = StringVar()
        self.rowsVar.set(25)    # Default
        self.colsVar = StringVar()
        self.colsVar.set(25)    # Default
        self.countBox = Spinbox(app, width=3, from_=5, to=51, textvariable=self.rowsVar, validate='focus', font=('Roboto',13), bd=2)      
        self.countBox.place(relx=.9, rely=.15, anchor=CENTER)
        
        self.message = Label(app, text="Click 'Create a Maze' and then 'Solve the Maze'", width = 55, font = ('Helvetica', 15), fg="BLUE")
        self.message.place(relx=.54, rely=.21, anchor='w')

        self.buttons = list()
        for i, action in enumerate(("New grid", "Create a Maze", "Clear", "Solve the Maze")):
            button = Button(app, text=action, width=21, font = ('Roboto', 12, 'bold'), bd = 3, bg = 'darkblue', fg = 'white',
                        command = partial(self.actions, action))
            button.place(x=920 if i%2==0 else 1140, y=230+45*int(i/2))
            self.buttons.append(button)

        self.canvas = Canvas(app, bd=0, highlightthickness = 0)
        self.initializeMaze(False)
    
    def actions(self, action):
        if action == "New grid":
            self.newGrid()
        elif action == "Create a Maze":
            self.createMaze()
        elif action == "Clear":
            self.clearMaze()
        elif action == "Solve the Maze":
            self.mazeSolver()

    def newGrid(self):
        self.solveMaze = False
        self.buttons[3].configure(fg = "WHITE")
        self.initializeMaze(False)
    
    def createMaze(self):
        self.solveMaze = False
        self.buttons[3].configure(fg = "WHITE")
        self.initializeMaze(True)

    def clearMaze(self):
        self.solveMaze = False
        self.buttons[3].configure(fg = "WHITE")

    def mazeSolver(self):
        self.solveMaze = True
        self.searching = True
        self.buttons[3].configure(fg="YELLOW")
        
    def initializeMaze(self, flag):
        self.rows = self.columns = int(self.countBox.get())
        if (flag and self.rows%2!=1):   # Grid won't have any path for Even no.s. Thus making count to odd
            self.columns = self.rows = self.rows - 1
            self.rowsVar.set(self.rows)
            self.colsVar.set(self.colsVar)
        
        self.grid = self.array[:self.rows*self.columns]
        self.grid = self.grid.reshape(self.rows, self.columns)

        self.squareSize = int(800/(self.rows))

        # background design
        self.width = self.height = self.columns * self.squareSize + 1
        self.canvas.configure(width = self.width, height = self.height)
        self.canvas.place(relx=0.28, rely=0.5, anchor=CENTER)
        self.canvas.create_rectangle(0, 0, self.width, self.height, width = 0, fill = "DARK GREY")

        for r in range(self.rows):
            for c in list(range(self.columns)):
                self.grid[r][c] = self.Empty

        self.startPos = self.Cell(self.rows-2, 1)
        self.targetPos = self.Cell(1, self.columns-2)

        if flag:
            maze = self.mazeCreator(int(self.rows/2))
            for r in range(self.rows):
                for c in range(self.columns):
                    if maze[r*self.columns+c : r*self.columns+c+1] in "|-+":
                        self.grid[r][c] = self.Obstacle

    @staticmethod
    def mazeCreator(width):
        ''' creates a random maze using recursive backtracking algorithm. Returns maze as a string '''
        height = width
        vis = [[0] * width + [1] for _ in range(height)] + [[1] * (width + 1)]
        ver = [["| "] * width + ['|'] for _ in range(height)] + [[]]
        hor = [["+-"] * width + ['+'] for _ in range(height + 1)]

        def walk(x, y):
            vis[y][x] = 1

            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]:
                    continue
                if xx == x:
                    hor[max(y, yy)][x] = "+ "
                if yy == y:
                    ver[y][max(x, xx)] = "  "
                walk(xx, yy)
        walk(randrange(width), randrange(height))

        s = ""
        for (a, b) in zip(hor, ver):
            s += ''.join(a + b)
        return s
        

if __name__ == '__main__':
    app = Tk()
    app.title("Maze Solver using DFS")
    app.attributes('-fullscreen',True)
    exitButton = Button(app, text='Exit', command = app.destroy, bd = 0, font = ('arial', 15, 'bold'), fg = 'red').place(relx = .94, rely = .03)
    count = Label(app, text = 'Select rows & columns count (5 to 51 odd values ONLY) => ', font = ('arial', 14))
    count.place(relx = .55, rely = .15,anchor = W)
    Maze(app)
    app.mainloop()