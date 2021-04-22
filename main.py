import pygame
from vector import Vector
from tile_type import TileType
from board import Board
import color


class Game:

    TILE_SIZE = 26

    def __init__(self, size, bombs):
        self.WIDTH, self.HEIGHT = size
        self.SIZE = Vector(size)
        self.SIZE_PIXELS = self.SIZE * self.TILE_SIZE
        self.BOMBS_NUMBER = bombs
        self.running = False
        self.board = Board(self.SIZE)
        pygame.init()
        self.font = pygame.font.SysFont("Consolas", self.TILE_SIZE // 2)
        self.screen = pygame.display.set_mode(self.SIZE_PIXELS.tup())

    def draw_board(self):
        for pos, tile_type in self.board.get_board().items():
            tile_pos = pos * self.TILE_SIZE + 1
            tile_size = self.TILE_SIZE - 2, self.TILE_SIZE - 2
            tile_color = tile_type.value
            tile_rect = pygame.Rect(tile_pos.tup(), tile_size)
            pygame.draw.rect(self.screen, tile_color, tile_rect)

    def draw_bomb_count(self):
        for pos, tile_type in self.board.get_board().items():
            cnt_bombs = self.board.count_bombs_at_pos(pos)
            if cnt_bombs > 0 and tile_type == TileType.EM_VIS:
                label = self.font.render(str(cnt_bombs), 1, color.BLUE)
                label_pos = pos * self.TILE_SIZE
                self.screen.blit(label, label_pos.tup())

    def set_game_caption(self):
        bombs_left = self.BOMBS_NUMBER - self.board.count_tiles(TileType.BO_FLA, TileType.EM_FLA)
        caption = "SAPER: {} bombs".format(bombs_left)
        pygame.display.set_caption(caption)

    def is_winner(self):
        if self.board.count_tiles(TileType.BO_FLA) == self.BOMBS_NUMBER and self.board.count_tiles(TileType.EM_FLA) == 0:
            self.board.replace_type(TileType.EM_HID, TileType.EM_VIS)
            self.running = False
        elif self.board.count_tiles(TileType.EM_VIS) == self.WIDTH * self.HEIGHT - self.BOMBS_NUMBER:
            self.board.replace_type(TileType.BO_HID, TileType.BO_FLA)
            self.running = False

    def handle_mouse(self, event):
        mouse_pos = pygame.mouse.get_pos()
        mouse_rect_pos = Vector(mouse_pos) // self.TILE_SIZE
        if event.button == 1:
            if self.board.get_type(mouse_rect_pos) == TileType.EM_HID:
                if self.board.count_tiles(TileType.BO_HID) == 0:
                    self.board.gen_bombs(self.BOMBS_NUMBER, mouse_rect_pos)
                self.board.clicked_empty_tile(mouse_rect_pos)
            elif self.board.get_type(mouse_rect_pos) == TileType.BO_HID:
                self.board.replace_type(TileType.BO_HID, TileType.BO_VIS)
                self.running = False
        elif event.button == 3:
            self.board.flag_action(mouse_rect_pos)

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse(event)
            self.screen.fill(color.DARK_GREY)
            self.is_winner()
            self.draw_board()
            self.draw_bomb_count()
            self.set_game_caption()
            pygame.display.flip()


if __name__ == "__main__":
    game_size = 18, 14
    game = Game(game_size, 40)
    game.run()
