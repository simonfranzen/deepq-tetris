import random
import numpy as np

class Tetrominos:

    def __init__(self):
        self.i = np.array([[0,1,0,0], [0,1,0,0], [0,1,0,0], [0,1,0,0]])
        self.o = np.array([[1,1],[1,1]])
        self.z = np.array([[1,1,0],[0,1,0],[0,1,1]])
        self.l = np.array([[0,1,0],[0,1,0],[0,1,1]])
        self.tetrominos = np.array([self.i, self.o, self.z, self.l])
        # select random tetromino
        self.tetromino = self.tetrominos[(random.randint(0, len(self.tetrominos)-1))]


    def get_tetromino(self):
        return self.tetromino


#tetrominos = Tetrominos();
#tetromino = tetrominos.get_tetromino();
#print(tetromino);

