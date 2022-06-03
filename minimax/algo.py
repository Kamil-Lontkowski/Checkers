from checkers.board import *


def minimax(board: Board, depth: int, color: tuple[int, int, int], max_player: bool = True, d=0):
    new_board = deepcopy(board)
    if depth == 0 or board.winner(color):
        return board.get_score_draft5ga(board.board)

    all_moves = board.get_all_moves(color)
    branches: list[tuple[tuple[int, int], list[tuple[int, int]], int]] = []
    for k in all_moves:
        for move in all_moves[k]:
            new_board.board = Board.kill(board.board, move, board.get_piece(k[0], k[1]))
            if color == WHITE:
                score = minimax(new_board, depth - 1, BLACK, not max_player, depth)
            else:
                score = minimax(new_board, depth - 1, WHITE, not max_player, depth)
            branches.append((k, move, score))
    if max_player:
        branches.sort(key=lambda x: x[2], reverse=True)
        if depth < d:
            return branches[0][2]
        else:
            return branches[0]
    else:
        branches.sort(key=lambda x: x[2])
        if depth < d:
            return branches[0][2]
        else:
            return branches[0]


def alfabeta(board: Board, depth: int, color: tuple[int, int, int], max_player: bool = True, d=0, alfa=float('-inf'),
             beta=float('inf')):
    new_board = deepcopy(board)
    if depth == 0 or board.winner(color):
        return board.get_score_draft5ga(board.board)

    all_moves = board.get_all_moves(color)
    branches: list[tuple[tuple[int, int], list[tuple[int, int]], int]] = []
    for k in all_moves:
        for move in all_moves[k]:
            new_board.board = Board.kill(board.board, move, board.get_piece(k[0], k[1]))
            if color == WHITE:
                score = alfabeta(new_board, depth - 1, BLACK, not max_player, depth, alfa, beta)
            else:
                score = alfabeta(new_board, depth - 1, WHITE, not max_player, depth, alfa, beta)
            if score > alfa and max_player:
                alfa = score
            if score < beta and not max_player:
                beta = score
            branches.append((k, move, score))
            if score < alfa and not max_player:
                break
            if score > beta and max_player:
                break
        if score < alfa and not max_player:
            break
        if score > beta and max_player:
            break

    if max_player:
        branches.sort(key=lambda x: x[2], reverse=True)
        if depth < d:
            return branches[0][2]
        else:
            return branches[0]
    else:
        branches.sort(key=lambda x: x[2])
        if depth < d:
            return branches[0][2]
        else:
            return branches[0]
