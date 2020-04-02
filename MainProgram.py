# This is initial comment to start the project.
from tkinter import *
from tkinter import font
from tkinter import messagebox
import numpy as np

class Maze:
    '''Maze class to create and solve Maze by DFS.'''
    
    def __init__(self, maze):
        ''' constructor of class '''
        self.rows = self.columns = 51  # Max size 
        self.array = np.array([0] * (self.rows*self.columns))
        self.rowsVar = StringVar()
        self.rowsVar.set(25)    # Default
        self.colsVar = StringVar()
        self.colsVar.set(25)    # Default
        self.countBox = Spinbox(app, width=3, from_=5, to=51, textvariable=self.rowsVar, validate='focus', font=('Roboto',13), bd=2)      
        self.countBox.place(relx=.9, rely=.15, anchor=CENTER)
        
        
if __name__ == '__main__':
    app = Tk()
    app.title("Maze Solver using DFS")
    app.attributes('-fullscreen',True)
    exitButton = Button(app, text='Exit', command = app.destroy, bd = 0, font = ('arial', 15, 'bold'), fg = 'red').place(relx = .94, rely = .03)
    count = Label(app, text = 'Select rows & columns count (5 to 51 odd values ONLY) => ', font = ('arial', 14))
    count.place(relx = .55, rely = .15,anchor = W)
    Maze(app)
    app.mainloop()