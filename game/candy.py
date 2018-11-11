import numpy as np

class Candy(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.candy_eaten = False
        self.current_candy = None

    def _random_candy(self, snake):
        available = np.argwhere(snake.board_state == 0)
        num_avail = len(available)
        chosen = np.random.choice(list(range(num_avail)))

        self.current_candy = available[chosen]

    def candy_update(self, snake):
        self.candy_eaten = False
        current_head = snake.body[0]
        if self.current_candy is None:
            self._random_candy(snake)
        elif (self.current_candy[0] == current_head[0]) and \
            (self.current_candy[1] == current_head[1]):
            self.candy_eaten = True
            self._random_candy(snake)