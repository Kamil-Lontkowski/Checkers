import pygame.draw
from pygame.surface import SurfaceType, Surface

from .constants import YELLOW, CROWN, SQUARE_SIZE, PADDING, BORDER, GREY, BLACK

WIN = Surface | SurfaceType


class Piece:
    def __init__(self, row: int, col: int, color: tuple[int, int, int]):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        if self.color == YELLOW:
            self.direction = -1
        else:
            self.direction = 1

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def draw(self, win: WIN):
        radius = SQUARE_SIZE // 2 - PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + BORDER)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def __repr__(self):
        if self.color == BLACK:
            if self.king:
                return f"BlackK({self.row}, {self.col})"
            else:
                return f"Black({self.row}, {self.col})"
        else:
            if self.king:
                return f"WhiteK({self.row}, {self.col})"
            else:
                return f"White({self.row}, {self.col})"
