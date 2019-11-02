from time import time, sleep
from tkinter import messagebox

from config import DIM, BOARD_PX_SIZE, CELL_PX_SIZE
from stone import Stone
from game_state import GameState
from player import Player
from board import Board
from locale_str import LocaleStr


class Game:
    YOKO = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, canvas_board, root, tk_vers):
        self.game_mode = GameState.STAY

        self.board = Board()  # 盤面作成
        self.canvas_board = canvas_board
        self.root = root
        self.tk_vars = tk_vers
        self.g_stones = [[None for _ in range(DIM)] for _ in range(DIM)]
        self.start()

    # 対局開始
    def start(
            self,
            _black_player=Player.HUMAN, _white_player=Player.HUMAN):

        self.black_player = _black_player
        self.white_player = _white_player
        self.last_move = None
        self.game_mode = GameState.PLAYING
        self.board.init_board()  # 盤面の初期化
        self.moves = [None for _ in range(DIM * DIM - 4)]

    # 局面を進める
    def game_move(self, position):
        if position:
            self.moves[self.board.move_num] = [
                self.board.turn.value, position.x,  position.y
            ]
            reverse_stones = self.board.move(position)  # 局面を進める
            self.draw_board(position, reverse_stones)   # 盤面を描画
            self.last_move = position

        # 終局判定
        if self.board.is_game_end():
            self.game_mode = GameState.END
            self.disp_message()  # メッセージ表示
            return

        # パス判定
        move_list = self.board.get_moveable_list()
        if len(move_list) == 0:
            # 石を打てる場所がないのでパス
            self.board.move_pass()
            if not self.get_turn().ai():
                messagebox.showinfo("パス", "打てる場所がないのでパスします")
                self.redraw()

        self.disp_message()  # メッセージ表示

    def get_turn(self):
        if self.board.turn == Stone.BLACK:
            return self.black_player
        if self.board.turn == Stone.WHITE:
            return self.white_player

    # 次の手番がコンピュータなら AIに指し手を選択させる
    def proc_machine_turn(self):
        while True:
            ai = self.get_turn().ai()
            if not ai:
                break

            position = ai.select_move(self.board)
            self.game_move(position)  # 局面を進める
            if self.game_mode == GameState.END:
                break  # 対局終了していたら抜ける

    def score_str(self):
        discs = self.board.get_discs()
        return " {}:{} {}:{}".format(
            LocaleStr.names(Stone.BLACK), discs[Stone.BLACK],
            LocaleStr.names(Stone.WHITE), discs[Stone.WHITE]
        )

    def result_str(self):
        discs = self.board.get_discs()
        if discs[Stone.BLACK] == discs[Stone.WHITE]:
            return " 引き分け"

        winer = Stone.WHITE
        if discs[Stone.BLACK] > discs[Stone.WHITE]:
            winer = Stone.BLACK

        return " {}の勝ち ".format(LocaleStr.names(winer))

    def get_player(self):
        if self.board.turn == Stone.BLACK:
            return self.black_player
        if self.board.turn == Stone.WHITE:
            return self.white_player

    # メッセージ表示
    def disp_message(self):
        mess = ""
        if self.game_mode == GameState.STAY:
            mess = "対局を開始してください"
        elif self.game_mode == GameState.PLAYING:
            mess += "対局中  {}手目 {} 次の手番 {}".format(
                self.board.move_num, self.score_str(),
                LocaleStr.names(self.board.turn)
            )
        elif self.game_mode == GameState.END:
            mess = "{} {}手 {} {}".format(
                LocaleStr.names("Label_end_game"),
                self.board.move_num, self.score_str(), self.result_str()
            )

        self.tk_vars["mess_var"].set(mess)  # メッセージラベルにセット
        self.tk_vars["kifu_var"].set(self.kifu_str(self.moves))

    def draw_board(self, position, reverse_stones=[]):
        self.last_move = position
        if self.black_player == Player.HUMAN or \
                self.white_player == Player.HUMAN:
            self.draw_stone(
                x=position.x, y=position.y,
                fill=self.board.turn.invert().color()
            )
            self.animation_reverse(reverse_stones)

        self.redraw()

    def animation_reverse(self, reverse_stones):
        fill_0 = self.board.turn.color()
        fill_1 = self.board.turn.invert().color()
        r = CELL_PX_SIZE / 2 * 0.8
        count = 5
        for stones in reverse_stones:
            for i in range(-count, count):
                for pos in stones:
                    id = self.g_stones[pos[1]][pos[0]]
                    cx = (pos[0] + 0.5) * CELL_PX_SIZE
                    cy = (pos[1] + 0.5) * CELL_PX_SIZE
                    if i < 0:
                        fill = fill_0
                    else:
                        fill = fill_1

                    dr = r * abs(i) / count
                    self.canvas_board.itemconfigure(id, fill=fill)
                    self.canvas_board.coords(
                        id, cx - dr, cy - r, cx + dr, cy + r
                    )

                self.canvas_board.update()
                sleep(0.02)

    def redraw(self):
        self.canvas_board.delete('all')  # キャンバスをクリア
        self.g_stones = [[None for _ in range(DIM)] for _ in range(DIM)]

        # 背景
        self.canvas_board.create_rectangle(
            0, 0, BOARD_PX_SIZE, BOARD_PX_SIZE, fill="#00a000"
        )
        move_list = []
        if self.game_mode == GameState.PLAYING and not self.get_turn().ai():
            move_list = self.board.get_moveable_list()
            self.board.set_marks(move_list, disp=True)

        for y in range(DIM):
            for x in range(DIM):
                cx = (x + 0.5) * CELL_PX_SIZE
                cy = (y + 0.5) * CELL_PX_SIZE
                r = CELL_PX_SIZE / 2 * 0.9
                self.g_stones[y][x] = self.canvas_board.create_oval(
                    cx - r, cy - r, cx + r, cy + r,
                    fill="#00a000", outline=""
                )

        for y in range(DIM):
            for x in range(DIM):
                disc = self.board.board[y][x]
                id = self.g_stones[y][x]
                if disc == Stone.BLACK or disc == Stone.WHITE:  # 石の描画
                    self.canvas_board.itemconfigure(id, fill=disc.color())
                elif disc == Stone.MARK:  # 次における場所の候補の描画
                    self.draw_stone(
                        x=x, y=y,
                        fill=self.board.turn.color(), stone_size=0.2
                    )

        self.board.set_marks(move_list, disp=False)
        self.draw_last_stone()

        # 枠を描画
        for i in range(DIM):
            d = i * CELL_PX_SIZE
            self.canvas_board.create_line(
                d, 0, d, BOARD_PX_SIZE, fill="black", width=1
            )
            self.canvas_board.create_line(
                0, d, BOARD_PX_SIZE, d, fill="black", width=1
            )

        self.canvas_board.update()

    def draw_stone(self, x=0, y=0, fill="black", stone_size=0.8):
        id = self.g_stones[y][x]
        cx = (x + 0.5) * CELL_PX_SIZE
        cy = (y + 0.5) * CELL_PX_SIZE
        r = CELL_PX_SIZE / 2 * stone_size
        self.canvas_board.itemconfigure(id, fill=fill)
        self.canvas_board.coords(id, cx - r, cy - r, cx + r, cy + r)

    def draw_last_stone(self, stone_size=0.2):
        if self.last_move is None:
            return

        cx = (self.last_move.x + 0.5) * CELL_PX_SIZE
        cy = (self.last_move.y + 0.5) * CELL_PX_SIZE
        r = CELL_PX_SIZE / 2 * stone_size
        self.g_last_stone = self.canvas_board.create_oval(
            cx - r, cy - r, cx + r, cy + r, fill="red", outline=""
        )

    def hide_last_stone(self):
        id = self.g_last_stone
        self.canvas_board.coords(id, 0, 0, 0, 0)

    def kifu_str(self, moves):
        kifu = ""
        for v in moves:
            if v:
                kifu += self.YOKO[v[1]] + str(v[2] + 1)
        return kifu
