import copy
import pickle
from collections import namedtuple
import os.path
import sys

from tetris_environment import *
from utils import *

RecordFrame = namedtuple('RecordFrame', ['env','action','next_env'])

class Recording:

    def __init__(self, filename='recording.pickle'):
        # list of recorded frames
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                self.frames = pickle.load(f)
        else:
            self.frames = []
        # frame that is currently being recorded
        self.env      = None
        self.action   = None

    def store(self, filename='recording.pickle'):
        with open(filename, 'wb') as f:
            pickle.dump(self.frames, f)

    def record_before_action(self, env, action):
        assert self.env is None
        assert action in TetrisEnvironment.actions
        self.env = copy.deepcopy(env)
        self.action = action

    def record_after_action(self, next_env):
        assert self.env is not None
        self.frames.append(RecordFrame(self.env, self.action, copy.deepcopy(next_env)))
        self.env    = None
        self.action = None

    def play(self, fps=2):
        for frame in self.frames:
            draw_board(frame.env)
            time.sleep(1/fps)
