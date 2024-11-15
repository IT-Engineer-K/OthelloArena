import math
import OthelloLogic

def evaluate(board, player):
    return sum(row.count(player) for row in board)


def minmax(board, moves, player=1, depth=7):
    