import random
import torch

class Experience:
    def __init__(self, state, action, reward, next_state):
        self.state = state
        self.action = action
        self.reward = reward
        self.next_state = next_state

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
