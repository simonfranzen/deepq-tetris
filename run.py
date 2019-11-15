import threading
import queue
import time
import os

from pynput import keyboard

from tetris_environment import TetrisEnvironment


input_queue = queue.Queue()

def on_press(key):
        try:
            input_queue.put(key)
        except:
            print('Error wit key {0}.'.format(key))

def on_release(key):
    if key == keyboard.Key.esc:
        return False



def main():

    tetris_environment = TetrisEnvironment()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:

        while True:
            if input_queue.qsize() > 0:
                key = input_queue.get()
                if key == 'q':
                    print('Exit GAME')
                    is_running = False
                    break
                elif key == 'a':
                    tetris_environment.move_left()
                elif key == 'd':
                    tetris_environment.move_right()
                elif key == 's':
                    tetris_environment.move_down()

            tetris_environment.wait()
            time.sleep(0.5)
            print(tetris_environment)

        listener.join()


if __name__ == '__main__':
    main()
