import OthelloLogic
import numpy as np

def nb_move(board, player):
    move = OthelloLogic.getMoves(board, player, 8)
    return len(move)

def count(board, player):
    return np.sum(np.array(board) == player)

weights_list = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [1, 1, 1, 1], [1, 1, 0, 0]])

def gen_evaluates(weights):
    def evaluate(board, player):
        nb_player = count(board, 1)
        nb_opponents = count(board, -1)
        nb_moves = nb_move(board, player)
        nb_opponents_moves = nb_move(board, -player)
        values = np.array([nb_player, -nb_opponents, nb_moves, -nb_opponents_moves])
        return (values * weights).sum()
    return evaluate

def evaluate1(board, player):
    nb_player = count(board, 1)
    nb_opponents = count(board, -1)
    nb_moves = nb_move(board, player)
    nb_opponents_moves = nb_move(board, -player)
    values = np.array([nb_player, -nb_opponents, nb_moves, -nb_opponents_moves])
    return (values * weights[0]).sum()

# 評価関数リスト
evaluate_funcs = [gen_evaluates(weights) for weights in weights_list]
# evaluate_funcs = [evaluate1, evaluate2, evaluate3, evaluate4, evaluate5]

nb_funcs = len(evaluate_funcs)

# 勝敗リスト
win_lose = np.zeros((nb_funcs, nb_funcs))