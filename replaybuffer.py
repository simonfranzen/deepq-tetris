import random
import copy
from collections import namedtuple
from tetris_environment import *

Experience = namedtuple('Experience', ['state','action','reward','finished','next_state'])

class ReplayBuffer:

    def __init__(self, max_size):
        self.max_size = max_size
        self.experiences = []

    def add(self, experience):
        self.experiences.append(experience)
        if len(self.experiences) > self.max_size:
            del self.experiences[random.randint(0,len(self.experiences)-1)]

    def sample(self, sample_size):

        state_shape = self.experiences[0].state.shape
        batch = random.sample(self.experiences, sample_size)

        states = np.stack([exp.state for exp in batch]).astype(np.float32)
        actions = np.array([exp.action for exp in batch])
        rewards = np.array([exp.reward for exp in batch], dtype=np.float32)
        finished = np.array(np.array([exp.finished for exp in batch]))
        next_states = np.stack([exp.next_state for exp in batch]).astype(np.float32)

        return states, actions, rewards, finished, next_states

    def __len__(self):
        return len(self.experiences)

