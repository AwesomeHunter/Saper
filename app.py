import pygame as pg
from pygame.math import Vector2
from board import Board


class App:

    TILE_SIZE = Vector2(32, 32)
    
    TILE_COLOR = {
        Board.EM_HID: pg.Color("gray79"),
        Board.BO_HID: pg.Color("gray79"),
        Board.EM_VIS: pg.Color("gray93"),
        Board.BO_VIS: pg.Color("red"),
        Board.EM_FLA: pg.Color("green"),
        Board.BO_FLA: pg.Color("green"),
    }

    def __init__(self, size, bombs):
        self.size = Vector2(size)
        self.bombs = bombs
        self.running = True
        self.bomb_clicked = False
        self.board = Board(self.size)
        pg.init()
        self.font = pg.font.SysFont("Consolas", int(min(self.TILE_SIZE.x, self.TILE_SIZE.y) * 2 // 3))
        screen_size = self.size.elementwise() * self.TILE_SIZE
        self.screen = pg.display.set_mode((int(screen_size.x), int(screen_size.y)))

    def draw_bomb_count(self, tile_data, box):
        cnt_bombs = self.board.count_bombs_at_pos(tile_data[0])
        if cnt_bombs > 0 and tile_data[1] == self.board.EM_VIS:
            label = self.font.render(str(cnt_bombs), True, pg.Color("blue"))
            text_rect = label.get_rect(center=box.center)
            self.screen.blit(label, text_rect)

    def get_tile_rect(self, tile_data):
        shift = Vector2(1, 1)
        tile_position = tile_data[0].elementwise() * self.TILE_SIZE + shift
        tile_size = self.TILE_SIZE - shift * 2
        return pg.Rect(tile_position, tile_size)

    def draw_board(self):
        for tile in self.board.get_board():
            tile_color = self.TILE_COLOR.get(tile[1], None)
            tile_rect = self.get_tile_rect(tile)
            pg.draw.rect(self.screen, tile_color, tile_rect)
            self.draw_bomb_count(tile, tile_rect)
            
    def set_game_caption(self):
        bombs_left = self.bombs - self.board.count_tiles(self.board.BO_FLA, self.board.EM_FLA)
        caption = "SAPER: {} bombs".format(bombs_left)
        pg.display.set_caption(caption)

    def is_winner(self):
        if self.board.count_tiles(self.board.EM_VIS) == self.size.x * self.size.y - self.bombs:
            self.board.replace_type(self.board.BO_HID, self.board.BO_FLA)

    def handle_mouse(self, event):
        mouse_pos = pg.mouse.get_pos()
        mouse_rect_pos = Vector2(mouse_pos).elementwise() // self.TILE_SIZE
        if event.button == 1:
            if self.board.get_at_position(mouse_rect_pos) == self.board.EM_HID:
                if self.board.count_tiles(self.board.BO_HID, self.board.BO_FLA) == 0:
                    self.board.gen_bombs(self.bombs, mouse_rect_pos)
                self.board.clicked_empty_tile(mouse_rect_pos)
            elif self.board.get_at_position(mouse_rect_pos) == self.board.BO_HID:
                self.board.replace_type(self.board.BO_HID, self.board.BO_VIS)
                self.bomb_clicked = True
        elif event.button == 3:
            self.board.flag_action(mouse_rect_pos)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN and self.bomb_clicked is False:
                self.handle_mouse(event)

    def run(self):
        while self.running:
            self.handle_events()
            self.screen.fill(pg.Color("gray70"))
            self.is_winner()
            self.draw_board()
            self.set_game_caption()
            pg.display.flip()