import queue
import time
import os
from pynput import keyboard
from tetris_environment import TetrisEnvironment


input_queue = queue.Queue()


clear = lambda:  os.system('cls' if os.name=='nt' else 'clear')

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
                print(key)
                if key == 'q':
                    print('Exit the GAME')
                    break
                elif key == 'a' or key == '\x1b[D' or key == keyboard.Key.left:
                    tetris_environment.move_left()
                elif key == 'd' or key == '\x1b[C'  or key == keyboard.Key.right:
                    tetris_environment.move_right()
                elif key == 's' or key == '\x1b[B'  or key == keyboard.Key.down:
                    tetris_environment.move_down()
                elif key == 'w' or key == '\x1b[A' or key == '.' or key == keyboard.Key.up:
                    tetris_environment.rotate_right()
                elif key == ',':
                    tetris_environment.rotate_left()

            tetris_environment.wait()
            time.sleep(0.1)
            clear()
            print(tetris_environment)

        listener.join()


if __name__ == '__main__':
    main()
