import time
from tetris_environment import TetrisEnvironment

running = True


def run():

    env = TetrisEnvironment()
    env.grid[0,:] = 1
    env.grid[0,5] = 0
    env.grid[14,:] = 1
    env.grid[15,:] = 2
    env.grid[15,7] = 0
    env.grid[16,:] = 3
    env.grid[17,:] = 4
    env.grid[17,1:5] = 0
    env.grid[18,:] = 5
    env.grid[19,:] = 6
    print(env)

    while running:
        time.sleep(1)

        # get keyboard input, returns -1 if none available
        
        key = input('My test input')
        print(key)

        if key != -1:
            if key == 260:
                print(key)
            elif key == 261:
                print(key)
            elif key == 258:
                print(key)
            elif key == 91:
                print(key)
            else:
                print(key)
            

# def run():
#     # tetris_environment = TetrisEnvironment()
#     print('Press Q for quit')

#     while running:
#         stdscr.nodelay(True)

#         key = curses.wrapper(keypress)

#         print("key:", curses.wrapper(keypress)) # prints: 'key: 97' for 'a' pressed
#         time.sleep(1)

#         if key == 27:
#             tetris_environment.move_left()
#         elif key == 91:
#             tetris_environment.move_right()
#         elif key == 91:
#             tetris_environment.move_down()
#         elif key == 91:
#             tetris_environment.move_right()

        # elif keyboard.is_pressed('a'):
        #     # tetris_environment.render()
        # elif keyboard.is_pressed('s'):
        #     # tetris_environment.render()
        # elif keyboard.is_pressed('d'):
        #     # tetris_environment.render()
        # elif keyboard.is_pressed('f'):
            # tetris_environment.render()


        # key_events() 
        #update() # update all objects that need to be updated, e.g. position changes, physics, all that other stuff
        # tetris_environment.render() #render things on screen


if __name__ == "__main__":
    run()
