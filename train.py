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
mean_rewards= 0
num_episodes_played = 0
num_moves_played = 0
t_counter = 0
t_max_count = 0

replaybuffer = ReplayBuffer(100000)

if os.path.isfile('recording.pickle'):
    print('Loading experiences from a recording ...')
    rec = Recording('recording.pickle')
    replaybuffer.add_recording(rec)
    print('{} experiences loaded!'.format(len(replaybuffer)))
    time.sleep(2)

agent = DQNAgent(216,len(TetrisEnvironment.actions))
plotter = Plotter(datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))



def draw_training_info(tetris_environment, reward, actionidx):
    print('')
    print('==== LEARNING STUFF ====')
    print('last action = {}'.format(TetrisEnvironment.actions[actionidx]))
    print('last reward = {}'.format(reward))
    print('epsilon = {}'.format(agent.epsilon))
    print('num moves played = {}'.format(num_moves_played))
    print('num episodes played = {}'.format(num_episodes_played))
    print('max score = {}'.format(max_score))
    print('mean score = {}'.format(mean_score))
    print('mean rewards last 1000 = {}'.format(mean_rewards))
    print('aggregate height = {}'.format(tetris_environment.aggregate_height))
    print('holes = {}'.format(tetris_environment.holes))
    print('cleared rows = {}'.format(tetris_environment.cleared_rows))
    print('bumpiness = {}'.format(tetris_environment.bumpiness))
    

while True:

    tetris_environment = etrisEnvironment(20,10,'o') if t_counter < t_max_count else TetrisEnvironment(20,10)
    t_counter += 1
    
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

    rewards = []

    while not tetris_environment.gameover:
        
        state = tetris_environment.state
        actionidx = 3 if num_moves_played % 30 == 0 else agent.act(state)
        reward = getattr(tetris_environment, TetrisEnvironment.actions[actionidx])()
        finished = tetris_environment.gameover
        next_state = tetris_environment.state

        replaybuffer.add(Experience(state, actionidx, reward, finished, next_state))
        agent.train(replaybuffer)

        rewards.append(reward)
        num_moves_played += 1
        moves_played_this_episode += 1
        actions_made[TetrisEnvironment.actions[actionidx]] += 1

        if num_moves_played % 1000 == 0:
            # clear rewards to reset mean_rewards value
            rewards.clear()
        
        # draw the game
        draw_board(tetris_environment)
        draw_training_info(tetris_environment, reward, actionidx)
        
        # time.sleep(0.1)


    draw_board(tetris_environment)
    draw_training_info(tetris_environment, reward, actionidx)


    num_episodes_played += 1
    acc_score += tetris_environment.score
    mean_score = acc_score / num_episodes_played
    max_score = max(max_score, tetris_environment.score)
    print('GAME OVER')
    print('YOUR SCORE: {0}'.format(tetris_environment.score))
    mean_rewards_len = len(rewards)
    if mean_rewards_len == 0:
        mean_rewards_len = 1
    mean_rewards = (sum(rewards) / mean_rewards_len)

    plotter.write('{0} {1} {2} {3} {4} {5}'.format(num_episodes_played, tetris_environment.score, moves_played_this_episode, mean_score, mean_rewards, " ".join([str(actions_made[k]) for k in sorted(actions_made.keys())] ) ))

    agent.store_model('model.hdf5')

    time.sleep(0.5)


