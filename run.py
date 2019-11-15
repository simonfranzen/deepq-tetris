import threading
import queue
import time

def read_kbd_input(inputQueue):
    print('Ready for keyboard input:')
    while (True):
        key = input()
        inputQueue.put(key)

def run():
    EXIT_COMMAND = 'exit'
    inputQueue = queue.Queue()

    inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,), daemon=True)
    inputThread.start()

    while (True):
        if (inputQueue.qsize() > 0):
            key = inputQueue.get()
            print('key = {}'.format(key))

            if (key == EXIT_COMMAND):
                print('Exiting serial terminal.')
                break
            elif key == 260:
                print('move left')
            elif key == 261:
                print('move right')
            elif key == 258:
                print('move down')
            else:
                continue

        time.sleep(1)
        print('hello')

    print('End.')


if __name__ == '__main__':
    run()
