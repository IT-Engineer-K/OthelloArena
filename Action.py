from OthelloLogic import copy
import numpy as np
import OthelloLogic

class ActionClass:
    def __init__(self, evaluate):
        self.evaluate = evaluate

    # 評価関数
    def evaluateBoard(self, board, theta):
        score = self.evaluate(board, 1)
        return score

    # 安定な石の数を計算
    def countStablePieces(self, board, player):
        stable_count = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == player and self.isStable(board, i, j, player):
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
    def alphaBetaMinimax(self, board, depth, alpha, beta, is_maximizing, theta):
        if depth == 0:
            return self.evaluateBoard(board, theta)

        moves = OthelloLogic.getMoves(board, 1 if is_maximizing else -1, 8)
        if not moves:
            return self.evaluateBoard(board, theta)

        moves = sorted(moves, key=lambda move: self.evaluateBoard(OthelloLogic.execute(copy(board), move, 
                                                                                1 if is_maximizing else -1, 8), theta),
                    reverse=is_maximizing)

        if is_maximizing:
            max_eval = -float('inf')
            for move in moves:
                next_board = OthelloLogic.execute(copy(board), move, 1, 8)
                eval = self.alphaBetaMinimax(next_board, depth - 1, alpha, beta, False, theta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                next_board = OthelloLogic.execute(copy(board), move, -1, 8)
                eval = self.alphaBetaMinimax(next_board, depth - 1, alpha, beta, True, theta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    # 次の手を決定する関数
    def getAction(self, board, moves, depth=6):
        #print("現在の盤面")
        #print(board)
        #print("自分が石を置ける場所のリスト")
        #print(moves)

        # thetaの初期値
        theta = np.array([1, -1, 0.5, -0.5])  # 初期重み (4つの特徴量に対応)
        max_score = -float('inf')
        best_move = moves[0]

        # 各手について評価し、最適な手を選択
        for move in moves:
            next_board = OthelloLogic.execute(copy(board), move, 1, 8)

            # 深さ6まで読み込んでスコアを計算
            score = self.alphaBetaMinimax(next_board, depth, -float('inf'), float('inf'), False, theta)
            if score > max_score:
                max_score = score
                best_move = move

        #print("次に石を置く予定の場所")
        #print(best_move)
        #next_board = OthelloLogic.execute(copy(board), best_move, 1, 8)
        #print("次の盤面")
        #print(next_board)

        # 次の盤面で対戦相手が石を置くことができる場所のリスト
        #opponents_moves = OthelloLogic.getMoves(next_board, -1, 8)
        #print("対戦相手が次に石を置く予定の場所")
        #print(opponents_moves)

        # タプル形式の座標をリストに変換して返す
        return list(best_move)
