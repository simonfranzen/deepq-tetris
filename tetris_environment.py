import numpy as np
import time

from tetromino import *
from colors import *

score_for_rows = {
    0: 0,
    1: 40,
    2: 100,
    3: 300,
    4: 1200
}

class TetrisEnvironment:

    def __init__(self, rows=20, cols=10):

        # state of the grid
        self.gameover = False
        self.rows = rows
        self.cols = cols
        self.padding = 3
        self.grid = np.zeros([rows+self.padding,cols+2*self.padding], np.int8)
        self.grid[:,0:self.padding] = -1
        self.grid[:,cols+self.padding:] = -1
        self.grid[rows:,:] = -1

        # type and position of the active tetromino
        self.active_tetromino = None
        self.at_row = None
        self.at_col = None

        # scores and levels
        self.score = 0

        # already determine which tetromimo we want next
        self.next_tetromino = Tetromino()

    def _filled_grid(self):
        fg = self.grid.copy()
        if self.active_tetromino is not None:
            fg[self.at_row:self.at_row+self.active_tetromino.size,
               self.at_col:self.at_col+self.active_tetromino.size] += self.active_tetromino.grid
        return fg

    def __str__(self):
        printed_grid = self._filled_grid()[:self.rows,self.padding:self.padding+self.cols]
        bar = (2*self.cols-1)*'='
        header = ' deep-Q TETRIS '.center(2*self.cols-1,'=')
        lines = [bar,header,bar]
        for r in range(self.rows):
            elements = []
            for c in range(self.cols):
                v = printed_grid[r,c]
                elements.append(color('{}'.format(v),blockcolors[v]))
            lines.append(' '.join(elements))
        lines.append(bar)
        lines.append('SCORE: {0}'.format(self.score))
        lines.append('NEXT:\n{0}'.format(self.next_tetromino))
        return '\n'.join(lines)

    def _spawn_new_tetromino(self):
        assert self.active_tetromino is None
        self.active_tetromino = self.next_tetromino
        self.next_tetromino = Tetromino()
        self.at_row = 0
        self.at_col = int(self.cols/2) + self.padding
        self.gameover = self._tetromino_overlaps(self.active_tetromino,
                                                 self.at_row, self.at_col)
        if self.gameover:
            self.active_tetromino = None

    def _tetromino_overlaps(self, t, r, c):
        return not np.all(t.grid * self.grid[r:r+t.size,
                                             c:c+t.size] == 0)

    def wait(self):
        reward = 0
        if self.active_tetromino is None:
            self._spawn_new_tetromino()
        else:
            # check if we can still move the active tetromino down
            if self._tetromino_overlaps(self.active_tetromino, self.at_row+1, self.at_col):
                # ... nope! this is the end ...
                self.grid = self._filled_grid() # dump the active tetro into the grid
                self.active_tetromino = None
                cleared_rows = self._clear_rows()
                reward = (1 + score_for_rows[cleared_rows])
                self._spawn_new_tetromino()
                self.score += reward
            else:
                self.at_row = self.at_row + 1
        return reward

    def _clear_rows(self):
        num_cleared_rows = 0
        r = self.rows-1
        while r >= 0:
            if np.all(self.grid[r,self.padding:self.padding+self.cols] != 0):
                num_cleared_rows += 1
                self.grid[1:r+1,self.padding:self.padding+self.cols] \
                    = self.grid[0:r,self.padding:self.padding+self.cols]
                self.grid[0,self.padding:self.padding+self.cols] = 0
            else:
                r -= 1
        return num_cleared_rows

    def drop(self):
        at_newrow = self.at_row
        while not self._tetromino_overlaps(self.active_tetromino, at_newrow+1, self.at_col):
            at_newrow += 1
        self.at_row = at_newrow

    def move_right(self):
        self._move(+1)

    def move_left(self):
        self._move(-1)

    def _move(self,m):
        at_newcol = self.at_col + m
        if not self._tetromino_overlaps(self.active_tetromino, self.at_row, at_newcol):
            self.at_col = at_newcol

    def rotate_right(self):
        self._rotate(-1)

    def rotate_left(self):
        self._rotate(+1)

    def _rotate(self, s):
        self.active_tetromino.rotate(s)
        if self._tetromino_overlaps(self.active_tetromino, self.at_row, self.at_col):
            self.active_tetromino.rotate(-s)
