import random
import numpy as np
import time

from tetromino import *

colorcodes = {
    'black':30,
    'red':31,
    'green':32,
    'yellow':33,
    'blue':34,
    'purple':35,
    'cyan':36,
    'white':37}

blockcolors = {
    0:'black',
    1:'red',
    2:'green',
    3:'yellow',
    4:'blue',
    5:'purple',
    6:'cyan',
    7:'white'}

def color(s, c):
    return '\033[1;{};40m{}\033[0m'.format(colorcodes[c.lower()],s)


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

        # already determine which tetromimo we want next
        self.next_tetromino = Tetromino()

    def _filled_grid(self):
        fg = self.grid.copy()
        if self.active_tetromino is not None:
            fg[self.at_row:self.at_row+self.active_tetromino.size,
               self.at_col:self.at_col+self.active_tetromino.size] += self.active_tetromino.as_array()
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
        print('r', r)
        print('c', c)
        print('t', t.as_array())
        return not np.all(t.as_array() * self.grid[r:r+t.size,
                                                   c:c+t.size] == 0)

    def wait(self):
        if self.active_tetromino is None:
            print('spawning new tetromino')
            self._spawn_new_tetromino()
        else:
            # check if we can still move the active tetromino down
            if self.at_row == self.rows - self.active_tetromino.size \
            or self._tetromino_overlaps(self.active_tetromino, self.at_row+1, self.at_col):
                # ... nope! this is the end ...
                print('no space')
                self.grid = self._filled_grid() # dump the active tetro into the grid
                self.active_tetromino = None
                self._clear_rows()
                self._spawn_new_tetromino()
            else:
                print('we have space -> moving')
                self.at_row = self.at_row + 1

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


    def move_down():
        print('move down')

    def move_right():
        print('move right')

    def move_left():
        print('move left')

    def rotate_right():
        print('rotate right')

    def rotate_left():
        print('rotate left')



if __name__ == "__main__":
    env = TetrisEnvironment()
    while not env.gameover:
        print(env)
        time.sleep(0.1)
        env.wait()
    print('Game over!')
