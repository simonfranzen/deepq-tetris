import random
import numpy as np

tetromino_grids = {

    'i': np.array([[0,1,0,0],
                   [0,1,0,0],
                   [0,1,0,0],
                   [0,1,0,0]], np.int8),

    'o': np.array([[2,2],
                   [2,2]], np.int8),

    'z': np.array([[0,0,0],
                   [3,3,0],
                   [0,3,3]], np.int8),

'z_rev': np.array([[0,0,0],
                   [0,4,4],
                   [4,4,0]], np.int8),

    'l': np.array([[0,5,0],
                   [0,5,0],
                   [0,5,5]], np.int8),

'l_rev': np.array([[0,6,0],
                   [0,6,0],
                   [6,6,0]], np.int8),

    't': np.array([[0,0,0],
                   [7,7,7],
                   [0,7,0]], np.int8)
}


class Tetromino:

    def __init__(self, t= None):
        if t == None or t not in tetromino_grids:
            self.type = random.choice(list(tetromino_grids.keys()))
        else:
            self.type = t
        self.grid = tetromino_grids[self.type]
        self.rotate(random.randint(0,4))


    def rotate(self, steps):
        if self.type != 'o':
            self.grid = np.rot90(self.grid, steps)

    @property
    def size(self):
        return np.size(self.grid, 0)

    def __str__(self):
        lines = []
        for row in self.grid:
            elements = []
            for col in row:
                if col != 0:
                    elements.append(format(col))
                else:
                    elements.append(' ')
            lines.append(' '.join(elements))
        return '\n'.join(lines);

