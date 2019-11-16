import numpy as np
import time

from tetromino import *
from colors import *

"""The module that handles the game state and interactions with it"""

score_for_rows = {
    0: 0,
    1: 40,
    2: 100,
    3: 300,
    4: 1200
}

class TetrisEnvironment:
    """ a class responsible for the game's logic and printing the visuals to console """

    actions = ['move_left', 'move_right', 'wait', 'drop', 'rotate_right', 'rotate_left']

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

        self.wait()

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
        self.add_game_info(lines)
        return '\n'.join(lines)

    def add_game_info(self, lines):
        """ prints out score and next tetromino information right of the board"""
        padding = 5*' '
        # row to start at (from the top)
        start_at = 4
        tetromino_rows = format(self.next_tetromino).split('\n')
        # take first index in case top row is empty
        tetromino_color = format(self.next_tetromino).replace(' ', '').replace('\n', '')[0]
        # add score
        lines[start_at] = lines[start_at] + padding + 'SCORE: {0}'.format(self.score)

        # a look in the future
        line_idx = start_at+2;
        lines[line_idx] = lines[line_idx] + padding + 'NEXT TETROMINO:'
        line_idx = line_idx+2
        padding = padding+ 2*' '
        for row in tetromino_rows:
            line_idx = line_idx +1;
            lines[line_idx] = lines[line_idx]+padding+color('{}'.format(row),blockcolors[int(tetromino_color)])


    def _spawn_new_tetromino(self):
        """ creates a new random tetromino, except if gameover is true"""
        assert self.active_tetromino is None
        self.active_tetromino = self.next_tetromino
        self.next_tetromino = Tetromino()
        self.at_row = 0
        self.at_col = int(self.cols/2) + self.padding - 1
        self.gameover = self._tetromino_overlaps(self.active_tetromino,
                                                 self.at_row, self.at_col)
        if self.gameover:
            self.active_tetromino = None

    def _tetromino_overlaps(self, t, r, c):
        """ checks if the tetromino overlaps with another tetromino or the borders of the game board"""
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
                old_height = self._height()
                self.grid = self._filled_grid() # dump the active tetro into the grid
                self.active_tetromino = None
                cleared_rows = self._clear_rows()
                reward = 1 + score_for_rows[cleared_rows] - (self._height() - old_height)
                if self._height() >= 16:
                    reward -= 40
                self._spawn_new_tetromino()
                self.score += 1 + score_for_rows[cleared_rows]
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
        return self.wait()

    def move_right(self):
        self._move(+1)
        return 0

    def move_left(self):
        self._move(-1)
        return 0

    def _move(self,m):
        at_newcol = self.at_col + m
        if not self._tetromino_overlaps(self.active_tetromino, self.at_row, at_newcol):
            self.at_col = at_newcol

    def rotate_right(self):
        self._rotate(-1)
        return 0

    def rotate_left(self):
        self._rotate(+1)
        return 0

    def _rotate(self, s):
        self.active_tetromino.rotate(s)
        if self._tetromino_overlaps(self.active_tetromino, self.at_row, self.at_col):
            self.active_tetromino.rotate(-s)

    def _height(self):
        for h in range(self.rows-1,-1,-1):
            if np.all(self.grid[h,self.padding:self.padding+self.cols] == 0):
                return self.rows - h - 1
        return self.rows

    @property
    def state(self):
        if self.gameover:
            return np.ones((self.rows*self.cols+4*4), np.float32)
        fg = self.grid.copy()
        if self.active_tetromino is not None:
            fg[self.at_row:self.at_row+self.active_tetromino.size,
               self.at_col:self.at_col+self.active_tetromino.size] -= self.active_tetromino.grid
        fg = np.clip(fg[:self.rows,self.padding:self.padding+self.cols], -1, 1)
        top_of_pile = 0
        while top_of_pile < self.rows \
        and not np.any(fg[top_of_pile,:] == 1):
            top_of_pile += 1
        ntg = self.next_tetromino.grid.copy()
        ntg.resize((4,4))
        return np.concatenate((np.clip(ntg.flatten(), 0, 1),
                               fg[top_of_pile:,:].flatten(),
                               fg[:top_of_pile,:].flatten())).astype(np.float32)
