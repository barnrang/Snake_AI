from queue import deque

class Snake(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        born_position = (int)(height / 2)
        born_head = (int)(width / 2)
        born_length = (int)(width / 4)

        #print([(born_position, x) for x in range(born_head, bornborn_length)])
        self.body = deque([(born_position, x) for x in range(born_head, born_head + born_length)])
        self.direct = 'l'
        self.board_state = [[0 for _ in range(width)] for __ in range(height)]
        for body_part in self.body:
            self.board_state[body_part[0]][body_part[1]] = 1
        for i in range(self.width):
            self.board_state[0][i] = 1
            self.board_state[-1][i] = 1
        for i in range(self.height):
            self.board_state[i][0] = 1
            self.board_state[i][-1] = 1

        self.dead = False

    def move(self, action=None):
        '''
        Update the snake body for an action
        '''
        if action is not None:
            self.direct = action

        current_head = self.body[0]
        catch_food = False
        if self.direct == 'u':
            next_head = (current_head[0] - 1, current_head[1])
        if self.direct == 'd':
            next_head = (current_head[0] + 1, current_head[1])
        if self.direct == 'l':
            next_head = (current_head[0], current_head[1] - 1)
        if self.direct == 'r':
            next_head = (current_head[0], current_head[1] + 1)
        
        if self.board_state[next_head[0]][next_head[1]]:
            self.dead = True

        self.body.appendleft(next_head)
        if not catch_food:
            self.body.pop()

    