from tkinter import *
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
    
    class Point(object):
        ''' Class which represents point on the grid '''
        def __init__(self, x, y):
            self.X = x
            self.Y = y
        def getX(self):
            return self.X
        def getY(self):
            return self.Y

    # Constants:
    Empty = 0
    Obstacle = 1
    Start = 2
    Target = 3
    Frontier = 4
    Explored = 5
    Route = 6
    Counter = 0

    def __init__(self, maze):
        ''' constructor of class '''
        self.rows = self.columns = 51  # Max size 
        self.squareSize = 0
        self.solveMaze = False
        self.found = False
        self.searching = False
        self.endOfSearch = False
        self.grid = [[]]    # Empty grid
        self.startPos = self.Cell(self.rows-2, 1)
        self.targetPos = self.Cell(1, self.columns-2)
        self.openList = []
        self.closedList = []
        self.centers = [[self.Point(0, 0) for c in range(self.rows)] for r in range(self.rows)]  # the centers of the cells

        self.array = np.array([0] * (self.rows*self.columns))
        self.rowsVar = StringVar()
        self.rowsVar.set(25)    # Default
        self.colsVar = StringVar()
        self.colsVar.set(25)    # Default
        self.countBox = Spinbox(app, width=3, from_=5, to=51, textvariable=self.rowsVar, validate='focus', font=('Roboto',13), bd=2)      
        self.countBox.place(relx=.93, rely=.15, anchor=CENTER)
        
        self.message = Label(app, text="Click 'Create a Maze' and then 'Solve the Maze'", width = 55, font = ('Helvetica', 15), fg="BLUE")
        self.message.place(relx=.57, rely=.21, anchor='w')

        self.buttons = list()
        for i, action in enumerate(("New grid", "Create a Maze", "Clear", "Solve the Maze")):
            button = Button(app, text=action, width=21, font = ('Roboto', 12, 'bold'), bd = 3, bg = 'darkblue', fg = 'white',
                        command = partial(self.actions, action))
            button.place(relx=0.635 if i%2==0 else 0.775, rely=0.25+0.05*int(i/2))
            self.buttons.append(button)
        
        self.buttons[1].config(state=DISABLED)
        self.buttons[2].config(state=DISABLED)
        self.buttons[3].config(state=DISABLED)

        self.shapeFrame = LabelFrame(app, text="  Notations  ", width=555, height=200, fg='Black', font=('Roboto',14, 'bold'), bd=3).place(relx=0.585, rely=0.395)
        memo_colors = ("RED", "GREEN", "BLUE", "CYAN")
        for i, memo in enumerate(("Start : Starting position from which DFS search starts", 
                        "Target : Target position for DFS", 
                        "Frontier : All Unexplored siblings upto last step", 
                        "Explored nodes : Path from which Target is unreachable")):
            label = Label(app, text=memo,  width=46, anchor='w', fg=memo_colors[i], font=("Helvetica", 14))
            label.place(relx = 0.6, rely = 0.435+(0.045*i))
        
        self.explFrame = LabelFrame(app, text="  Maze Path Exploration Priority  ", width=555, height=80, fg='Black', font=('Roboto',14, 'bold'), bd=3).place(relx=0.585, rely=0.655)
        Label(app, text="1. Up (↑)\t\t2. Right (→)\t3.Down (↓)\t4. Left (←)", font=("Helvetica", 13)).place(relx = 0.6, rely = 0.7)
        self.canvas = Canvas(app, bd=0, highlightthickness = 0)
    
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
        self.buttons[1].config(state=NORMAL)
        self.buttons[3].config(state=NORMAL)
        self.buttons[3].configure(fg = "WHITE")
        self.initializeGrid(False)
    
    def createMaze(self):
        self.solveMaze = False
        self.buttons[3].configure(fg = "WHITE")
        self.buttons[2].config(state=NORMAL)
        self.Counter = 1
        self.initializeGrid(True)

    def clearMaze(self):
        self.solveMaze = False
        self.buttons[3].configure(fg = "WHITE")
        self.Counter = self.Counter - 1
        if self.Counter == 0:
            self.buttons[2].config(state=DISABLED)
        self.gridCreator()
        
    def initializeGrid(self, flag):
        self.rows = self.columns = int(self.countBox.get())
        if flag and (self.rows % 2 != 1):   # Grid won't have any path for Even no.s. Thus making count to odd
            self.rows = self.rows - 1
            self.columns = self.rows
            self.rowsVar.set(self.rows)
            self.colsVar.set(self.columns)
        
        self.grid = self.array[:self.rows*self.columns]
        self.grid = self.grid.reshape(self.rows, self.columns)

        self.squareSize = int(800/self.rows)

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

        # Calculation of the coordinates of the cells' centers
        for r in range(self.rows):
            for c in range(self.columns):
                self.centers[r][c] = self.Point(c*self.squareSize + self.squareSize/2,
                                                    r*self.squareSize + self.squareSize/2)
        self.gridCreator()
        if flag:
            maze = self.mazeCreator(int(self.rows/2))
            for r in range(self.rows):
                for c in range(self.columns):
                    if maze[r*self.columns+c : r*self.columns+c+1] in "|-+":
                        self.grid[r][c] = self.Obstacle
        self.paintCells()

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

    def gridCreator(self):
        '''Initialized all cells in grid. Resets all cells to previous state'''
        if self.searching or self.endOfSearch:
            for r in range(self.rows):
                for c in range(self.columns):
                    if self.grid[r][c] in [self.Frontier, self.Explored, self.Route]:
                        self.grid[r][c] = self.Empty
                    if self.grid[r][c] == self.Start:
                        self.startPos = self.Cell(r, c)
            self.searching = False
        else:
            for r in range(self.rows):
                for c in range(self.columns):
                    self.grid[r][c] = self.Empty
            self.startPos = self.Cell(self.rows-2, 1)
            self.targetPos = self.Cell(1, self.columns-2)

        self.found = False
        self.searching = False
        self.endOfSearch = False
        self.openList.clear()
        self.closedList.clear()
        self.openList = [self.startPos]
        self.closedList = []
        self.grid[self.targetPos.row][self.targetPos.col] = self.Target
        self.grid[self.startPos.row][self.startPos.col] = self.Start

        self.paintCells()
    
    def paintCells(self):
        ''' Paints cells according to their properties '''
        color = ""
        for r in range(self.rows):
            for c in range(self.columns):
                if self.grid[r][c] == self.Empty:
                    color = "WHITE"
                elif self.grid[r][c] == self.Start:
                    color = "RED"
                elif self.grid[r][c] == self.Target:
                    color = "GREEN"
                elif self.grid[r][c] == self.Obstacle:
                    color = "BLACK"
                elif self.grid[r][c] == self.Frontier:
                    color = "BLUE"
                elif self.grid[r][c] == self.Explored:
                    color = "CYAN"
                elif self.grid[r][c] == self.Route:
                    color = "YELLOW"
                self.canvas.create_polygon(self.calculateSquare(r,c), width=0, fill=color)

    def calculateSquare(self, r, c):
        '''Calculate co-ordinates of vertices of the square corresponding to particular cell'''
        polygon = []
        polygon.extend((    c*self.squareSize + 1,     r*self.squareSize + 1))
        polygon.extend(((c+1)*self.squareSize + 0,     r*self.squareSize + 1))
        polygon.extend(((c+1)*self.squareSize + 0, (r+1)*self.squareSize + 0))
        polygon.extend((    c*self.squareSize + 1, (r+1)*self.squareSize + 0))
        return polygon

    def mazeSolver(self):
        self.solveMaze = True
        self.searching = True
        self.buttons[2].config(state=NORMAL)
        self.buttons[3].configure(fg="YELLOW")
        self.Counter = 2

        while not self.endOfSearch:
            # if no element in openList, then no solution is present
            if(not self.openList):
                self.endOfSearch = True
                self.grid[self.startPos.row][self.startPos.col] = self.Start
                self.message.configure(app, text="No Path Found!", width = 55, font = ('Helvetica', 15), fg="BLUE")
                self.paintCells()
            else: # expand node:
                self.expandNodes()
                if self.found:
                    self.endOfSearch = True
                    self.plotRoute()

    def expandNodes(self):
        current = self.openList.pop(0)
        self.closedList.insert(0, current)
        self.grid[current.row][current.col] = self.Explored
        self.canvas.create_polygon(self.calculateSquare(current.row, current.col), width=0, fill="CYAN")

        if current == self.targetPos:
            last = self.targetPos
            last.prev = current.prev
            self.closedList.append(last)
            self.found = True
            return
                
        successors = self.createSuccessors(current, False)
        for cell in successors:
            self.openList.insert(0, cell)
            self.grid[cell.row][cell.col] = self.Frontier
            self.canvas.create_polygon(self.calculateSquare(cell.row, cell.col), width=0, fill="BLUE")

    def createSuccessors(self, current, flag):
        ''' Creates successors of a cell '''
        r = current.row
        c = current.col
        successors = []
        if(r>0 and self.grid[r-1][c] != self.Obstacle
            and (not self.Cell(r-1, c) in self.openList and not self.Cell(r-1, c) in self.closedList)):
            cell = self.Cell(r-1, c)
            cell.prev = current
            successors.append(cell)
        
        if (c < self.columns-1 and self.grid[r][c+1] != self.Obstacle and
                (not self.Cell(r, c+1) in self.openList and not self.Cell(r, c+1) in self.closedList)):
            cell = self.Cell(r, c+1)
            cell.prev = current
            successors.append(cell)
        
        if (r < self.rows-1 and self.grid[r+1][c] != self.Obstacle and
                ((not self.Cell(r+1, c) in self.openList and not self.Cell(r+1, c) in self.closedList))):
            cell = self.Cell(r+1, c)
            cell.prev = current
            successors.append(cell)
        
        if (c > 0 and self.grid[r][c-1] != self.Obstacle and
                (not self.Cell(r, c-1) in self.openList and not self.Cell(r, c-1) in self.closedList)):
            cell = self.Cell(r, c-1)
            cell.prev = current
            successors.append(cell)
        return reversed(successors)
    
    def plotRoute(self):
        '''Plot route from Start to Target'''
        self.paintCells()
        self.searching = False

        index = self.closedList.index(self.targetPos)
        cur = self.closedList[index]
        self.grid[cur.row][cur.col] = self.Target
        self.canvas.create_polygon(self.calculateSquare(cur.row, cur.col), width=0, fill="GREEN")
        while cur != self.startPos:
            cur = cur.prev
            self.grid[cur.row][cur.col] = self.Route
            self.canvas.create_polygon(self.calculateSquare(cur.row, cur.col), width=0, fill="YELLOW")

        self.grid[self.startPos.row][self.startPos.col] = self.Start
        self.canvas.create_polygon(self.calculateSquare(self.startPos.row, self.startPos.col), width=0, fill="RED")
            
if __name__ == '__main__':
    app = Tk()
    app.title("Maze Solver using DFS")
    app.attributes('-fullscreen',True)
    Button(app, text='Exit', command = app.destroy, bd = 0, font = ('arial', 17, 'bold'), fg = 'red').place(relx = .94, rely = .03)
    Label(app, text = 'Select rows & columns count (5 to 51 odd values ONLY) => ', font = ('arial', 14)).place(relx = .58, rely = .15, anchor = W)
    Label(app, text = "Click on \n\n'New Grid'\n\nto create empty grid", font = ('roboto', 28, 'bold'), fg='brown').place(relx = .25, rely = .50, anchor = CENTER)
    Maze(app)
    app.mainloop()