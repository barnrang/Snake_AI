import os
import sys
import platform
from time import sleep

import numpy as np
#from pynput.keyboard import Key, Controller, Listener
#import snake

from game.snake import Snake
from game.world_map import Map
from game.candy import Candy

if platform.system() == 'Windows':
    def clear(): return os.system('cls')
elif platform.system() == 'Darwin':
    def clear(): return os.system('clear')


class SnakeEnvironment(object):
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self.game_state = 'init'
        self.action_list = ['u','d','l','r',None]

        self.snake = Snake(width, height)
        self.candy = Candy(width, height)

        self.world_map = Map(width, height)
        self.world_map.make_lst(self.snake, self.candy)

        self.done = False

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def _replace_item_map(self, x):
        if x in 'v^><':
            return 0
        elif x == '@':
            return 1
        elif x == '*':
            return 2
        else:
            return 3

    @property
    def state(self):
        '''
        Return state from raw map
        wall - 0
        snake - 1
        candy - 2
        '''
        state_map = self.world_map.map.copy()
        for i in range(self.height):
            state_map[i] = list(map(self._replace_item_map, state_map[i]))
        return np.array(state_map)

    def reset(self):
        '''
        Reset state (e.g. Game over)
        and return init state
        '''
        self.game_state = 'init'

        self.snake = Snake(self.width, self.height)
        self.candy = Candy(self.width, self.height)

        self.world_map = Map(self.width, self.height)
        self.world_map.make_lst(self.snake, self.candy)
        self.done = False
        return self.state

    def step(self, action):
        '''
        Input:
        Int - action

        Output:
        Float - reward

        Move an act, return state, reward & done
        '''
        self.snake.move(self.candy, self.action_list[action])
        self.candy.candy_update(self.snake)
        self.world_map.make_lst(self.snake, self.candy)

        if self.candy.candy_eaten:
            return self.state, 5, self.snake.dead, None
        
        if self.snake.dead:
            self.done = True
            # The training process will negative it
            return self.state, 5, self.snake.dead, None

        return self.state, 0, self.snake.dead, None

    
    def render(self):
        '''
        Render game from map
        '''
        clear()
        for stri in self.world_map.map:
            for char in stri:
                print(char, end='')
            print('')

if __name__ == "__main__":
    snake_env = SnakeEnvironment(30,10)
    import random
    reward = 0
    action_list = ''
    while not snake_env.done:
        act = random.choice(range(5))
        action_list += snake_env.action_list[act] if snake_env.action_list[act] is not None else ''
        reward += snake_env.act(act)
        snake_env.render()
        print('reward: ', reward)
        print('acted: ', action_list)
        sleep(1)
    
