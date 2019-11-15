import random
import numpy as np

class Tetromino:

    def __init__(self):
        # initialize possible shapes
        self.i = np.array([[0,1,0,0], [0,1,0,0], [0,1,0,0], [0,1,0,0]], int)
        self.o = np.array([[2,2],[2,2]], int)
        self.z = np.array([[0,0,0],[3,3,0],[0,3,3]], int)
        self.z_rev = np.array([[0,0,0],[0,4,4],[4,4,0]], int)
        self.l = np.array([[0,5,0],[0,5,0],[0,5,5]], int)
        self.l_rev = np.array([[0,6,0],[0,6,0],[6,6,6]], int)
        self.w = np.array([[0,0,0],[7,7,7],[0,7,0]], int)
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

    @property
    def size(self):
        return len(self.tetromino)

#tetromino = Tetromino()
#print(tetromino.size())
#print(tetromino.as_array())
#print("\n")
#tetromino.rotate(False)
#print(tetromino.as_array())
#tetromino.rotate(False)
#print(tetromino.as_array())
#tetromino.rotate(True)
#print(tetromino.as_array())
