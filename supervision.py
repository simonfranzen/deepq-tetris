#!/bin/python

from agent import *
from tetris_environment import *

import pickle

print('Loading replay buffer ...')
with open('replaybuffer.pickle', 'rb') as rbf:
    replaybuffer = pickle.load(rbf)
print('Loaded experiences in replay buffer: {}'.format(len(replaybuffer)))

agent = DQNAgent(216, len(TetrisEnvironment.actions),
                 training_batch_size=len(replaybuffer), training_epochs=10, target_model_lifetime=1)

for rliteration in range(1,101):
    print('RL iteration: {}'.format(rliteration))
    agent.train(replaybuffer)

agent.store_model('supervised_model.hdf5')
