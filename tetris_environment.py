import random
import numpy as np
import time

from tetromino import *
from colors import *

class TetrisEnvironment:

    def __init__(self, rows=20, cols=10):

        # state of the grid
        self.gameover = False
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros([rows,cols], np.int8)

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
        filled_grid = self._filled_grid()
        bar = (2*self.cols-1)*'='
        header = ' deep-Q TETRIS '.center(2*self.cols-1,'=')
        lines = [bar,header,bar]
        for r in range(self.rows):
            elements = []
            for c in range(self.cols):
                v = filled_grid[r,c]
                elements.append(color('{}'.format(v),blockcolors[v]))
            lines.append(' '.join(elements))
        lines.append(bar)
        lines.append('SCORE: {0}'.format(self.score))
        return '\n'.join(lines)

    def _spawn_new_tetromino(self):
        assert self.active_tetromino is None
        self.active_tetromino = self.next_tetromino
        self.next_tetromino = Tetromino()
        self.at_row = 0
        self.at_col = random.randint(0,self.cols-self.active_tetromino.size)
        self.gameover = self._tetromino_overlaps(self.active_tetromino,
                                                 self.at_row, self.at_col)

    def _tetromino_overlaps(self, t, r, c):
        #print('r', r)
        #print('c', c)
        #print('t', t.grid)
        return not np.all(t.grid * self.grid[r:r+t.size,
                                             c:c+t.size] == 0)

    def score_for_rows(self):
        return {
            0: 0,
            1: 40,
            2: 100,
            3: 300,
            4: 1200
        }

    def wait(self):
        cleared_rows = 0
        if self.active_tetromino is None:
            #print('spawning new tetromino')
            self._spawn_new_tetromino()
        else:
            # check if we can still move the active tetromino down
            if self.at_row == self.rows - self.active_tetromino.size \
            or self._tetromino_overlaps(self.active_tetromino, self.at_row+1, self.at_col):
                # ... nope! this is the end ...
                #print('no space')
                self.grid = self._filled_grid() # dump the active tetro into the grid
                self.active_tetromino = None
                cleared_rows = self._clear_rows()
                self._spawn_new_tetromino()
                self.score += (1 + self.score_for_rows()[cleared_rows])
            else:
                #print('we have space -> moving')
                self.at_row = self.at_row + 1

        return cleared_rows

    def _clear_rows(self):
        num_cleared_rows = 0
        r = self.rows-1
        while r >= 0:
            if np.all(self.grid[r,:] != 0):
                num_cleared_rows = num_cleared_rows + 1
                self.grid[1:r+1,:] = self.grid[0:r,:]
                self.grid[0,:] = 0
            else:
                r = r - 1
        return num_cleared_rows


    def move_down(self):
        print('move down')

    def move_right(self):
        self.at_col = min(self.at_col+1, self.cols-self.active_tetromino.size)

    def move_left(self):
        self.at_col = max(self.at_col-1, 0)

    def rotate_right(self):
        print('rotate right')

    def rotate_left(self):
        print('rotate left')



if __name__ == "__main__":
    env = TetrisEnvironment()
    while not env.gameover:
        print(env)
        env.wait()
    print('Game over!')
