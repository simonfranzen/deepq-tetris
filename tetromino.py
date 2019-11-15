import random
import numpy as np

class Tetromino:

    def __init__(self):
        # initialize possible shapes
        self.i = np.array([[0,1,0,0], [0,1,0,0], [0,1,0,0], [0,1,0,0]], int)
        self.o = np.array([[1,1],[1,1]], int)
        self.z = np.array([[0,0,0],[1,1,0],[0,1,1]], int)
        self.z_rev = self.z[::-1]
        self.l = np.array([[0,1,0],[0,1,0],[0,1,1]], int)
        self.l_rev = self.l[::-1]
        self.w = np.array([[0,0,0],[1,1,1],[0,1,0]], int)
        self.tetrominos = np.array([self.i, self.o, self.z, self.z_rev, self.l, self.l_rev, self.w])
        # select random tetromino
        self.tetromino = self.tetrominos[(random.randint(0, len(self.tetrominos)-1))]

    def rotate(self, counter_clockwise = True):
        """ rotates a tetromino by 90 degrees """
        steps = 1
        if(counter_clockwise == False):
            steps = 3
        self.tetromino = np.rot90(self.tetromino, steps)

    def as_array(self):
        return self.tetromino


#tetromino = Tetromino()
#print(tetromino.as_array())
#tetromino.rotate(False)
#print(tetromino.as_array())
#tetromino.rotate(False)
#print(tetromino.as_array())
#tetromino.rotate(True)
#print(tetromino.as_array())
