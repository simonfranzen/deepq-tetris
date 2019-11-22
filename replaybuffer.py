import random
import copy
from collections import namedtuple
from tetris_environment import *

Experience = namedtuple('Experience', ['state','action','reward','finished','next_state'])
def experience_is_equivalent(e1, e2):
    return e1.action == e2.action and \
           e1.reward == e2.reward and \
           e1.finished == e2.finished and \
           np.array_equal(e1.state, e2.state) and \
           np.array_equal(e1.next_state, e2.next_state)


class ReplayBuffer:

    def __init__(self, max_size, no_shortterm_duplicates=False, protected_reward=None):
        self.max_size = max_size
        self.experiences = []
        self.no_shortterm_duplicates = no_shortterm_duplicates
        self.protected_reward = protected_reward

    def add(self, experience):
        if self.no_shortterm_duplicates and any(experience_is_equivalent(past_experience,experience) for past_experience in self.experiences[-10:]):
            return
        while len(self.experiences) >= self.max_size:
            randidx = random.randint(0,len(self.experiences)-1)
            if self.protected_reward is not None:
                while self.experiences[randidx].reward > self.protected_reward:
                    randidx = random.randint(0,len(self.experiences)-1)
            del self.experiences[randidx]
        self.experiences.append(experience)

    @property
    def avg_reward(self):
        return sum([exp.reward for exp in self.experiences])/len(self.experiences)

    def remove_duplicates(self):
        deleter = 1
        while deleter < len(self.experiences):
            if any(experience_is_equivalent(e,self.experiences[deleter]) for e in self.experiences[:deleter]):
                del self.experiences[deleter]
                print('Deleted duplicate experience {}!'.format(deleter))
            else:
                deleter +=1

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

