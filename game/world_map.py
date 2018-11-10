class Map(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = None
        
        self._reset_map()

    def _reset_map(self):
        self.map = [[' ' for __ in range(self.width)] for _ in range(self.height)]
        for i in range(self.width):
            self.map[0][i] = '>'
            self.map[-1][i] = '<'
        for i in range(self.height):
            self.map[i][0] = '^'
            self.map[i][-1] = 'v'

    def make_lst(self, snake):
        self._reset_map()
        for coor in snake.body:
            self.map[coor[0]][coor[1]] = '@'