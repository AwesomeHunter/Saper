from pygame.math import Vector2
from random import random

class Board:
    
    neighbours = [Vector2(neighbour) for neighbour in 
                  [(1, 1), (1, 0), (0, 1), (-1, -1), (-1, 0), (0, -1), (-1, 1), (1, -1)]]

    EM_HID = 0
    BO_HID = 1
    EM_VIS = 2
    BO_VIS = 3
    EM_FLA = 4
    BO_FLA = 5

    def __init__(self, size):
        self.size = size
        self.board = [[self.EM_HID] * int(self.size.x) for i in range(int(self.size.y))]

    def count_tiles(self, *args):
        return sum([1 for row in self.board for val in row if val in args])
    
    def gen_rand_position(self):
        x = int(random() * self.size.x)
        y = int(random() * self.size.y)
        return Vector2(x, y)
    
    def is_correct_position(self, position):
        return 0 <= position.x < self.size.x and 0 <= position.y < self.size.y
    
    def get_at_position(self, position):
        if self.is_correct_position(position):
            return self.board[int(position.y)][int(position.x)]
        return None
    
    def set_at_position(self, position, value):
        if self.is_correct_position(position):
            self.board[int(position.y)][int(position.x)] = value
        
    def gen_bombs(self, number_of_bombs, mouse_pos):
        not_allowed_positions = [mouse_pos + neighbour for neighbour in self.neighbours] + [mouse_pos]
        while self.count_tiles(self.BO_HID) < number_of_bombs:
            random_pos = self.gen_rand_position()
            if random_pos not in not_allowed_positions:
                self.set_at_position(random_pos, self.BO_HID)

    def count_bombs_at_pos(self, pos):
        return sum([1 for neighbour in self.neighbours
                    if self.get_at_position(pos + neighbour) in [self.BO_HID, self.BO_FLA, self.BO_VIS]])

    def clicked_empty_tile(self, position):
        if self.get_at_position(position) in [self.EM_HID, self.EM_FLA]:
            self.set_at_position(position, self.EM_VIS)
            if self.count_bombs_at_pos(position) == 0:
                for neighbour in self.neighbours:
                    self.clicked_empty_tile(neighbour + position)
                    
    def flag_action(self, position):
        flag_tile_type = {
            self.BO_HID: self.BO_FLA,
            self.BO_FLA: self.BO_HID,
            self.EM_HID: self.EM_FLA,
            self.EM_FLA: self.EM_HID,
        }
        old_value = self.get_at_position(position)
        new_value = flag_tile_type.get(old_value, old_value)
        self.set_at_position(position, new_value)

    def get_board(self):
        board = []
        for y in range(int(self.size.y)):
            for x in range(int(self.size.x)):
                position = Vector2(x, y)
                board.append((position, self.get_at_position(position)))
        return board

    def replace_type(self, type_to_replace, new_type):
        for val in self.get_board():
            if val[1] == type_to_replace:
                self.set_at_position(val[0], new_type)
