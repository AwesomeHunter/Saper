from vector import Vector
from random import random
from tile_type import TileType


class Board:
    neighbours = [Vector(neighbour) for neighbour in
                  [(1, 1), (1, 0), (0, 1), (-1, -1), (-1, 0), (0, -1), (-1, 1), (1, -1)]]

    def __init__(self, size):
        self.SIZE = self.WIDTH, self.HEIGHT = size.tup()
        self.board = {Vector(x, y): TileType.EM_HID for x in range(self.WIDTH) for y in range(self.HEIGHT)}

    def count_tiles(self, *args):
        return sum([1 for key, val in self.board.items() if val in args])

    def gen_bombs(self, number_of_bombs, mouse_pos):
        not_allowed_positions = [mouse_pos + neighbour for neighbour in self.neighbours] + [mouse_pos]
        while self.count_tiles(TileType.BO_HID) < number_of_bombs:
            x = int(random() * self.WIDTH)
            y = int(random() * self.HEIGHT)
            random_pos = Vector(x, y)
            if random_pos not in not_allowed_positions:
                self.board[random_pos] = TileType.BO_HID

    def count_bombs_at_pos(self, pos):
        return sum([1 for neighbour in self.neighbours
                    if self.board.get(pos + neighbour) in [TileType.BO_HID, TileType.BO_FLA, TileType.BO_VIS]])

    def clicked_empty_tile(self, pos):
        if self.board.get(pos) in [TileType.EM_HID, TileType.EM_FLA]:
            self.board[pos] = TileType.EM_VIS
            if self.count_bombs_at_pos(pos) == 0:
                for neighbour in self.neighbours:
                    self.clicked_empty_tile(neighbour + pos)

    def get_board(self):
        return self.board

    def get_type(self, pos):
        return self.board.get(pos)

    def flag_action(self, pos):
        flag_tile_type = {
            TileType.BO_HID: TileType.BO_FLA,
            TileType.BO_FLA: TileType.BO_HID,
            TileType.EM_HID: TileType.EM_FLA,
            TileType.EM_FLA: TileType.EM_HID,
        }
        self.board[pos] = flag_tile_type.get(self.get_type(pos), self.get_type(pos))

    def replace_type(self, type_to_replace, new_type):
        for pos, tile_type in self.board.items():
            if tile_type == type_to_replace:
                self.board[pos] = new_type
