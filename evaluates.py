import OthelloLogic
import numpy as np

def nb_move(board, player):
    move = OthelloLogic.getMoves(board, player, 8)
    return len(move)

def count(board, player):
    return sum(sum(row) for row in board) * player

def evaluate1(board, player):
    # 置ける数
    return nb_move(board, player)

def evaluate2(board, player):
    # -相手が置ける数
    return -nb_move(board, -player)

def evaluate3(board, player):
    # 置ける数の差
    return nb_move(board, player) - nb_move(board, -player)

def evaluate4(board, player):
    # コマ数
    return count(board, player)

def evaluate5(board, player):
    # 置ける数+コマ数
    return nb_move(board, player) + count(board, player)
    
def evaluate6(board, player):
    # 置ける数+コマ数-相手のコマ数
    return nb_move(board, player) + count(board, player) - count(board, -player)

def evaluate7(board, player):
    # -相手のコマ数
    return -count(board, -player)

def evaluate8(board, player):
    nb_empty = count(board, 0)
    if nb_empty % 2:
        # -相手が置ける数
        value = -nb_move(board, -player)
    else:
        # コマ数
        value = count(board, player)
    return value

def evaluate9(board, player):
    # 置ける数-相手のコマ数
    return nb_move(board, player) - count(board, -player)

def evaluate10(board, player):
    # 相手のコマ数
    nb_player = count(board, -player)
    # 相手が置ける数
    nb_opponent_moves = nb_move(board, -player)
    
    # 序盤
    if nb_player < nb_opponent_moves:
        return -nb_opponent_moves
    # 終盤
    return -nb_player

def evaluate11(board, player):
    # コマ数
    nb_player = count(board, player)
    # 置ける数
    nb_moves = nb_move(board, player)
    
    # 序盤
    if nb_player < nb_moves:
        return nb_moves
    # 終盤
    return nb_player

def evaluate12(board, player):
    # 置ける数*コマ数
    return nb_move(board, player) * count(board, player)

def evaluate13(board, player):
    # 置ける数*コマ数-相手のコマ数
    return nb_move(board, player) * count(board, player) - count(board, -player)

def evaluate14(board, player):
    # バラバラ
    np_board_my_stone = np.array(np.array(board) == 0, dtype=int)
    a = np_board_my_stone[:-1] - np_board_my_stone[1:]
    b = np_board_my_stone.T[:-1] - np_board_my_stone.T[1:]
    return -a.sum()-b.sum()


def evaluate15(board, player):
    nb_empty = count(board, 0)
    if nb_empty % 2:
        # コマ数
        value = count(board, player)
    else:
        # -相手が置ける数
        value = -nb_move(board, -player)
    return value

def evaluate16(board, player):
    nb_empty = count(board, 0)
    if nb_empty % 2:
        # 置ける数
        value = nb_move(board, player)
    else:
        # -相手が置ける数
        value = -nb_move(board, -player)
    return value

# 評価関数リスト
evaluate_funcs = [evaluate1, evaluate2, evaluate3, evaluate4, evaluate5, evaluate6, evaluate7, evaluate8, evaluate9, evaluate10, evaluate11, evaluate12, evaluate13, evaluate14, evaluate15, evaluate16]
# evaluate_funcs = [evaluate1, evaluate2, evaluate3, evaluate4, evaluate5]

nb_funcs = len(evaluate_funcs)

# 勝敗リスト
win_lose = np.zeros((nb_funcs, nb_funcs))