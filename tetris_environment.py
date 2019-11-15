import numpy as np
from tetrominos import *

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
    6:'cyan'}

def color(s, c):
    return '\033[1;{};40m{}\033[0m'.format(colorcodes[c.lower()],s)


class TetrisEnvironment:

    def __init__(self, rows=20, cols=10):

        # state of the grid
        self._gameover = False
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros([rows,cols], np.int8)

        # type and position of the active tetromino
        self.active_tetromino = None
        self.at_row = None
        self.at_col = None

        # already determine which tetromimo we want next
        self.next_tetromino = Tetrominos().get_tetromino()

    @property
    def gameover(self):
        return _gameover

    def _filled_grid(self):
        fg = self.grid.copy()
        if self.active_tetromino is not None:
            fg[self.at_row:self.at_row+np.size(self.active_tetromino,0),
               self.at_col:self.at_col+np.size(self.active_tetromino,1)] = self.active_tetromino
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
        self.next_tetromino = Tetrominos().get_tetromino()
        self.at_row = 0
        self.at_col = round(self.cols/2) - np.size(self.active_tetromino,1)
        #self._gameover = self._tetromino_overlaps(self.active_tetromino,
        #                                          self.at_row, self.at_col)

    def wait(self):
        if self.active_tetromino is None:
            print('spawning new tetromino')
            self._spawn_new_tetromino()
        else:
            #move, check overlap, clear rows, etc ...
            pass

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


if __name__ == "__main__":
    env = TetrisEnvironment()
    env.grid[0,:] = 1
    env.grid[0,5] = 0
    env.grid[14,:] = 1
    env.grid[15,:] = 2
    env.grid[15,7] = 0
    env.grid[16,:] = 3
    env.grid[17,:] = 4
    env.grid[17,1:5] = 0
    env.grid[18,:] = 5
    env.grid[19,:] = 6
    print(env)
    print('num cleared rows =', env._clear_rows())
    print(env)
    env.wait()
    print(env)
