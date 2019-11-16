import os
import time
import random
from tetris_environment import *
from replaybuffer import *
from utils import *
from dqnn import *
from plotter import Plotter
from datetime import datetime
from recording import *

max_score = 0
num_episodes_played = 0
num_moves_played = 0

learning_rate = 0.001

epsilon = 1.0
eps_decay = 0.99999

gamma = 0.999

replaybuffer = ReplayBuffer(1000000, 300)
if os.path.isfile('recording.pickle'):
    rec = Recording('recording.pickle')
    replaybuffer.add_recording(rec)
    print('Loaded {} experiences from a recording ...'.format(len(replaybuffer)))
    time.sleep(2)

# Setup neural networks
policy_net = DQNN(216,len(TetrisEnvironment.actions))
target_net = DQNN(216,len(TetrisEnvironment.actions))
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()
optimizer = torch.optim.Adam(params=policy_net.parameters(), lr=learning_rate)


plotter = Plotter(datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))

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

        state = torch.from_numpy(tetris_environment.state)

        epsilon *= eps_decay
        if random.random() < epsilon:
            motivation = 'exploration'
            actionidx = random.randint(0,len(TetrisEnvironment.actions)-1)
        else:
            motivation = 'exploitation'
            with torch.no_grad():
                actionidx = policy_net(state).argmax()

        actions_made[actions[actionidx]] += 1

        reward    = getattr(tetris_environment, TetrisEnvironment.actions[actionidx])()
        next_state = torch.from_numpy(tetris_environment.state)

        if tetris_environment.gameover: continue
        replaybuffer.add(Experience(state, actionidx, reward, next_state))

        exp_sample = replaybuffer.sample()
        if exp_sample is not None:
            current_q = policy_net(exp_sample.state).gather(dim=1, index=exp_sample.action.unsqueeze(-1))
            next_q    = target_net(exp_sample.next_state).max(dim=1)[0].detach()
            target_q  = exp_sample.reward + (gamma * next_q)

            loss = torch.nn.functional.mse_loss(current_q, target_q.unsqueeze(1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        num_moves_played += 1
        if num_moves_played % 1000 == 0:
            target_net.load_state_dict(policy_net.state_dict())


        moves_played_this_episode += 1

        draw_board(tetris_environment)
        print('')
        print('==== LEARNING STUFF ====')
        print('motivation = {}'.format(motivation))
        print('last action = {}'.format(TetrisEnvironment.actions[actionidx]))
        print('last reward = {}'.format(reward))
        print('epsilon = {}'.format(epsilon))
        print('num moves played = {}'.format(num_moves_played))
        print('num episodes played = {}'.format(num_episodes_played))
        print('max score = {}'.format(max_score))
        print('tower high punishment = {}'.format(tetris_environment._height()))
        #time.sleep(0.05)



    draw_board(tetris_environment)

    num_episodes_played += 1
    max_score = max(max_score, tetris_environment.score)
    print('GAME OVER')
    print('YOUR SCORE: {0}'.format(tetris_environment.score))

    plotter.write('{0} {1} {2} {3}'.format(num_episodes_played, tetris_environment.score, moves_played_this_episode, " ".join([str(actions_made[k]) for k in sorted(actions_made.keys())] ) ))

    time.sleep(0.2)
