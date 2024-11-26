import OthelloLogic
import Action
from kubo import play_sound

class ActionClass:
    def __init__(self, evaluate_func):
        self.evaluate = evaluate_func
        self.action = Action.ActionClass(self.evaluate)

    # α-β剪定を用いたミニマックス関数
    def alphaBetaMinimax(self, board, depth, alpha, beta, is_maximizing):
        player = [-1, 1][is_maximizing]
        if depth == 0:
            return self.evaluate(board, player)

        moves = OthelloLogic.getMoves(board, 1 if is_maximizing else -1, 8)
        if not moves:  # 合法手がない場合は評価関数に基づいたスコアを返す
            next_board = OthelloLogic.copy(board)
            eval = self.alphaBetaMinimax(next_board, depth - 1, alpha, beta, False)

        if is_maximizing:
            max_eval = -float('inf')
            for move in moves:
                next_board = OthelloLogic.execute(OthelloLogic.copy(board), move, 1, 8)
                eval = self.alphaBetaMinimax(next_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # βカットオフ
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                next_board = OthelloLogic.execute(OthelloLogic.copy(board), move, -1, 8)
                eval = self.alphaBetaMinimax(next_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # αカットオフ
            return min_eval

    # 次の手を決定する関数
    def getAction(self, board, moves, depth=6):
        #play_sound(moves)
        return self.action.getAction(board, moves, depth=depth)