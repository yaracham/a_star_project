from state import *
from utils import *
from algorithms import *
from tkinter import Tk, Button
from tkinter.font import Font

level = 1
first = "h"
start = time.time()


class GUI:
    def __init__(self):
        self.stats = SearchStats()
        self.game = State(nextPlayer=human_player)
        self.app = Tk()
        self.app.title('Tic Tac Toe')
        self.app.resizable(width=False, height=False)
        self.font = Font(family="Helvetica", size=32)
        self.buttons = {}

        for x, y in self.game.table:
            handler = lambda x=x, y=y: self.move(x, y)
            button = Button(self.app, command=handler, font=self.font, width=2, height=1)
            button.grid(row=x, column=y)
            self.buttons[x, y] = button

        handler = lambda: self.reset()
        button = Button(self.app, text='Reset', command=handler)
        button.grid(row=size + 1, column=0, columnspan=size, sticky='WE')

        """
        Code for selecting the levels
        """
        buttonE = Button(self.app, text='Easy', command=lambda: self.selectdifficulty(1))
        buttonE.grid(row=size + 2, column=0, columnspan=size, sticky='WE')
        buttonM = Button(self.app, text='Medium', command=lambda: self.selectdifficulty(2))
        buttonM.grid(row=size + 3, column=0, columnspan=size, sticky='WE')
        buttonH = Button(self.app, text='Hard', command=lambda: self.selectdifficulty(3))
        buttonH.grid(row=size + 4, column=0, columnspan=size, sticky='WE')
        self.update()
        if first == "c":
            self.game.nextPlayer = computer_player
            self.computer_move()

    def selectdifficulty(self, value):
        global level
        level = value
        self.reset()

    def reset(self):
        self.stats.reset()  # Reset stats on game reset
        self.game = State(nextPlayer=human_player)
        self.update()
        self.app.destroy()
        Select().mainloop()

    def move(self, x, y):
        global level
        self.app.config(cursor="watch")
        self.app.update()
        self.game.table[x, y] = human_player
        self.game.nextPlayer = computer_player
        self.update()
        if TERMINAL_TEST(self.game):
            return
        self.computer_move()

    def computer_move(self):
        if level == 3:
            self.game.depth = 0
            self.stats.maxDepth = 15
            self.game = ALPHA_BETA_SEARCH(self.game, time.time(), self.stats)
            self.stats.print()
            self.stats.reset() 
        elif level == 2:
            self.stats.maxDepth = 10
            self.game = ALPHA_BETA_SEARCH(self.game, time.time(), self.stats)
            self.stats.print()
            self.stats.reset()
        elif level == 1:
            self.game = ALPHA_BETA_SEARCH(self.game,time.time(),self.stats)
            self.stats.maxDepth = 5
            self.stats.print()
            self.stats.reset()
        self.update()
        self.app.config(cursor="")

    def update(self):
        for (x, y) in self.game.table:
            text = self.game.table[x, y]
            self.buttons[x, y]['text'] = text
            self.buttons[x, y]['disabledforeground'] = 'green'
            if text == empty:
                self.buttons[x, y]['state'] = 'normal'
            else:
                self.buttons[x, y]['state'] = 'disabled'
        winning = TERMINAL_TEST(self.game)
        if winning:
            winner = self.game.won(player=other_player(self.game.nextPlayer))
            if winner:
                for x, y in winner:
                    self.buttons[x, y]['disabledforeground'] = 'red'
            for x, y in self.buttons:
                self.buttons[x, y]['state'] = 'disabled'
        for (x, y) in self.game.table:
            self.buttons[x, y].update()

    def mainloop(self):
        self.app.mainloop()


class SearchStats:
    def __init__(self):
        self.cutOffOccured = False
        self.maxDepthReached = 0
        self.totalNodes = 0
        self.pruningMax = 0
        self.pruningMin = 0
        self.maxDepth = 5

    def reset(self):
        self.cutOffOccured = False
        self.maxDepthReached = 0
        self.totalNodes = 0
        self.pruningMax = 0
        self.pruningMin = 0
        self.maxDepth = 5

    def print(self):
        print("-----------------------")
        print("Statistics of the Move")
        print(f"Cutoff Occured: {self.cutOffOccured}")
        print(f"Maximum Depth Reached: {self.maxDepthReached}")
        print(f"Total number of nodes generated: {self.totalNodes}")
        print(f"Number of times pruning occured within Max-Value: {self.pruningMax}")
        print(f"Number of times pruning occured within Min-Value: {self.pruningMin}")


class Select:
    def __init__(self):
        self.app = Tk()
        self.app.title('Select Who Goes First')
        self.app.geometry("400x100")
        self.font = Font(family="Helvetica", size=32)

        computer_handle = lambda: self.choose("c")
        human_handle = lambda: self.choose("h")
        b1 = Button(self.app, text='Computer', command=computer_handle)
        b1.grid(row=0, column=0, columnspan=20, sticky='WE')

        b2 = Button(self.app, text='Human', command=human_handle)
        b2.grid(row=1, column=0, columnspan=20, sticky='WE')

    def choose(self, option):
        global first
        first = option
        self.app.destroy()
        GUI().mainloop()

    def mainloop(self):
        self.app.mainloop()