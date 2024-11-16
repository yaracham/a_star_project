from copy import deepcopy
import sys

x_player = 'X'
o_player = 'O'
empty = ' '
size = 4

class State:
    def __init__(self, nextPlayer, other=None):
        self.nextPlayer = nextPlayer
        self.table = {}
        self.depth = 0
        self.utility = 0
        self.value = 0
        self.children = {}

        for y in range(size):
            for x in range(size):
                self.table[x, y] = empty

        if other:
            self.__dict__ = deepcopy(other.__dict__)

    def printBoard(self):
        for i in range(0, size):
            for j in range(0, size):
                if self.table[i, j] == empty:
                    sys.stdout.write(' _ ')
                elif self.table[i, j] == x_player:
                    sys.stdout.write(' X ')
                else:
                    sys.stdout.write(' O ')
            print("")

    def is_full(self):
        for i in range(0, size):
            for j in range(0, size):
                if self.table[i, j] == empty:
                    return False

        return True

    def won(self, player):
        # horizontal
        for x in range(size):
            winning = []
            for y in range(size):
                if self.table[x, y] == player:
                    winning.append((x, y))
            if len(winning) == size:
                return winning

        # vertical
        for y in range(size):
            winning = []
            for x in range(size):
                if self.table[x, y] == player:
                    winning.append((x, y))
            if len(winning) == size:
                return winning

        # diagonal \
        winning = []
        for y in range(size):
            x = y
            if self.table[x, y] == player:
                winning.append((x, y))
        if len(winning) == size:
            return winning

        # diagonal /
        winning = []
        for y in range(size):
            x = size - 1 - y
            if self.table[x, y] == player:
                winning.append((x, y))
        if len(winning) == size:
            return winning

        # default
        return None