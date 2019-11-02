import time
import random
import copy
from board import Board
from stone import Stone

# ------------------------
# AI_Randum クラス
# ------------------------


class AI:
    AI_LEVEL = 4  # AIが読む深

    # 与えられた盤面から指し手を返す
    def select_move(self, board):
        # すべての指し手を生成
        move_list = board.get_moveable_list()
        # 同じ手になりにくくするためシャッフルする
        random.shuffle(move_list)

        ai_level = self.AI_LEVEL  # 読みの深さ

        if board.turn == Stone.BLACK:
            best_eval = -10000  # 黒の手番:すごく低い評価値からスタート
        else:
            best_eval = 10000   # 白の手番:すごく高い評価値からスタート

        for position in move_list:
            tmp_board = copy.deepcopy(board)
            tmp_board.move(position)  # 局面を進める
            eval = self.minmax(tmp_board, ai_level - 1)  # 局面を評価
            if board.turn == Stone.BLACK:
                if eval > best_eval:
                    # 黒の手番 : 評価値がより高い手の場合は最善手を入れ替える
                    best_eval = eval
                    best_position = position
            else:
                if eval < best_eval:
                    # 白の手番 : 評価値がより低い手の場合は最善手を入れ替える
                    best_eval = eval
                    best_position = position

        print(
            str(board.move_num) + "手 best_eval: " + str(best_eval)
        )
        return best_position

    def minmax(self, board, depth):
        # 引数で指定された深さまで読んだか終局となった場合は、局面評価値を返す
        if depth <= 0 or board.is_game_end():
            return board.evaluation()

        # すべての指し手を生成
        move_list = board.get_moveable_list()
        if len(move_list) == 0:
            # 打てる場所がないのでパス
            tmp_board = copy.deepcopy(board)
            tmp_board.move_pass()
            return self.minmax(tmp_board, depth)

        if board.turn == Stone.BLACK:
            best_eval = -10000  # 黒の手番:すごく低い評価値からスタート
        else:
            best_eval = 10000   # 白の手番:すごく高い評価値からスタート

        for position in move_list:
            tmp_board = copy.deepcopy(board)
            tmp_board.move(position)
            eval = self.minmax(tmp_board, depth - 1)
            if board.turn == Stone.BLACK:
                if eval > best_eval:  # 黒の手番 : 評価値がより高い手
                    best_eval = eval
            else:
                if eval < best_eval:  # 白の手番 : 評価値がより低い手
                    best_eval = eval

        return best_eval
