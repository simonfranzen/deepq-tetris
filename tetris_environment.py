import numpy as np

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
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros([rows,cols], np.int8)

    def __str__(self):
        bar = (2*self.cols-1)*'='
        lines = [bar]
        for r in range(self.rows):
            elements = []
            for c in range(self.cols):
                v = self.grid[r,c]
                elements.append(color('{}'.format(v),blockcolors[v]))
            lines.append(' '.join(elements))
        lines.append(bar)
        return '\n'.join(lines)

    def _clear_rows(self):
        num_cleared_rows = 0
        r = self.rows-1
        while r >= 0:
            if np.all(self.grid[r,:] != 0):
                print('deleting ', r)
                num_cleared_rows = num_cleared_rows + 1
                self.grid[1:r+1,:] = self.grid[0:r,:]
                self.grid[0,:] = 0
            else:
                r = r - 1
        return num_cleared_rows

#env = TetrisEnvironment()
#env.grid[0,:] = 1
#env.grid[0,5] = 0
#env.grid[14,:] = 1
#env.grid[15,:] = 2
#env.grid[15,7] = 0
#env.grid[16,:] = 3
#env.grid[17,:] = 4
#env.grid[17,1:5] = 0
#env.grid[18,:] = 5
#env.grid[19,:] = 6
#print(env)
#print('num cleared rows =', env._clear_rows())
#print(env)
