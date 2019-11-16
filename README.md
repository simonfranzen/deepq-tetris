# DeepQ TETRIS - a 2 day hackathon project

## Goal
Creating a Tetris AI with Reinforcement Learning!

## Start
Watching videos about Reinforcement Learning :)

https://deeplizard.com/learn/video/nyjbcRQ-uQ8

## Dependencies

- [pytorch](https://pytorch.org/docs/stable/) for neural net
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
- plotting of results (soon)



## Trial and Error

### First generation
Getting negative reward for every move the AI does, based on the height of the highest tower in the game.

**Problem here (assumptions)**
For every move we punish the AI, so the AI optimized to make as less move as possible to finish one game. Because every rotation, every wait, every step left or right was a negative reward.


### Second generation
The AI was allowed to make moves without getting any negative rewards. If a tetromino was filed we gave negative rewards for the height of the largest tower. If the tower is greater than 16, then the negative reward was doubled.


### Third generation
Same like second generation, but we only gave negative rewards if the height of the largest tower increased. The number of negative rewards was based on the height it increased.


### Fourth generation
Reward of each action is 1 for each shape that is dropped summed up with the score for the cleared rows and the score of the game. Expectation is that the score of the game keeps rising when the AI plays longer games and therefore (hopefully) tries to stay in the game as long as possible. Negative reward is still having a tower height greater than 16.
