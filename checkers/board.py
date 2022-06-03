import pygame
from pygame.surface import SurfaceType, Surface
from copy import deepcopy

from .constants import BLACK, ROWS, YELLOW, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

WIN = Surface | SurfaceType


class Board:
    def __init__(self):
        self.board: list[list[Piece | int]] = []
        self.white_left = self.black_left = 0
        self.white_kings = self.black_kings = 0
        self.create_board()
        self.best_move_size = 0
        self.count_pieces()

    @staticmethod
    def draw_cubes(win: WIN):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, YELLOW,
                                 (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 2:
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row > 5:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def move(self, piece, row, col, did_eat=False, move: list[tuple[int, int]] = None):
        if move is None:
            move = []
        for row, col in move:
            if self.get_piece(row, col) != 0:
                self.board[row][col] = 0
        self.board[piece.row][piece.col], self.board[row][col] = \
            self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if (row == ROWS - 1 or row == 0) and not did_eat:
            piece.make_king()
            if piece.color == WHITE and not piece.king:
                self.white_kings += 1
            if piece.color == BLACK and not piece.king:
                self.black_kings += 1
        self.count_pieces()

    def get_piece(self, row, col):
        return self.board[row][col]

    def draw(self, win: WIN):
        self.draw_cubes(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def get_piece_moves(self, piece: Piece) -> list[list[tuple[int, int]]]:
        row, col = piece.row, piece.col
        moves = []
        killing_moves = []
        if piece.king:
            for i in range(1, min(row, col) + 1):
                if self.get_piece(row - i, col - i) != 0:
                    if self.get_piece(row - i, col - i).color != piece.color:
                        killing_moves.append((row - i, col - i))
                    break
                else:
                    moves.append([(row - i, col - i)])

            for i in range(1, min(row, COLS - col - 1) + 1):
                if self.get_piece(row - i, col + i) != 0:
                    if self.get_piece(row - i, col + i).color != piece.color:
                        killing_moves.append((row - i, col + i))
                    break
                else:
                    moves.append([(row - i, col + i)])

            for i in range(1, min(ROWS - row - 1, col) + 1):
                if self.get_piece(row + i, col - i) != 0:
                    if self.get_piece(row + i, col - i).color != piece.color:
                        killing_moves.append((row + i, col - i))
                    break
                else:
                    moves.append([(row + i, col - i)])

            for i in range(1, min(ROWS - row - 1, COLS - col - 1) + 1):
                if self.get_piece(row + i, col + i) != 0:
                    if self.get_piece(row + i, col + i).color != piece.color:
                        killing_moves.append((row + i, col + i))
                    break
                else:
                    moves.append([(row + i, col + i)])
        else:
            if piece.color == BLACK:
                if row == ROWS - 1:
                    moves = [[]]
                else:
                    if col != 0 and self.get_piece(row + 1, col - 1) == 0:
                        moves.append([(row + 1, col - 1)])
                    if col != COLS - 1 and self.get_piece(row + 1, col + 1) == 0:
                        moves.append([(row + 1, col + 1)])
            else:
                if row == 0:
                    moves = [[]]
                else:
                    if col != 0 and self.get_piece(row - 1, col - 1) == 0:
                        moves.append([(row - 1, col - 1)])
                    if col != COLS - 1 and self.get_piece(row - 1, col + 1) == 0:
                        moves.append([(row - 1, col + 1)])

        possible_kills = killing_moves + Board._get_moves_around(row, col, deepcopy(self.board), piece.color)
        poss = []
        for k in possible_kills:
            poss.append([k])
        if len(possible_kills) == 0:
            if moves:
                return moves
            else:
                return [[]]
        else:
            i = len(poss)
            for a in range(i):
                kill = poss[a]
                k_row, k_col = kill[0]
                Board._get_kills(k_row, k_col, deepcopy(self.board), piece.color, row, col, poss, kill)
            maks = 0
            for move in poss:
                if len(move) > maks:
                    maks = len(move)
            result = []
            for move in poss:
                if len(move) == maks:
                    result.append(move)
            condition = False
            for move in result:
                if len(move) > 0:
                    condition = True
            if condition:
                return result
            else:
                return moves

    @staticmethod
    def _get_moves_around(row, col, board: list[list[Piece | int]], color) -> list[tuple[int, int]]:
        all_moves: list[tuple[int, int]] = [(row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1),
                                            (row + 1, col + 1)]
        all_moves = [i for i in all_moves if not (i[0] < 0 or i[0] >= ROWS or i[1] < 0 or i[1] >= COLS)]
        possible_kills = [i for i in all_moves if board[i[0]][i[1]] and board[i[0]][i[1]].color != color]
        return possible_kills

    @staticmethod
    def _get_kills(row, col, board: list[list[Piece | int]], color, start_r, start_c, all_moves, curr_move):
        dir_row, dir_col = start_r - row, start_c - col
        new_row: int
        new_col: int
        if dir_row > 0 and dir_col < 0:
            # Do gory w prawo
            new_row = row - 1
            new_col = col + 1
            if new_row < 0 or new_col > COLS - 1:
                curr_move.pop()
                return
            elif board[new_row][new_col] != 0:
                curr_move.pop()
                return
        elif dir_row > 0 and dir_col > 0:
            # Do gory w lewo
            new_row = row - 1
            new_col = col - 1
            if new_row < 0 or new_col < 0:
                curr_move.pop()
                return
            elif board[new_row][new_col] != 0:
                curr_move.pop()
                return
        elif dir_row < 0 and dir_col < 0:
            # W dol w prawo
            new_row = row + 1
            new_col = col + 1
            if new_row > ROWS - 1 or new_col > COLS - 1:
                curr_move.pop()
                return
            elif board[new_row][new_col] != 0:
                curr_move.pop()
                return
        elif dir_row < 0 and dir_col > 0:
            # W dol w lewo
            new_row = row + 1
            new_col = col - 1
            if new_row > ROWS - 1 or new_col < 0:
                curr_move.pop()
                return
            elif board[new_row][new_col] != 0:
                curr_move.pop()
                return
        else:
            curr_move.pop()
            return

        curr_move.append((new_row, new_col))
        new_board = Board.kill(board, curr_move, board[start_r][start_c])
        possible_next_kills = Board._get_moves_around(new_row, new_col, new_board, color)

        if len(possible_next_kills) == 1:
            curr_move.append((possible_next_kills[0][0], possible_next_kills[0][1]))
            Board._get_kills(possible_next_kills[0][0], possible_next_kills[0][1], new_board, color, new_row, new_col,
                             all_moves, curr_move)
        elif len(possible_next_kills) > 1:
            curr_move.append((possible_next_kills[0][0], possible_next_kills[0][1]))
            curr = deepcopy(curr_move)
            curr.pop()
            Board._get_kills(possible_next_kills[0][0], possible_next_kills[0][1], new_board, color, new_row, new_col,
                             all_moves, curr_move)
            for i in range(1, len(possible_next_kills)):
                cp_curr = deepcopy(curr)
                cp_curr.append((possible_next_kills[i][0], possible_next_kills[i][1]))
                all_moves.append(cp_curr)
                Board._get_kills(possible_next_kills[i][0], possible_next_kills[i][1], new_board, color, new_row,
                                 new_col,
                                 all_moves, cp_curr)
        else:
            return

    def __repr__(self):
        s = '=' * (11 * 13 - 17) + '\n|'
        for row in self.board:
            for col in row:
                s += f'{col.__repr__():^13}|' + '\t'
            s += '\n' + '=' * (11 * 13 - 17) + '\n|'
        return s[:-1]

    @staticmethod
    def kill(board: list[list[Piece | int]], move: list[tuple[int, int]], piece: Piece) -> list[list[Piece | int]]:
        new_board = deepcopy(board)
        for row, col in move:
            if new_board[row][col] != 0:
                new_board[row][col] = 0
        row, col = move[-1]
        new_board[piece.row][piece.col] = 0
        new_piece = deepcopy(piece)
        new_piece.row, new_piece.col = row, col
        new_board[row][col] = new_piece
        if len(move) == 1:
            if piece.color == WHITE and new_piece.row == 0:
                new_piece.make_king()
            if piece.color == BLACK and new_piece.row == ROWS - 1:
                new_piece.make_king()
        return new_board

    def get_all_moves(self, color: tuple[int, int, int]) -> dict[tuple[int, int], list[list[tuple[int, int]]]]:
        d = {}
        for row in self.board:
            for field in row:
                if field != 0:
                    if field.color == color:
                        d[(field.row, field.col)] = self.get_piece_moves(field)
        maks = 0
        new_d = {}
        for k in d:
            if len(d[k]) != 0:
                if len(d[k][0]) > maks:
                    maks = len(d[k][0])

        for k in d:
            if len(d[k]) != 0:
                if len(d[k][0]) == maks:
                    new_d[k] = d[k]
        self.best_move_size = maks
        for k in new_d:
            if len(new_d[k][0]) == 0:
                return {}
        return new_d

    def count_pieces(self):
        self.white_left = self.black_left = 0
        for row in self.board:
            for field in row:
                if field != 0:
                    if field.color == WHITE:
                        self.white_left += 1
                    else:
                        self.black_left += 1

    @staticmethod
    def get_score_draft5ga(board: list[list[Piece | int]]) -> int:
        score = 0
        for row in board:
            for field in row:
                if field != 0:
                    to_add = 3
                    if field.king:
                        to_add = 5
                    if field.color == WHITE:
                        score += to_add
                    else:
                        score -= to_add
        return score

    @staticmethod
    def get_score_color(board: list[list[Piece | int]], color: tuple[int, int, int]) -> int:
        score = Board.get_score_draft5ga(board)
        if color == WHITE:
            return score
        else:
            return score * (-1)

    def winner(self, color: tuple[int, int, int]):
        self.count_pieces()
        if self.black_left == 0:
            return 'WHITE'
        elif self.white_left == 0:
            return 'BLACK'
        elif len(self.get_all_moves(color)) == 0:
            if color == BLACK:
                return 'WHITE'
            else:
                return 'BLACK'
        else:
            return None
