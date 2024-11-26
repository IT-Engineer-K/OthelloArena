import OthelloLogic
import numpy as np

corners = (0, 0), (0, 7), (7, 0), (7, 7)
close_corners = (0, 1), (1, 1), (1, 0), (0, 6), (1, 6), (1, 7), (6, 0), (6, 1), (7, 1), (6, 7), (6, 6), (7, 6)

def count(board, player):
    return np.sum(np.array(board) == player)

def count_positions(board, player, positions):
    nb_position = 0
    for position in positions:
        if board[position[0]][position[1]] == player:
            nb_position += 1
    return nb_position

weights_list = np.array([[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]])


def gen_evaluates(weights):
    def evaluate(board, player):
        board = np.array(board)
        move = OthelloLogic.getMoves(board, player, 8)
        
        nb_player = count(board, player)
        nb_corners = count_positions(board, player, corners)
        nb_close_corners = count_positions(board, player, close_corners)
        nb_moves = len(move)

        nb_stones = 64 - count(board, 0)

        # 0→1
        time_param = (nb_stones - 4) / 60
        # 1→0
        start_param = 1 - time_param

        values = [nb_corners * time_param, nb_player * time_param, nb_moves * time_param, -nb_close_corners * time_param]
        values += [nb_corners * start_param, nb_player * start_param, nb_moves * start_param, -nb_close_corners * start_param]
        return (np.array(values) * weights).sum()
    return evaluate

# [0.  0.  0.  0.  0.  0.5 0.  0.5]