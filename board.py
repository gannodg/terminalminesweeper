import numpy as nm
import random as random

class Board:

    # M is the minefield
    M = []
    # R is the revealed minefield
    R = []
    # G is the guessed minefield
    G = []
    # Size of the minefield
    size = 0
    # Bomb squad count
    bombs_left = 0
    # Bombs marked
    bombs_marked = 0
    # Bombs guessed
    bombs_guessed = 0

    def __init__(self, gridSize):
        super().__init__()
        self.size = gridSize
        numBombs = nm.math.floor(self.size * 0.15)
        self.M = [[0 for x in range(self.size)] for y in range(self.size)]
        self.R = [[0 for x in range(self.size)] for y in range(self.size)]
        self.G = [[0 for x in range(self.size)] for y in range(self.size)]
        # Initialize the minefield
        for i in range(0, self.size):
            for j in range(0, self.size):
                rval = random.uniform(0.0, 1.0)
                self.R[i][j] = False
                self.G[i][j] = False
                # 15% bombs
                if (rval <= 0.15):
                    self.M[i][j] = 9
                    self.bombs_left = self.bombs_left + 1
                    self.bombs_marked = self.bombs_marked + 1
        self.neighbors()

    def neighbors(self):
        # compute the neighborhood values for each location
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.M[i][j] != 9:
                    for x in range(i - 1, i + 2):
                        for y in range(j - 1, j + 2):
                            if (x in range(0, self.size)) and (y in range(0, self.size)) and (self.M[x][y] == 9):
                                self.M[i][j] = self.M[i][j] + 1

    def visited(self, x, y):
        result = True
        if (x < 0 or x == self.size) or (y < 0 or y == self.size):
            return True
        if self.R[x][y] == False:
            self.R[x][y] = True
            if self.M[x][y] == 0:
                # Iterate through the neighborhood and 
                # recursively visit the adjacent locations
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        self.visited(i, j)
            if self.M[x][y] == 9:
                result = False
        return result

    def mark_bomb(self, x, y):
        result = True
        if not self.G[x][y]:
            self.G[x][y] = True
            self.R[x][y] = True
            self.bombs_marked = self.bombs_marked - 1
            if self.M[x][y] == 9:
                self.bombs_left = self.bombs_left - 1
            self.bombs_guessed = self.bombs_guessed + 1
        else:
            self.G[x][y] = False
            self.R[x][y] = False
            self.bombs_marked = self.bombs_marked + 1
            if self.M[x][y] == 9:
                self.bombs_left = self.bombs_left + 1
            self.bombs_guessed = self.bombs_guessed - 1
            result = False
        return result

    def score(self):
        score = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.M[i][j] == 9 and self.G[i][j] == True:
                    score = score + 1
        return score
       
