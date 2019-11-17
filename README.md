# DeepQ TETRIS - a 3 day hackathon project

## Goal
Do Reinforcement Learning to train an AI to play the popular game Tetris. We are using a neural network to predict a Q-function that returns the best next action for the current state of the game.

In Reinforcement Learning you train the model in the beginning with random actions to obtain as much information about the environment as possible. The biggest problem with Tetris is, that clearing a line is nothing which occurs randomly. So the network will only see a cleared row every ~20k moves.

For this problem we tried out different things like Supervised Learning, improving reward function that the player gets rewarded not just for clearing lines or dropping one shape ( rewards based on bumpiness, number of holes, heights of the towers), grouping actions together.

These heuristic model improved our network over the time that the AI was able to make more and more points each round.

**BUT: We did not reach the goal to build a working Tetris AI in just 3 days.**


## Motivation
Learning something new is great. Learning something about Artificial Intelligence is even better. We all are developers in companies where they touch the topic AI just little, so we decided to make a private hackathon and to dive into the topic of Reinforcement Learning. 

We are not Data Scientists and we do not work with Machine Learning on a daily basis. We have a understanding of what a AI in general does, but we haven't implemented an algorithm like Reinforcement Learning before.

The plan was to build an AI which can play a game. We have seen some youtube videos about building a Tetris AI with Evolutionary Algorithms. We decided to not do it with EA, we decided to do it with Reinforcement Learning, because we knew that there are AIs out there which can already play half of the Atari games. 

We didn't know before that Tetris is such a hard game. After the hackathon We had to confess, that we should have chosen an easier game to learn the implementation of Reinforcement Learning. 

## AI for games

If you don't know anything about Reinforcement Learning you should read the DeepMind's paper in 2013 and their follow up papery in 2015. The AI's they trained played pretty well most of the Atari video games and their results are very impressive. 

You might also have heard of Google's AI playing GO and beating the best GO players of the world. 

Our first day at the hackathon was about understanding the techniques of Reinforcement Learning so we decided to watch all the videos on [deeplizard.com](https://deeplizard.com/learn/video/nyjbcRQ-uQ8). These videos helped us to get a common understanding of the process of the algorithm.

We have also watched the approach of Evolutionary Algorithm where some guz implemented a Tetris AI in Javascript.

All this was our input for starting the small project. What we have not known was the fact that these algorithms achieve superhuman power for games, where the player gets immediately a reward for an action, but they fail hard for games which require a long-term strategic planning to get a reward. 

We aren't experts in the field of AI, so we learned after the Hackathon that we really tried to solve a hard problem where even [students from Stanford University](http://cs231n.stanford.edu/reports/2016/pdfs/121_Report.pdf) had their problems. This paper was eye-opening for us, but we have read it at the end of our Hackathon. 

How sad! But we will take their ideas and concepts to improve our algorithm to finally get a working Tetris AI.


## Methods

### The Deep Reinforcement Learning Algorithm
We used the classic approach for Reinforcement Learning and our network trues to approximate a function Q:

TODO 

**Bellman equation**

TODO


#### State


#### Actions


#### Rewards


### Neural Network


#### Training


#### Epsilon


#### Replay Buffer



### The Game
To have everything under control we have build our own Tetris with Python which can run directly in the console. It was pretty easy for us to implement the Game at Day 1 of our hackathon. To have our own Tetris it allows to record human players, to tweek the game (e.g. drop only quads instead of all kind of shapes)

#### Game states
The state in the game at time `t` is simply the Tetris grid of 10 x 20 plus the next Tetromino you see as a user. This is the same as the human player can see when playing Tetris. Other Reinforcement Learning algorithm are screen capturing images from the game emulator to feed the Neural Net. We decided to not use images to remove complexity from our hackathon project.

#### Game Actions
We have chosen the classical way and the actions of the game are the actions you can make as a user with the Joystick. 

These are our actions we track:
 - move left
 - move right
 - rotate right
 - rotate left
 - wait
 - drop


We want to improve this actions, by adding combination of actions together:

```
3 directional actions (left, right, wait) * 4 rotation actions (0, 90, 180, 270 degrees)

+

drop the shape
```

In total these are 13 actions.


##### We have to improve

???? GROUPED ACTIONS ???? 

#### Rewards
The primarliy rewards are based on the Tetris Gamescore. For every line the player cleared you get a certain amount of score.

TODO heuristic calc (aggregate height, holes, bumpiness)

##### We have to improve
 - Extra negative rewards when loosing the game


### Results

#### Evaluation Metrics

- achieved score in one game
- moves the AI took in one round
- the average award over 1000 moves
-  ??

#### Tweek the variables
- random drop in of shapes
- changing epsilon
- using Supervised Learning to train in the beginning
- ????


### Discussion

#### Grouping Actions

#### From easy Tetris to Advanced

#### Remove a bit of randomness


### Final words



### The project


## Dependencies

- [keras](???) for neural net
- [pygame](https://www.pygame.org/news) for sound
- [pynput](https://pypi.org/project/pynput/) for keyboard listeners


## Usage

You can either play the game yourself, or train the AI by letting it play.

To train the AI call:
`python train.py`

Or play the game yourself to set a new highscore!
`python run.py`


## Features

- 7 unique Tetromino shapes
- best music
- highscore lists
- watch the AI play
- plotting of results
- record human player and train network with that data





