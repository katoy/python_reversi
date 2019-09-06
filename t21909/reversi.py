# coding: utf8
from enum import Enum
import math
import tkinter
from tkinter import messagebox
from tkinter import ttk
from time import time, sleep

from config import CELL_PX_SIZE, BOARD_PX_SIZE
from position import Position
from player import Player
from game_state import GameState
from game import Game
from locale_str import LocaleStr

# =========================
# リバーシ
#     https://info.nikkeibp.co.jp/media/NSW/atcl/mag/071800024/
#     日経ソフトウエア 2019年9月号
#  をベースにして作成した。
# =========================


def init_board(game):
    # キャンバスの位置を指定
    game.canvas_board.place(x=16, y=72)

    # 対局条件
    black_label = ttk.Label(text=LocaleStr.JA_NAMES["Play_First"])
    black_label.place(x=16, y=4)
    black_rdo0 = ttk.Radiobutton(
        game.root, text=LocaleStr.JA_NAMES[Player.HUMAN],
        value=Player.HUMAN.value, variable=game.tk_vars["black_var"]
    )
    black_rdo0.place(x=70, y=4)
    black_rdo1 = ttk.Radiobutton(
        game.root, text=LocaleStr.JA_NAMES[Player.AI_RANDUM],
        value=Player.AI_RANDUM.value, variable=game.tk_vars["black_var"]
    )
    black_rdo1.place(x=120, y=4)

    white_label = ttk.Label(text=LocaleStr.JA_NAMES["Play_Second"])
    white_label.place(x=16, y=24)
    white_rdo0 = ttk.Radiobutton(
        game.root, text=LocaleStr.JA_NAMES[Player.HUMAN],
        value=Player.HUMAN.value, variable=game.tk_vars["white_var"]
    )
    white_rdo0.place(x=70, y=24)
    white_rdo1 = ttk.Radiobutton(
        game.root, text=LocaleStr.JA_NAMES[Player.AI_RANDUM],
        value=Player.AI_RANDUM.value, variable=game.tk_vars["white_var"]
    )
    white_rdo1.place(x=120, y=24)

    # 「対局開始」ボタンを設置
    button_start = ttk.Button(
        game.root, text="対局開始", width=6, command=lambda: play_start(game)
    )
    button_start.place(x=300, y=12)

    mess_label = ttk.Label(game.root, textvariable=game.tk_vars["mess_var"])
    mess_label.place(x=16, y=48)

# 「対局開始」ボタンが押された時


def play_start(game):
    # 対局開始
    game.start(
        Player(game.tk_vars["black_var"].get()),
        Player(game.tk_vars["white_var"].get())
    )
    game.disp_message()  # メッセージ表示
    game.redraw()        # 盤面を描画

    # 次の手番がコンピュータの場合（人間の手番なら何もしない）
    game.proc_machine_turn()

# 盤面がクリックされた時


def click_board(event, game):
    if game.game_mode != GameState.PLAYING:
        messagebox.showinfo("", "対局開始してください")
        return

    if game.is_human_turn():
        x = math.floor(event.x / CELL_PX_SIZE)
        y = math.floor(event.y / CELL_PX_SIZE)
        if not game.board.is_movable_xy(x, y):
            return

        game.game_move(Position(x=x, y=y))  # 局面を進める
        if game.game_mode == GameState.END:
            return  # 対局終了していたら抜ける

    # 次の手番がコンピュータの場合
    game.proc_machine_turn()


# ------------------------
# メイン処理
# ------------------------
root = tkinter.Tk()
root.title("リバーシ 0.1")
tk_vars = {
    "black_var": tkinter.IntVar(),
    "white_var": tkinter.IntVar(),
    "mess_var": tkinter.StringVar()
}
# ウインドウサイズを指定
root.geometry('{}x{}'.format(BOARD_PX_SIZE + 32, BOARD_PX_SIZE + 90))

# 盤面キャンバスを作成
canvas_board = tkinter.Canvas(root, width=BOARD_PX_SIZE, height=BOARD_PX_SIZE)
# キャンバスがクリックされた時に呼び出す関数を設定
canvas_board.bind("<Button-1>", lambda e: click_board(e, game))

game = Game(canvas_board, root, tk_vars)
init_board(game)
game.redraw()        # 盤面を描画
game.disp_message()  # メッセージ表示

root.mainloop()     # GUIの待ち受けループ
