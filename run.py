import time
from pynput import keyboard
from tetris_environment import TetrisEnvironment
from audio_player import AudioPlayer
from highscore import Highscore
from utils import *
from recording import *

FPS = 60

def main():
    player = AudioPlayer()
    player.play()
    tetris_environment = TetrisEnvironment()
    rec = Recording('recording.pickle')
    timer = 0
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while not tetris_environment.gameover:

            if input_queue.qsize() > 0:
                key = input_queue.get()
                if key == 'q':
                    print('Exit the GAME')
                    break
                elif key == 'a' or key == '\x1b[D' or key == keyboard.Key.left:
                    rec.record_before_action(tetris_environment, 'move_left')
                    tetris_environment.move_left()
                    rec.record_after_action(tetris_environment)
                elif key == 'd' or key == '\x1b[C'  or key == keyboard.Key.right:
                    rec.record_before_action(tetris_environment, 'move_right')
                    tetris_environment.move_right()
                    rec.record_after_action(tetris_environment)
                elif key == 's' or key == '\x1b[B'  or key == keyboard.Key.down:
                    rec.record_before_action(tetris_environment, 'drop')
                    tetris_environment.drop()
                    rec.record_after_action(tetris_environment)
                elif key == 'w' or key == '\x1b[A' or key == '.' or key == keyboard.Key.up:
                    rec.record_before_action(tetris_environment, 'rotate_right')
                    tetris_environment.rotate_right()
                    rec.record_after_action(tetris_environment)
                elif key == ',':
                    rec.record_before_action(tetris_environment, 'rotate_left')
                    tetris_environment.rotate_left()
                    rec.record_after_action(tetris_environment)

                draw_board(tetris_environment)

            if timer % FPS == 0:
                rec.record_before_action(tetris_environment, 'wait')
                tetris_environment.wait()
                rec.record_after_action(tetris_environment)
                draw_board(tetris_environment)

            timer += 1
            time.sleep(1/FPS)

        player.stop()
        rec.store('recording.pickle')
        print('GAME OVER')
        print('YOUR SCORE: {0}'.format(tetris_environment.score))
        print('')
        highscore = Highscore()
        highscore.write(tetris_environment.score)
        print(highscore)
        exit(0)


if __name__ == '__main__':
    main()
