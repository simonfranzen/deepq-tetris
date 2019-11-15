import threading
import queue
import time
import os
from getch import _Getch

from pynput import keyboard

# from tetris_environment import TetrisEnvironment


input_queue = queue.Queue()

def on_press(key):
        try:
            print(key)
            input_queue.put(key)
            print(input_queue.qsize())
        except:
            print('Error wit key {0}.'.format(key))

def on_release(key):
    if key == keyboard.Key.esc:
        return False


# def read_kbd_input(input_queue):
#     while True:
#         getch = _Getch()
#         input_queue.put(getch.impl.getch())



def main():

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    print("after keyboard listener")

    while True:
        if input_queue.qsize() > 0:
            key = input_queue.get()
            print("Game Loop")
            print(key)
            if key == 'q':
                print('Exit GAME')
                is_running = False
                break
            elif key == 'a':
                print('move left')
            elif key == 'd':
                print('move right')
            elif key == 's':
                print('move down')
            else:
                print('wait')

        time.sleep(0.1)
        print('print game')



if __name__ == '__main__':
    main()
