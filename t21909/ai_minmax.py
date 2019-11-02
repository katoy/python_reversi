import time
import random
import copy
from config import DIM
from board import Board
from stone import Stone

# ------------------------
# AI_MinMax クラス
# ------------------------


class AI:
    AI_LEVEL = 3  # 4  # AIが読む深さ
    CORNERS = [
        (0, 0), (0, DIM - 1), (DIM - 1, 0), (DIM - 1, DIM - 1)
    ]

    # 局面評価
    # 黒:プラス  白:マイナス
    def evaluation(self, board):
        # 終了局面であれば (黒石数 - 白石数) を返す
        if board.is_game_end():
            discs = board.get_discs()  # 黒白の石数をタプルで取得
            return 1000 * (discs[Stone.BLACK] - discs[Stone.WHITE])

        eval_val = 0
        # 隅
        eval_val += 16 * sum([board.board[y][x].value for x, y in self.CORNERS])

        # 手番 打てるマスの数
        move_num = len(board.get_moveable_list()) * board.turn.value

        # 相手 打てるマスの数
        board.move_pass()
        move_num += len(board.get_moveable_list()) * board.turn.value
        board.move_pass()

        eval_val += move_num * 2
        return eval_val

    # 与えられた盤面から指し手を返す
    def select_move(self, board):
        best_position = None
        # すべての指し手を生成
        move_list = board.get_moveable_list()
        # 同じ手になりにくくするためシャッフルする
        random.shuffle(move_list)

        if board.turn == Stone.BLACK:
            best_eval = -1000000  # 黒の手番:すごく低い評価値からスタート
        else:
            best_eval = 1000000  # 白の手番:すごく高い評価値からスタート

        ai_level = self.AI_LEVEL  # 読みの深さ
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

        print("{:02}手 best_eval: {}".format(board.move_num, best_eval))
        return best_position

    def minmax(self, board, depth):
        # 引数で指定された深さまで読んだか終局となった場合は、局面評価値を返す
        if depth <= 0 or board.is_game_end():
            return self.evaluation(board)

        # すべての指し手を生成
        move_list = board.get_moveable_list()
        if len(move_list) == 0:
            # 打てる場所がないのでパス
            tmp_board = copy.deepcopy(board)
            tmp_board.move_pass()
            return self.minmax(tmp_board, depth)

        best_eval = -10000 * board.turn.value
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
