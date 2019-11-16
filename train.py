import os
import time
from tetris_environment import *
from replaybuffer import *
from utils import *
from plotter import Plotter
from datetime import datetime
from recording import *
from agent import *

max_score = 0
acc_score = 0
mean_score = 0
num_episodes_played = 0
num_moves_played = 0

replaybuffer = ReplayBuffer(100000)
if os.path.isfile('recording.pickle'):
    print('Loading experiences from a recording ...')
    rec = Recording('recording.pickle')
    replaybuffer.add_recording(rec)
    print('{} experiences loaded!'.format(len(replaybuffer)))
    time.sleep(2)

agent = DQNAgent(20*10+4*4,len(TetrisEnvironment.actions))

plotter = Plotter(datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
plotter.write('episode score moves_played mean_score move_left move_right drop wait rotate_right rotate_left')

while True:

    tetris_environment = TetrisEnvironment(20,10)
    draw_board(tetris_environment)

    moves_played_this_episode = 0
    actions_made = {
        'move_left': 0,
        'move_right': 0,
        'drop': 0,
        'wait': 0,
        'rotate_right': 0,
        'rotate_left': 0,
    }

    while not tetris_environment.gameover:

        state = tetris_environment.state
        actionidx = agent.act(state)
        reward = getattr(tetris_environment, TetrisEnvironment.actions[actionidx])()
        finished = tetris_environment.gameover
        next_state = tetris_environment.state

        replaybuffer.add(Experience(state, actionidx, reward, finished, next_state))
        agent.train(replaybuffer)

        num_moves_played += 1
        moves_played_this_episode += 1
        actions_made[TetrisEnvironment.actions[actionidx]] += 1

        draw_board(tetris_environment)
        print('')
        print('==== LEARNING STUFF ====')
        print('last action = {}'.format(TetrisEnvironment.actions[actionidx]))
        print('last reward = {}'.format(reward))
        print('epsilon = {}'.format(agent.epsilon))
        print('num moves played = {}'.format(num_moves_played))
        print('num episodes played = {}'.format(num_episodes_played))
        print('max score = {}'.format(max_score))
        print('mean score = {}'.format(mean_score))


    draw_board(tetris_environment)

    num_episodes_played += 1
    acc_score += tetris_environment.score
    mean_score = acc_score / num_episodes_played
    max_score = max(max_score, tetris_environment.score)
    print('GAME OVER')
    print('YOUR SCORE: {0}'.format(tetris_environment.score))

    plotter.write('{0} {1} {2} {3} {4}'.format(num_episodes_played, tetris_environment.score, moves_played_this_episode, mean_score, " ".join([str(actions_made[k]) for k in sorted(actions_made.keys())] ) ))


    time.sleep(0.2)
