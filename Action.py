from OthelloLogic import copy
import numpy as np
import OthelloLogic
import json
from evaluates import evaluate_funcs
evaluate = evaluate_funcs[-1]

# 最急降下法（効率化: 確率的勾配降下法）
def stochasticGradientDescent(X, y, theta, alpha, num_iters):
    X = np.array(X)
    y = np.array(y)
    theta = np.array(theta)
    m = len(y)
    for _ in range(num_iters):
        idx = np.random.randint(m)
        x_i = X[idx]
        y_i = y[idx]
        hx = np.dot(x_i, theta)
        gradient = x_i * (hx - y_i)
        theta -= alpha * gradient
    return theta

# 評価関数
def evaluateBoard(board, theta):
    score = evaluate(board, 1)
    return score
    piece_count = sum(row.count(1) for row in board)
    opponent_piece_count = sum(row.count(-1) for row in board)
    stable_pieces = countStablePieces(board, 1)
    opponent_stable_pieces = countStablePieces(board, -1)
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    corner_count = sum(1 for x, y in corners if board[x][y] == 1)
    opponent_corner_count = sum(1 for x, y in corners if board[x][y] == -1)

    # 特徴量ベクトルの定義
    X = np.array([piece_count, opponent_piece_count, corner_count, opponent_corner_count])
    
    # ベクトルサイズに応じたスコア計算
    score = np.dot(X, theta[:len(X)])  # 必要に応じてthetaを切り取る
    return score

# 安定な石の数を計算
def countStablePieces(board, player):
    stable_count = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == player and isStable(board, i, j, player):
                stable_count += 1
    return stable_count

def isStable(board, x, y, player):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        while 0 <= nx < 8 and 0 <= ny < 8:
            if board[nx][ny] != player:
                break
            nx += dx
            ny += dy
        else:
            return True
    return False

# α-β剪定の改良版
def alphaBetaMinimax(board, depth, alpha, beta, is_maximizing, theta):
    if depth == 0:
        return evaluateBoard(board, theta)

    moves = OthelloLogic.getMoves(board, 1 if is_maximizing else -1, 8)
    if not moves:
        return evaluateBoard(board, theta)

    moves = sorted(moves, key=lambda move: evaluateBoard(OthelloLogic.execute(copy(board), move, 
                                                                              1 if is_maximizing else -1, 8), theta),
                   reverse=is_maximizing)

    if is_maximizing:
        max_eval = -float('inf')
        for move in moves:
            next_board = OthelloLogic.execute(copy(board), move, 1, 8)
            eval = alphaBetaMinimax(next_board, depth - 1, alpha, beta, False, theta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            next_board = OthelloLogic.execute(copy(board), move, -1, 8)
            eval = alphaBetaMinimax(next_board, depth - 1, alpha, beta, True, theta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# 次の手を決定する関数
def getAction(board, moves, depth=6):
    print("現在の盤面")
    print(board)
    print("自分が石を置ける場所のリスト")
    print(moves)

    # thetaの初期値
    theta = np.array([1, -1, 0.5, -0.5])  # 初期重み (4つの特徴量に対応)
    max_score = -float('inf')
    best_move = moves[0]

    # 各手について評価し、最適な手を選択
    for move in moves:
        next_board = OthelloLogic.execute(copy(board), move, 1, 8)

        # 深さ6まで読み込んでスコアを計算
        score = alphaBetaMinimax(next_board, depth, -float('inf'), float('inf'), False, theta)
        if score > max_score:
            max_score = score
            best_move = move

    print("次に石を置く予定の場所")
    print(best_move)
    next_board = OthelloLogic.execute(copy(board), best_move, 1, 8)
    print("次の盤面")
    print(next_board)

    # 次の盤面で対戦相手が石を置くことができる場所のリスト
    opponents_moves = OthelloLogic.getMoves(next_board, -1, 8)
    print("対戦相手が次に石を置く予定の場所")
    print(opponents_moves)

    # タプル形式の座標をリストに変換して返す
    return list(best_move)

# 動作例
if __name__ == "__main__":
    # サンプルの盤面と合法手
    board = [[0 for _ in range(8)] for _ in range(8)]
    board[3][3], board[3][4], board[4][3], board[4][4] = 1, -1, -1, 1  # 初期配置
    moves = [(2, 3), (3, 2), (4, 5), (5, 4)]  # サンプルの合法手

    # 次の手を取得
    action = getAction(board, moves)
    action_json = json.dumps(action)  # JSON形式に変換
    print("次のアクション (JSON):", action_json)

    # finish_flag の確認
    data = {'finish_flag': False}  # 例: 事前にfinish_flagを初期化
    if 'finish_flag' in data and data['finish_flag']:
        print("ゲームが終了しました")
    else:
        print("ゲームを続行します")