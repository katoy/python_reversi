# coding: utf8
from enum import Enum
import math
import tkinter
from tkinter import messagebox
from tkinter import ttk

import ai_randum

# =========================
# リバーシ
# See https://info.nikkeibp.co.jp/media/NSW/atcl/mag/071800024/
#     日経ソフトウエア 2019年9月号
# =========================
DIM = 8                             # 一辺のマス数
BOARD_PX_SIZE = 400                 # 盤面のサイズ
CELL_PX_SIZE = BOARD_PX_SIZE / DIM  # マスのサイズ


class GameState(Enum):
    # ゲームの状態 開始待ち / 対局中 / 対局終了
    STAY = 1
    PLAYING = 2
    END = 3


class Stone(Enum):
    SPACE = 0   # 空き
    BLACK = 1   # 黒石
    WHITE = -1  # 白石

    def invert(self):
        return Stone(self.value * (-1))


class Player(Enum):
    HUMAN = -1
    MACHINE = 1


class Position:
    def __init__(self, x=0, y=0):
        self.y = y
        self.x = x


class LocaleStr:
    JA_NAMES = {
        Stone.WHITE: "白", Stone.BLACK: "黒",
        Player.HUMAN: "人間", Player.MACHINE: "コンピュータ"
    }


class Board:
    # 8方向
    DIRS = [[dx, dy]
            for dx in [-1, 0, 1] for dy in [-1, 0, 1]
            if dx * dx + dy * dy > 0]

    def __init__(self):
        self.board = [
            [Stone.SPACE for _ in range(DIM)] for _ in range(DIM)
        ]
        self.turn = Stone.BLACK   # 手番
        self.move_num = 0         # 手数

    # 盤面の初期化（初期配置）
    def init_board(self):
        for y in range(DIM):
            for x in range(DIM):
                self.board[y][x] = Stone.SPACE

        c0 = DIM // 2 - 1
        for dy in range(2):
            for dx in range(2):
                val = 2 * ((dx + dy) % 2) - 1
                self.board[c0 + dy][c0 + dx] = Stone(val)

        self.turn = Stone.BLACK   # 手番
        self.move_num = 0         # 手数

    # 黒白の石数をタプルで返す
    def get_discs(self):
        discs = {1: 0, -1: 0, 0: 0}
        for y in range(DIM):
            for x in range(DIM):
                discs[(self.board[y][x]).value] += 1
        return (discs[1], discs[-1])

    # 指定のマスに石を打てるか？
    def is_movable(self, position):
        # 空きでなければ打てない
        if self.board[position.y][position.x] != Stone.SPACE:
            return False

        # 各方向に石をひっくり返せるか？
        for dir in Board.DIRS:
            y = position.y + dir[0]
            x = position.x + dir[1]
            if y >= 0 and x >= 0 and y < 8 and x < 8 \
                    and self.board[y][x].value == -self.turn.value:
                # 隣が相手の石
                y += dir[0]
                x += dir[1]
                while y >= 0 and x >= 0 and y < 8 and x < 8 \
                        and self.board[y][x].value == -self.turn.value:
                    y += dir[0]
                    x += dir[1]
                if y >= 0 and x >= 0 and y < 8 and x < 8 \
                        and self.board[y][x].value == self.turn.value:
                    return True

        return False

    # 石を打てる Position のリストを返す
    def get_move_list(self):
        move_list = []
        for y in range(DIM):
            for x in range(DIM):
                if self.board[y][x] == Stone.SPACE:
                    position = Position(x, y)
                    if self.is_movable(position):
                        move_list.append(position)
        return move_list

    # 局面を進める
    def move(self, position):
        # 石を打つ
        self.board[position.y][position.x] = Stone(self.turn.value)

        # 石をひっくり返す
        # 各方向に石をひっくり返せるか調べる
        for dir in Board.DIRS:
            y = position.y + dir[0]
            x = position.x + dir[1]
            if y >= 0 and x >= 0 and y < DIM and x < DIM \
                    and self.board[y][x].value == -self.turn.value:
                # 隣が相手の石
                y += dir[0]
                x += dir[1]
                while y >= 0 and x >= 0 and y < DIM and x < DIM \
                        and self.board[y][x].value == -self.turn.value:
                    y += dir[0]
                    x += dir[1]
                if y >= 0 and x >= 0 and y < 8 and x < 8 \
                        and self.board[y][x].value == self.turn.value:
                    # この方向は返せる
                    # 1マス戻る
                    y -= dir[0]
                    x -= dir[1]
                    # 戻りながら返す
                    while y >= 0 and x >= 0 and y < DIM and x < DIM \
                            and self.board[y][x].value == -self.turn.value:
                        self.board[y][x] = Stone(self.turn.value)
                        y -= dir[0]
                        x -= dir[1]

        self.turn = self.turn.invert()  # 手番を変更
        self.move_num += 1    # 手数を増やす

    # パスする
    def move_pass(self):
        self.turn = self.turn.invert()  # パス

    # 対局終了の判定
    def is_game_end(self):
        # 60手に達した時
        if self.move_num == DIM * DIM - 4:
            return True

        # 黒白どちらかの石数が0になった時
        # 黒白の石数をタプルで取得
        (black_discs, white_discs) = self.get_discs()
        if black_discs == 0 or white_discs == 0:
            return True

        # 黒白どちらも手がない場合
        move_list1 = self.get_move_list()
        if len(move_list1) == 0:
            self.move_pass()  # パスして相手番にする
            move_list2 = self.get_move_list()
            self.move_pass()  # パスして戻す
            if len(move_list2) == 0:
                return True

        return False

# ------------------------
# ゲームクラス
# ------------------------


class Game:
    def __init__(self, canvas_board, root, black_var, white_var, mess_var):
        self.game_mode = GameState.STAY

        self.black_player = Player.HUMAN
        self.white_player = Player.HUMAN
        self.board = Board()  # 盤面作成
        self.board.init_board()  # 盤面の初期化
        self.canvas_board = canvas_board
        self.root = root
        self.black_var = black_var
        self.white_var = white_var
        self.mess_var = mess_var

    # 対局開始
    def start(self, _black_player, _white_player):
        self.black_player = _black_player
        self.white_player = _white_player
        self.game_mode = GameState.PLAYING
        self.board.init_board()  # 盤面の初期化

    # 局面を進める
    def game_move(self, position):
        self.board.move(position)  # 局面を進める
        draw_board(self)        # 盤面を描画

        # 終局判定
        if self.board.is_game_end():
            self.game_mode = GameState.END
            disp_message(self)        # メッセージ表示
            messagebox.showinfo("", "対局終了")
            return

        # パス判定
        move_list = self.board.get_move_list()
        if len(move_list) == 0:
            # 石を打てる場所がないのでパス
            self.board.move_pass()
            if self.is_human_turn():
                messagebox.showinfo("パス", "打てる場所がないのでパスします")

        disp_message(self)          # メッセージ表示

    # 次の手番はコンピュータか？
    def is_machine_turn(self):
        return (
            self.board.turn == Stone.BLACK and
            self.black_player == Player.MACHINE
        ) or (
            self.board.turn == Stone.WHITE and
            self.white_player == Player.MACHINE
        )

    def is_human_turn(self):
        return not self.is_machine_turn()

    # 次の手番がコンピュータなら
    # AIに指し手を選択させる
    def proc_machine_turn(self):
        ai = ai_randum.AI()
        while True:
            if self.is_machine_turn():
                position = ai.select_move(self.board)
                self.game_move(position)  # 局面を進める
                if self.game_mode == GameState.END:
                    break  # 対局終了していたら抜ける
            else:
                break

    def score_str(self):
        (black_discs, white_discs) = game.board.get_discs()
        return " {}:{} {}:{}".format(
            LocaleStr.JA_NAMES[Stone.BLACK], black_discs,
            LocaleStr.JA_NAMES[Stone.WHITE], white_discs
        )

    def result_str(self):
        (black_discs, white_discs) = game.board.get_discs()
        if black_discs == white_discs:
            return " 引き分け"
        elif black_discs > white_discs:
            return " {}の勝ち ".format(LocaleStr.JA_NAMES[Stone.BLACK])
        else:
            return " {}の勝ち ".format(LocaleStr.JA_NAMES[Stone.WHITE])

# ------------------------
# UI関数
# ------------------------
# 盤面の描画


def init_board(game):
    # キャンバスの位置を指定
    game.canvas_board.place(x=16, y=72)

    # 対局条件
    black_label = ttk.Label(text="先手●")
    black_label.place(x=16, y=4)
    black_rdo0 = ttk.Radiobutton(
        game.root, value=-1, variable=game.black_var,
        text=LocaleStr.JA_NAMES[Player.HUMAN]
    )
    black_rdo0.place(x=70, y=4)
    black_rdo1 = ttk.Radiobutton(
        game.root, value=1, variable=game.black_var,
        text=LocaleStr.JA_NAMES[Player.MACHINE]
    )
    black_rdo1.place(x=120, y=4)

    white_label = ttk.Label(text="後手○")
    white_label.place(x=16, y=24)
    white_rdo0 = ttk.Radiobutton(
        game.root, value=-1, variable=game.white_var,
        text=LocaleStr.JA_NAMES[Player.HUMAN]
    )
    white_rdo0.place(x=70, y=24)
    white_rdo1 = ttk.Radiobutton(
        game.root, value=1, variable=game.white_var,
        text=LocaleStr.JA_NAMES[Player.MACHINE]
    )
    white_rdo1.place(x=120, y=24)

    # 「対局開始」ボタンを設置
    button_start = ttk.Button(
        game.root, text="対局開始", width=6, command=lambda: play_start(game)
    )
    button_start.place(x=240, y=12)

    mess_label = ttk.Label(game.root, textvariable=game.mess_var)
    mess_label.place(x=16, y=48)


def draw_board(game):
    game.canvas_board.delete('all')  # キャンバスをクリア
    # 背景
    game.canvas_board.create_rectangle(
        0, 0, BOARD_PX_SIZE, BOARD_PX_SIZE, fill='#00a000'
    )
    for y in range(DIM):
        for x in range(DIM):
            disc = game.board.board[y][x]
            if disc != Stone.SPACE:
                if disc == Stone.BLACK:
                    color = "black"
                else:
                    color = "white"
                # 石の描画
                game.canvas_board.create_oval(
                    x * CELL_PX_SIZE + 4, y * CELL_PX_SIZE + 4,
                    (x + 1) * CELL_PX_SIZE - 4,
                    (y + 1) * CELL_PX_SIZE - 4, fill=color)

    # 枠を描画
    for x in range(DIM):
        game.canvas_board.create_line(
            x * CELL_PX_SIZE,
            0, x * CELL_PX_SIZE, BOARD_PX_SIZE,
            fill="black", width=1
        )
    for y in range(DIM):
        game.canvas_board.create_line(
            0, y * CELL_PX_SIZE,
            BOARD_PX_SIZE, y * CELL_PX_SIZE,
            fill="black", width=1
        )

    game.canvas_board.update()

# メッセージ表示


def disp_message(game):
    mess = ""
    if game.game_mode == GameState.STAY:
        mess = "対局を開始してください"
    elif game.game_mode == GameState.PLAYING:
        mess += "対局中 {}手目 {}番 {}".format(
            game.board.move_num, LocaleStr.JA_NAMES[game.board.turn],
            game.score_str()
        )
    elif game.game_mode == GameState.END:
        mess = "対局終了 {}手 {}".format(
            game.board.move_num, game.score_str(), game.result_str()
        )

    game.mess_var.set(mess)  # メッセージラベルにセット


# 「対局開始」ボタンが押された時


def play_start(game):
    # 対局開始
    game.start(Player(game.black_var.get()), Player(game.white_var.get()))
    disp_message(game)  # メッセージ表示
    draw_board(game)    # 盤面を描画

    # 次の手番がコンピュータの場合（人間の手番なら何もしない）
    game.proc_machine_turn()

# 盤面がクリックされた時


def click_board(event, game):
    if game.game_mode != GameState.PLAYING:
        messagebox.showinfo("", "対局開始してください")
        return
    y = math.floor(event.y / CELL_PX_SIZE)
    x = math.floor(event.x / CELL_PX_SIZE)
    position = Position(x, y)
    if not game.board.is_movable(position):
        messagebox.showinfo("", "そこには打てません")
        return

    game.game_move(position)  # 局面を進める
    if game.game_mode == GameState.END:
        return  # 対局終了していたら抜ける

    # 次の手番がコンピュータの場合
    # （プレイヤーの手番なら何もしない）
    game.proc_machine_turn()


# ------------------------
# メイン処理
# ------------------------
root = tkinter.Tk()
black_var = tkinter.IntVar()
white_var = tkinter.IntVar()
mess_var = tkinter.StringVar()

root.title("リバーシ 0.1")
# ウインドウの幅, 高さ
window_width = BOARD_PX_SIZE + 32
window_height = BOARD_PX_SIZE + 88
# ウインドウサイズを指定
root.geometry('{}x{}'.format(BOARD_PX_SIZE + 32, BOARD_PX_SIZE + 88))

# 盤面キャンバスを作成
# キャンバスを作成
canvas_board = tkinter.Canvas(root, width=BOARD_PX_SIZE, height=BOARD_PX_SIZE)
# キャンバスがクリックされた時に呼び出す関数を設定
canvas_board.bind("<Button-1>", lambda e: click_board(e, game))

game = Game(canvas_board, root, black_var, white_var, mess_var)   # ゲームインスタンス作成
init_board(game)

draw_board(game)            # 盤面を描画
disp_message(game)          # メッセージ表示

# GUIの待ち受けループ
root.mainloop()
