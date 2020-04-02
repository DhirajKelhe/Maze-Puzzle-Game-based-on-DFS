# This is initial comment to start the project.
from tkinter import *
from tkinter import font
from tkinter import messagebox
import numpy as np
from functools import partial

class Maze:
    '''Maze class to create and solve Maze by DFS.'''
    
    def __init__(self, maze):
        ''' constructor of class '''
        self.rows = self.columns = 51  # Max size 
        self.solveMaze = False
        self.found = False
        self.searching = False
        self.endOfSearch = False

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
        pass

if __name__ == '__main__':
    app = Tk()
    app.title("Maze Solver using DFS")
    app.attributes('-fullscreen',True)
    exitButton = Button(app, text='Exit', command = app.destroy, bd = 0, font = ('arial', 15, 'bold'), fg = 'red').place(relx = .94, rely = .03)
    count = Label(app, text = 'Select rows & columns count (5 to 51 odd values ONLY) => ', font = ('arial', 14))
    count.place(relx = .55, rely = .15,anchor = W)
    Maze(app)
    app.mainloop()