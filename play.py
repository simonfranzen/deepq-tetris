#!/usr/bin/env python

import time
from pynput import keyboard
from tetris_environment import TetrisEnvironment
from audio_player import AudioPlayer
from highscore import Highscore
from utils import *

FPS = 24

def main():
    player = AudioPlayer()
    player.play()
    tetris_environment = TetrisEnvironment()
    timer = 0
    reward = 0
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while not tetris_environment.gameover:

            if input_queue.qsize() > 0:
                key = input_queue.get()
                if key == 'q':
                    print('Exit the GAME')
                    break
                elif key == 'a' or key == '\x1b[D' or key == keyboard.Key.left:
                    reward = tetris_environment.move_left()
                elif key == 'd' or key == '\x1b[C'  or key == keyboard.Key.right:
                    reward = tetris_environment.move_right()
                elif key == 's' or key == '\x1b[B'  or key == keyboard.Key.down:
                    reward = tetris_environment.drop()
                elif key == 'w' or key == '\x1b[A' or key == '.' or key == keyboard.Key.up:
                    reward = tetris_environment.rotate_right()
                elif key == ',':
                    reward = tetris_environment.rotate_left()

                draw_board(tetris_environment)
                print('Reward: {}'.format(reward))

            if timer % FPS == 0:
                reward = tetris_environment.wait()
                draw_board(tetris_environment)
                print('Reward: {}'.format(reward))

            timer += 1
            time.sleep(1/FPS)

        player.stop()
        print('GAME OVER')
        print('YOUR SCORE: {0}'.format(tetris_environment.score))
        print('')
        highscore = Highscore()
        highscore.write(tetris_environment.score)
        print(highscore)
        exit(0)


if __name__ == '__main__':
    main()
