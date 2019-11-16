import random
import torch
import copy
from collections import namedtuple
from tetris_environment import *

Experience = namedtuple('Experience', ['state','action','reward','next_state'])

class ReplayBuffer:

    def __init__(self, max_size, sample_size):
        self.max_size = max_size
        self.experiences = []
        self.sample_size = sample_size

    def add(self, experience):
        self.experiences.append(experience)
        if len(self.experiences) > self.max_size:
            del self.experiences[0]

    def sample(self):

        if len(self.experiences) < self.sample_size:
            return None

        state_size = list(self.experiences[0].state.size())[0]
        batch = random.sample(self.experiences, self.sample_size)

        states      = torch.zeros((self.sample_size,state_size,), dtype=torch.float)
        actions     = torch.zeros((self.sample_size), dtype=torch.long)
        rewards     = torch.zeros((self.sample_size), dtype=torch.float)
        next_states = torch.zeros((self.sample_size, state_size), dtype=torch.float)

        for i, exp in enumerate(batch):
            states[i,:] = exp.state
            actions[i] = exp.action
            rewards[i] = exp.reward
            next_states[i,:] = exp.next_state

        return Experience(states, actions, rewards, next_states)

    def add_recording(self, rec):
        for frame in rec.frames:
            state  = torch.from_numpy(frame.env.state)
            action = TetrisEnvironment.actions.index(frame.action) # <-- as an index
            reward = getattr(copy.deepcopy(frame.env), frame.action)()
            new_state = torch.from_numpy(frame.next_env.state)
            self.add(Experience(state, action, reward, new_state))

    def __len__(self):
        return len(self.experiences)
