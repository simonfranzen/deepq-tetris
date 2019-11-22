#from pynput import keyboard
import os
import queue

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

def draw_board(tetris_environment):
    clear()
    print(tetris_environment)
    #print(tetris_environment.state[:,:,0])

input_queue = queue.Queue()

def on_press(key):
        try:
            input_queue.put(key.char if hasattr(key, 'char') else key)
        except:
            print('Error wit key {0}.'.format(key))

def on_release(key):
    if key == keyboard.Key.esc:
        return False
