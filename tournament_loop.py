from TestPlay_tournament import TestPlay
import OthelloAction
from evaluates import evaluate_funcs
import numpy as np

nb_funcs = len(evaluate_funcs)
winlose = np.zeros((nb_funcs, nb_funcs))

depth=2

for index1, evaluate_func1 in enumerate(evaluate_funcs):
    for index2, evaluate_func2 in enumerate(evaluate_funcs):
        if index1 == index2:
            continue
        othelloAction1 = OthelloAction.ActionClass(evaluate_func1)
        othelloAction2 = OthelloAction.ActionClass(evaluate_func2)
        result = TestPlay(othelloAction1, othelloAction2, index1, index2, depth)
        if result < 0:
            winlose[index1][index2] = -1
        elif result > 0:
            winlose[index1][index2] = 1
        else:
            winlose[index1][index2] = 0
print(winlose)
print(np.sum(winlose, axis=1))
print(np.sum(winlose, axis=0))
print()
print(np.sum(winlose, axis=1) + np.sum(winlose, axis=0))