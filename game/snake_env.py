import os
import sys
import platform
from time import sleep

import numpy as np
from pynput.keyboard import Key, Controller, Listener

from snake import Snake
from world_map import Map
from candy import Candy

class SnakeEnvironment(object):
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def _reset(self):
        '''
        Reset state (e.g. Game over)
        '''
        raise NotImplementedError

    def act(self, action):
        '''
        Move an act, return next state
        '''
        raise NotImplementedError

    
