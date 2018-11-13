from collections import deque
import random
import sys

sys.path.append('../../')
sys.path.append('game/')

import numpy as np

from base_network import BaseNetwork
from keras.models import load_model
from snake_env import SnakeEnvironment

EP = 100000

class Config:
    height = 20
    width = 30
    action_num = 5
    lr = 3e-5
    eps = 1.
    eps_min = 0.1
    eps_decay = 0.999
    gamma = 0.95

class DQAgent():
    def __init__(self, config):
        self.config = config
        self.memory = deque(maxlen=20000)

        # model
        self.q = BaseNetwork(config.height, config.width, config.action_num, config) 
        # target model
        self.qt = BaseNetwork(config.height, config.width, config.action_num, config)


    def act(self, state):
        if random.uniform(0, 1) < self.config.eps:
            return random.randrange(self.config.action_num)
        else:
            return np.argmax(self.q.model.predict(self.rescale_color(state))[0])

    def replay(self, batch_size):

        if batch_size > len(self.memory):
            return
        minibatch = random.sample(self.memory, batch_size)
        states = []
        targets = []
        for state, action, reward, next_state, done in minibatch:
            #print(state, action, reward, next_state, done)
            inpu = self.rescale_color(state)
            target = self.q.model.predict(inpu)
            if done:
                target[0][action] = reward
            else:
                inp = self.rescale_color(next_state)
                t = self.qt.model.predict(inp)[0]
                target[0][action] = reward + self.config.gamma * np.max(t)
            self.q.model.fit(inpu, target, epochs=1, verbose=0)
        if self.config.eps> self.config.eps_min:
            self.config.eps *= self.config.eps_decay

    def rescale_color(self, state):
        return state / 3.
        

    def copy_param(self):
        self.qt.model.set_weights(self.q.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def save_model(self, path):
        self.q.model.save(path)
    
    def load_model(self, path):
        self.q.model = load_model(path)

def train():
    config = Config()
    env = SnakeEnvironment(config.width, config.height)
    agent = DQAgent(config)

    done = False
    batch_size = 32

    agent.copy_param()

    for i in range(EP):
        state = env.reset()
        
        state = np.expand_dims(state, axis=0)
        state = np.stack([state for _ in range(2)], axis=-1)
        #print(state.shape)
        done = False
        point = 0
        for t in range(5000):
            action = agent.act(state)
            tmp_state, reward, done = env.act(action)

            next_state = np.roll(state, -1, axis=-1)
            next_state[:,:,:,-1] = tmp_state

            point += reward

            agent.remember(state, action, reward, next_state, done)
            state = next_state.copy()
            if done:
                print('episode {}/{}, score: {}'.format(i, EP, point))

                # Print counted frames
                print(t)
                break
            
            agent.replay(batch_size)
        if i % 10 == 0:
            agent.copy_param()
        if i % 100 == 0:
            agent.save_model('model/snake.h5')


if __name__ == "__main__":
    train()
