from TestPlay_tournament import TestPlay
import Action as OthelloAction
from evaluates import gen_evaluates
import numpy as np
import pickle
import random

def save_data(data):
    with open("data.pickle", "wb") as f:
        pickle.dump(data, f)

def load_data():
    try:
        with open("data.pickle", "rb") as f:
            return pickle.load(f)
    except:
        return {}

def toKey(depth, weights):
    return str(depth) + "_" + str(weights).replace(' ', '')

data = load_data()
nb_funcs = 8
depth = 1

if data == {}:
    # 初期化
    weights_list = np.random.random((5, nb_funcs))
    data = {
        "players": {},
        "enemies": []
    }
else:
    # 評価の高い重み参考に、新たな重みを生成
    scores = []
    weights_list = []
    for key in list(data["players"].keys()):
        d = data["players"][key]
        if key not in data["enemies"]:
            continue
        scores.append(np.average(d["winlose"]))
        weights_list.append(d["weights"])
    scores = np.array(scores)
    weights_list = np.array(weights_list)
    good_score = np.average(scores)
    print(scores, good_score)
    w = [s if 0 <= s else 0 for s in scores - good_score]
    k = random.randint(1, 2)

    new_weights_list = random.choices(weights_list, weights=w, k=k)
    new_weights_list = np.array(new_weights_list)
    
    new_weights = np.random.rand(8)
    new_weights /= new_weights.sum()
    new_weights *= random.random() * .2
    for new_weights_ in new_weights_list:
        new_weights += new_weights_ * random.random()
    weights_list = [new_weights]


weights_list = np.array(weights_list)
# 重みの正規化
weights_list = weights_list / weights_list.sum(axis=1, keepdims=True)
print(len(data["players"].keys()))

if not(len(weights_list.shape) == 2 and weights_list.shape[1] == nb_funcs):
    raise


for weights in weights_list:
    if toKey(depth, weights) not in data["players"].keys():
        new_data = {
            "weights": weights,
            "str_opponents": [],
            "opponents": [],
            "winlose": []
        }
        data["players"][toKey(depth, weights)] = new_data

nb_players = len(data["players"].keys())
if nb_players < 10:
    enemies = list(data["players"].keys())
else:
    enemies = random.sample(list(data["players"].keys()), k=10)

# 対戦開始
for key, player_data in data["players"].items():
    weights1 = np.array(player_data["weights"])

    evaluate_func1 = gen_evaluates(weights1)
    
    will_save = False
    
    for enemy_key in enemies:
        if enemy_key in player_data["str_opponents"]:
            continue
        weights2 = data["players"][enemy_key]["weights"]

        will_save = True
        evaluate_func2 = gen_evaluates(weights2)
        othelloAction1 = OthelloAction.ActionClass(evaluate_func1)
        othelloAction2 = OthelloAction.ActionClass(evaluate_func2)
        result = TestPlay(othelloAction1, othelloAction2, depth)


        if 0 < result: winlose = 1
        elif result < 0: winlose = -1
        else: winlose = 0
        winlose += result * .001
        print(result, winlose)

        player_data["str_opponents"].append(toKey(depth, weights2))
        player_data["opponents"].append(weights2)
        player_data["winlose"].append(winlose)
        
    data["players"][key] = player_data
    if will_save:
        save_data(data)
        print()

print()

max_index = 0
max_score = -float('inf')
scores = []
i = 0
for weights_key, value in data["players"].items():
    score = 0
    for enemy in enemies:
        score += value["winlose"][value["str_opponents"].index(enemy)]
    score /= len(enemies)
    scores.append(score)
    
    if score > max_score:
        max_score = score
        max_index = i
        best_weights = value["weights"]
    i += 1
data["enemies"] = enemies
save_data(data)
print()
print(scores)
print(max_score, max_index)
np.save("best_weights.npy", best_weights)