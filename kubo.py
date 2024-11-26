import random
import copy
import OthelloLogic
import pyttsx3


def getAction(board,moves):
	print("現在の盤面")
	print(board)

	print("自分が石を置ける場所のリスト")
	print(moves)

	#渡されたMovesの中からランダムで返り値として返却する。
	index = random.randrange(len(moves))
	next_move = moves[index]

	print("次に石を置く予定の場所")
	print(next_move)

	# next_moveに石を置いた場合の次の盤面を取得する
	# OthelloLogic.executeの第1引数は現在の盤面、第2引数はこれから石を置く場所、
	# 第3引数は石を置く人が自分のAIなら1で、対戦相手なら-1に設定、
	# 第4引数は盤面の大きさで8×8なら8を設定
     
	next_board = OthelloLogic.execute(copy.deepcopy(board),next_move,1,8)
	print("次の盤面")
	print(next_board)
    

	# 次の盤面で対戦相手が石を置くことができる場所のリスト
	# OthelloLogic.getMovesの第1引数は盤面、第２引数は対戦相手なら-1、自分なら1
	# 第3引数は盤面の大きさで8×8なら8を設定
	opponents_moves = OthelloLogic.getMoves(next_board,-1,8)

	print("対戦相手が次に石を置く予定の場所")
	print(opponents_moves)

	return next_move


#音声を出力する関数
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)      # 読み上げ速度
    engine.setProperty('volume', 0.9)    # 音量 (0.0から1.0)
    engine.say(text)
    engine.runAndWait()

def play_sound(next_move):
    # ブラックラインのチェック (左斜めと右斜め)
    black_line_left = all(next_move[i, i] == 1 for i in range(8))
    black_line_right = all(next_move[i, 7 - i] == 1 for i in range(8))
    
    # 爆弾のチェック (条件をリストにして any() で判定)
    bomb_conditions = [
        next_move[0, 2] == -1 and next_move[0, 3] == 1 and next_move[0, 4] == 1 and next_move[0, 5] == -1,
        next_move[2, 0] == -1 and next_move[3, 0] == 1 and next_move[4, 0] == 1 and next_move[5, 0] == -1,
        next_move[7, 2] == -1 and next_move[7, 3] == 1 and next_move[7, 4] == 1 and next_move[7, 5] == -1,
        next_move[2, 7] == -1 and next_move[3, 7] == 1 and next_move[4, 7] == 1 and next_move[5, 7] == -1
    ]
    bomb = any(bomb_conditions)

    # ウイング:片側は1マスだけ、もう片方は隅から2マスだけ空いている形のこと
    wing_condition = [
         all(next_move[0, i] == 1 for i in range(1, 6)) and next_move[1, 2] == 1 and next_move[1, 5] == 1,
         all(next_move[0, i] == 1 for i in range(2, 7)) and next_move[1, 2] == 1 and next_move[1, 5] == 1,
         all(next_move[i, 0] == 1 for i in range(1, 6)) and next_move[2, 1] == 1 and next_move[5, 1] == 1,
         all(next_move[i, 0] == 1 for i in range(2, 7)) and next_move[2, 1] == 1 and next_move[5, 1] == 1,
         all(next_move[i, 7] == 1 for i in range(1, 6)) and next_move[2, 6] == 1 and next_move[5, 6] == 1,
         all(next_move[i, 7] == 1 for i in range(2, 7)) and next_move[2, 6] == 1 and next_move[5, 6] == 1,
         all(next_move[7, i] == 1 for i in range(1, 6)) and next_move[6, 2] == 1 and next_move[6, 5] == 1,
         all(next_move[7, i] == 1 for i in range(2, 7)) and next_move[6, 2] == 1 and next_move[6, 5] == 1
    ]
    wing = any(wing_condition)

    mountain_condition = [
        all(next_move[0, i] == 1 for i in range(1, 6)),
        all(next_move[7, i] == 1 for i in range(1, 6)),
        all(next_move[i, 0] == 1 for i in range(1, 6)),
        all(next_move[i, 7] == 1 for i in range(1, 6))
    ]
    mountain = any(mountain_condition)

              
    # ブラックラインおよび爆弾の判定に基づき音声出力
    if black_line_left or black_line_right:
        print("ブラックライン")
        speak("ぶらっくらいん")
        black_line_left = False
        black_line_right = False

    if bomb:
        print("爆弾")
        speak("ばくだん")
        bomb = False
    
    if wing:
         print("ウィング")
         speak("ういんぐ")
         wing = False
    
    if mountain:
         print("山")
         speak("やま")
         mountain = False


"""
技名を参照したサイト
https://karench.link/wordpress/othello-terminology/
https://f8otheller.com/176/

"""