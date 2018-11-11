'''
Snake games
'''
import os
import sys
import platform
from time import sleep
from queue import deque

import numpy as np
from pynput.keyboard import Key, Controller, Listener

from snake import Snake
from world_map import Map
from candy import Candy

if platform.system() == 'Windows':
    def clear(): return os.system('cls')
elif platform.system() == 'Darwin':
    def clear(): return os.system('clear')

action = deque([])
exit_game = False

def render(str_list):
    clear()
    for stri in str_list:
        for char in stri:
            print(char, end='')
        print('')

def on_press(key):
    global action, exit_game

    try:
        pressed_button = key.char
        if pressed_button == 'w':
            action.append('u')

        elif pressed_button == 's':
            action.append('d')

        elif pressed_button == 'd':
            action.append('r')

        elif pressed_button == 'a':
            action.append('l')

    except:

        if key == Key.alt:
            action.append('u')

        elif key == Key.cmd:
            action.append('d')

        elif key == Key.alt_r:
            action.append('r')

        elif key == Key.cmd_r:
            action.append('l')

        elif key == Key.shift_r:
            exit_game = True

def on_release(key):
    return
        

        

if __name__ == "__main__":

    with Listener(on_press=on_press, on_release=on_release) as listener:
        # 'play' 'dead' 'init'
        game_state = 'init'
        while True:
            if exit_game: break
            if game_state == 'init':
                width = 30
                height = 10
                snake = Snake(width, height)
                world_map = Map(width, height)
                candy = Candy(width, height)
                game_state = 'play'
            elif game_state == 'play':
                try: next_action = action.popleft()
                except: next_action = None
                snake.move(candy, next_action)
                candy.candy_update(snake)
                world_map.make_lst(snake, candy)
                render(world_map.map)
                sleep(0.1)
                if snake.dead:
                    game_state = 'dead'
            elif game_state == 'dead':
                print('you died')
                sleep(2)
                break   
        quit()