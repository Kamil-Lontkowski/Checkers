import pygame
from .board import Board
from .constants import BLACK, WHITE, COLORS, SQUARE_SIZE
from .piece import Piece
from minimax.algo import minimax, alfabeta
import random


class Game:
    def __init__(self, win, mode: int, diff: int, white: int, black: int):
        self.selected: Piece | None = None
        self.board = Board()
        self.turn = WHITE if random.choice([0, 1]) == 0 else BLACK
        self.valid_moves: list[list[tuple[int, int]]] = [[]]
        self.win = win
        self.winner = None
        self.mode = mode
        self.diff = diff
        self.white_algo = white
        self.black_algo = black
        self.black_moves = 0
        self.white_moves = 0

    def update(self):
        if self.turn == WHITE:
            if self.mode == 3 or self.mode == 4:
                if self.white_algo == 1:
                    move = minimax(self.board, self.diff, WHITE)
                else:
                    move = alfabeta(self.board, self.diff, WHITE)
                self.selected = self.board.get_piece(move[0][0], move[0][1])
                ate = True if len(move[1]) > 1 else False
                self.board.move(self.selected, move[1][-1][0], move[1][-1][1], ate, move[1])
                self.change_turn()
        else:
            if self.mode == 2 or self.mode == 3:
                if self.black_algo == 1:
                    move = minimax(self.board, self.diff, BLACK, False)
                else:
                    move = alfabeta(self.board, self.diff, BLACK)
                self.selected = self.board.get_piece(move[0][0], move[0][1])
                ate = True if len(move[1]) > 1 else False
                self.board.move(self.selected, move[1][-1][0], move[1][-1][1], ate, move[1])
                self.change_turn()
            if self.mode == 4:
                moves = self.board.get_all_moves(BLACK)
                move = random.choice(list(moves.items()))
                self.selected = self.board.get_piece(move[0][0], move[0][1])
                m = random.choice(move[1])
                ate = True if len(m) > 1 else False
                self.board.move(self.selected, m[-1][0], m[-1][1], ate, m)
                self.change_turn()
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = []

    def select(self, row, col):
        if self.selected:
            if (self.selected.row, self.selected.col) == (row, col):
                self.selected = None
                self.valid_moves = [[]]
                return False
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.valid_moves = [[]]
                self.select(row, col)
            else:
                self.change_turn()

        else:
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_piece_moves(piece)
                if len(self.valid_moves[0]) != self.board.best_move_size:
                    self.valid_moves = [[]]
                return True
            else:
                self.valid_moves = [[]]
        return False

    def _move(self, row, col) -> bool:
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0:
            for move in self.valid_moves:
                if (row, col) in move:
                    if len(move) > 1:
                        self.board.move(self.selected, move[-1][0], move[-1][1], True, move)
                    else:
                        self.board.move(self.selected, move[-1][0], move[-1][1])
                    self.selected = None
                    self.valid_moves = []
                    break
        else:
            return False
        return True

    def change_turn(self):
        if self.turn == BLACK:
            self.black_moves += 1
            self.turn = WHITE
        elif self.turn == WHITE:
            self.turn = BLACK
            self.white_moves += 1
        self.who_won()

    def draw_valid_moves(self, moves: list[list[tuple[int, int]]]):
        i = 0
        for move in moves:
            for field in move:
                row, col = field
                pygame.draw.circle(self.win, COLORS[i % 4],
                                   (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2),
                                   SQUARE_SIZE // 5)

            i += 1

    def who_won(self):
        if self.board.black_left == 0:
            self.winner = 'WHITE'
        elif self.board.white_left == 0:
            self.winner = 'BLACK'
        elif len(self.board.get_all_moves(self.turn)) == 0:
            if self.turn == BLACK:
                self.winner = 'WHITE'
            else:
                self.winner = 'BLACK'
