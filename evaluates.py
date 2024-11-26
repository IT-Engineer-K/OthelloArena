import OthelloLogic
import numpy as np

def nb_move(board, player):
    move = OthelloLogic.getMoves(board, player, 8)
    return len(move)

def count(board, player):
    return np.sum(np.array(board) == player)

def count_corners(board, player):
    nb_corners = 0
    for corner in ((0, 0), (0, 7), (7, 0), (7, 7)):
        if board[corner[0]][corner[1]] == player:
            nb_corners += 1
    return nb_corners

weights_list = np.array([[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]])


def gen_evaluates(weights):
    def evaluate(board, player):
        board = np.array(board)
        
        nb_player = count(board, player)
        nb_corners = count_corners(board, player)
        nb_moves = nb_move(board, player)

        nb_opponents = count(board, -player)
        nb_opponents_corners = count_corners(board, -player)
        nb_opponents_moves = nb_move(board, -player)
        
        nb_stones = nb_player + nb_opponents
        # 0→1
        time_param = (nb_stones - 4) / 60
        # 1→0
        start_param = 1 - time_param

        values = [nb_corners, nb_player, nb_moves, nb_moves*start_param]
        opponents_value = [nb_opponents_corners, nb_opponents, nb_opponents_moves, nb_opponents_moves*time_param]
        return (np.array(values+opponents_value) * weights).sum()
    return evaluate

# [0.  0.  0.  0.  0.  0.5 0.  0.5]