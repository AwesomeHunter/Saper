from pygame.math import Vector2
from random import random
from tile_type import TileType


class Board:
    neighbours = [Vector2(neighbour) for neighbour in
                  [(1, 1), (1, 0), (0, 1), (-1, -1), (-1, 0), (0, -1), (-1, 1), (1, -1)]]

    def __init__(self, size):
        self.size = size
        self.board = {(x, y): TileType.EM_HID for x in range(int(self.size.x)) for y in range(int(self.size.y))}

    def count_tiles(self, *args):
        return sum([1 for key, val in self.board.items() if val in args])
    
    def gen_rand_position(self):
        x = int(random() * self.size.x)
        y = int(random() * self.size.y)
        return Vector2(x, y)
        
    def gen_bombs(self, number_of_bombs, mouse_pos):
        not_allowed_positions = [mouse_pos + neighbour for neighbour in self.neighbours] + [mouse_pos]
        while self.count_tiles(TileType.BO_HID) < number_of_bombs:
            random_pos = self.gen_rand_position()
            if random_pos not in not_allowed_positions:
                self.board[tuple(random_pos)] = TileType.BO_HID

    def count_bombs_at_pos(self, pos):
        return sum([1 for neighbour in self.neighbours
                    if self.board.get(tuple(pos + neighbour)) in [TileType.BO_HID, TileType.BO_FLA, TileType.BO_VIS]])

    def clicked_empty_tile(self, pos):
        if self.board.get(tuple(pos)) in [TileType.EM_HID, TileType.EM_FLA]:
            self.board[tuple(pos)] = TileType.EM_VIS
            if self.count_bombs_at_pos(pos) == 0:
                for neighbour in self.neighbours:
                    self.clicked_empty_tile(neighbour + pos)

    def get_board(self):
        return self.board

    def get_type(self, pos):
        return self.board.get(tuple(pos))

    def flag_action(self, pos):
        flag_tile_type = {
            TileType.BO_HID: TileType.BO_FLA,
            TileType.BO_FLA: TileType.BO_HID,
            TileType.EM_HID: TileType.EM_FLA,
            TileType.EM_FLA: TileType.EM_HID,
        }
        self.board[tuple(pos)] = flag_tile_type.get(self.get_type(pos), self.get_type(pos))

    def replace_type(self, type_to_replace, new_type):
        for pos, tile_type in self.board.items():
            if tile_type == type_to_replace:
                self.board[tuple(pos)] = new_type
