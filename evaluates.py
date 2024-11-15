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
    # ひっくり返せる数の差
    return nb_move(board, player) - nb_move(board, -player)

def evaluate4(board, player):
    # コマ数
    return count(board, player)

def evaluate5(board, player):
    # ひっくり返せる数+コマ数
    return nb_move(board, player) + count(board, player)
    
def evaluate6(board, player):
    # ひっくり返せる数+コマ数-相手のコマ数
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
        # 置ける数
        value = nb_move(board, player)
    return value

def evaluate9(board, player):
    # 置ける数-相手のコマ数
    return nb_move(board, player)-count(board, -player)

def evaluate10(board, player):
    # 置ける数-相手のコマ数
    return nb_move(board, player)-count(board, -player)


# 評価関数リスト
evaluate_funcs = [evaluate1, evaluate2, evaluate3, evaluate4, evaluate5, evaluate6, evaluate7, evaluate8]
evaluate_funcs = [evaluate1, evaluate2, evaluate4, evaluate7, evaluate8, evaluate9]

nb_funcs = len(evaluate_funcs)

# 勝敗リスト
win_lose = np.zeros((nb_funcs, nb_funcs))