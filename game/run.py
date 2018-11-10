'''
Snake game 
'''
import os
import sys
import platform
from time import sleep

import numpy as np
from pynput.keyboard import Key, Controller, Listener

from snake import Snake
from world_map import Map

if platform.system() == 'Windows':
    def clear(): return os.system('cls')
elif platform.system() == 'Darwin':
    def clear(): return os.system('clear')

def render(str_list):
    clear()
    for stri in str_list:
        for char in stri:
            print(char, end='')
        print('')

if __name__ == "__main__":

    # 'play' 'dead' 'init'
    game_state = 'init'
    while True:
        if game_state == 'init':
            width = 30
            height = 10
            snake = Snake(width, height)
            world_map = Map(width, height)
            game_state = 'play'
        elif game_state == 'play':
            snake.move()
            world_map.make_lst(snake)
            render(world_map.map)
            sleep(0.2)
            if snake.dead:
                game_state = 'dead'
        elif game_state == 'dead':
            print('you died')
            sleep(2)
            break       