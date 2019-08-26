
import time
import random

# ------------------------
# AI_Randum クラス
# ------------------------


class AI:
    SLEEP_SEC = 0.01

    # 与えられた盤面から指し手を返す
    def select_move(self, board):
        time.sleep(AI.SLEEP_SEC)  # すこし待つ
        move_list = board.get_move_list()
        # ランダムに指し手を選ぶ
        r = random.randint(0, len(move_list) - 1)
        return move_list[r]
