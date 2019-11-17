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

        state_size = np.size(self.experiences[0].state,0)
        batch = random.sample(self.experiences, sample_size)

        actions = np.array([exp.action for exp in batch])
        rewards = np.array([exp.reward for exp in batch], dtype=np.float32)
        finished = np.array(np.array([exp.finished for exp in batch]))

        # collect states and next_states of the batch in
        states      = np.zeros((sample_size, state_size), dtype=np.float32)
        next_states = np.zeros((sample_size, state_size), dtype=np.float32)
        for i, exp in enumerate(batch):
            states[i,:] = exp.state
            next_states[i,:] = exp.next_state

        return states, actions, rewards, finished, next_states

    def __len__(self):
        return len(self.experiences)

