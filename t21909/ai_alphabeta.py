import time
import random
import copy
from config import DIM
from board import Board
from stone import Stone

# ------------------------
# AI_AlphaBeta クラス
# ------------------------


class AI:
    AI_LEVEL = 4     # AIが読む深さ
    AI_PERFECT = 12  # 12  # 完全読みをする手数
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
        eval_val += 16 * sum(
            [board.board[y][x].value for x, y in self.CORNERS]
        )

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
        if board.move_num >= DIM * DIM - 4 - self.AI_PERFECT:
            ai_level = DIM * DIM - 4 - board.move_num + 1
        for position in move_list:
            tmp_board = copy.deepcopy(board)
            tmp_board.move(position)  # 局面を進める
            if board.turn == Stone.BLACK:
                alpha = best_eval
                beta = 1000000
            else:
                alpha = -1000000
                beta = best_eval

            # 局面を評価
            eval = self.alphabeta(tmp_board, ai_level - 1, alpha, beta)
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

    def alphabeta(self, board, depth, alpha, beta):
        # 引数で指定された深さまで読んだか終局となった場合は、局面評価値を返す
        if depth <= 0 or board.is_game_end():
            return self.evaluation(board)

        # すべての指し手を生成
        move_list = board.get_moveable_list()
        if len(move_list) == 0:
            # 打てる場所がないのでパス
            tmp_board = copy.deepcopy(board)
            tmp_board.move_pass()
            return self.alphabeta(tmp_board, depth, alpha, beta)

        best_eval = -10000 * board.turn.value
        if board.turn == Stone.BLACK:
            best_eval = alpha
        else:
            best_eval = beta

        for position in move_list:
            tmp_board = copy.deepcopy(board)
            tmp_board.move(position)
            eval = self.alphabeta(tmp_board, depth - 1, alpha, beta)
            if board.turn == Stone.BLACK:
                if eval >= beta:
                    return eval
                if eval > best_eval:  # 黒の手番 : 評価値がより高い手
                    best_eval = eval
                    if alpha < best_eval:
                        alpha = best_eval
            else:
                if eval <= alpha:
                    return eval
                if eval < best_eval:  # 白の手番 : 評価値がより低い手
                    best_eval = eval
                    if beta > best_eval:
                        beta = best_eval

        return best_eval
