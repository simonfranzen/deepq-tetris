#!/usr/bin/env python

import time
from pynput import keyboard
from tetris_environment import TetrisEnvironment
from audio_player import AudioPlayer
from highscore import Highscore
from utils import *

FPS = 60

def main():
    player = AudioPlayer()
    player.play()
    tetris_environment = TetrisEnvironment()
    timer = 0
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while not tetris_environment.gameover:

            if input_queue.qsize() > 0:
                key = input_queue.get()
                if key == 'q':
                    print('Exit the GAME')
                    break
                elif key == 'a' or key == '\x1b[D' or key == keyboard.Key.left:
                    tetris_environment.move_left()
                elif key == 'd' or key == '\x1b[C'  or key == keyboard.Key.right:
                    tetris_environment.move_right()
                elif key == 's' or key == '\x1b[B'  or key == keyboard.Key.down:
                    tetris_environment.drop()
                elif key == 'w' or key == '\x1b[A' or key == '.' or key == keyboard.Key.up:
                    tetris_environment.rotate_right()
                elif key == ',':
                    tetris_environment.rotate_left()

                draw_board(tetris_environment)

            if timer % FPS == 0:
                tetris_environment.wait()
                draw_board(tetris_environment)

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
