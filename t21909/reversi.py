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
    black_label = ttk.Label(text=LocaleStr.names("Play_First"))
    black_label.place(x=16, y=4)
    black_radio0 = ttk.Radiobutton(
        game.root, text=LocaleStr.names(Player.HUMAN),
        value=Player.HUMAN.value, variable=game.tk_vars["black_var"]
    )
    black_radio0.place(x=70, y=4)
    black_radio1 = ttk.Radiobutton(
        game.root, text=LocaleStr.names(Player.AI_RANDUM),
        value=Player.AI_RANDUM.value, variable=game.tk_vars["black_var"]
    )
    black_radio1.place(x=120, y=4)
    black_radio1 = ttk.Radiobutton(
        game.root, text=LocaleStr.names(Player.AI_MINMAX),
        value=Player.AI_MINMAX.value, variable=game.tk_vars["black_var"]
    )
    black_radio1.place(x=240, y=4)
    black_radio1 = ttk.Radiobutton(
        game.root, text=LocaleStr.names(Player.AI_ALPHABETA),
        value=Player.AI_ALPHABETA.value, variable=game.tk_vars["black_var"]
    )
    black_radio1.place(x=320, y=4)

    white_label = ttk.Label(text=LocaleStr.names("Play_Second"))
    white_label.place(x=16, y=24)
    white_radio0 = ttk.Radiobutton(
        game.root, text=LocaleStr.names(Player.HUMAN),
        value=Player.HUMAN.value, variable=game.tk_vars["white_var"]
    )
    white_radio0.place(x=70, y=24)
    white_radio1 = ttk.Radiobutton(
        game.root, text=LocaleStr.names(Player.AI_RANDUM),
        value=Player.AI_RANDUM.value, variable=game.tk_vars["white_var"]
    )
    white_radio1.place(x=120, y=24)
    white_radio1 = ttk.Radiobutton(
        game.root, text=LocaleStr.names(Player.AI_MINMAX),
        value=Player.AI_MINMAX.value, variable=game.tk_vars["white_var"]
    )
    white_radio1.place(x=240, y=24)
    white_radio1 = ttk.Radiobutton(
        game.root, text=LocaleStr.names(Player.AI_ALPHABETA),
        value=Player.AI_ALPHABETA.value, variable=game.tk_vars["white_var"]
    )
    white_radio1.place(x=320, y=24)

    # 「対局開始」ボタンを設置
    button_start = ttk.Button(
        game.root, text=LocaleStr.names("Label_start_game"),
        width=6, command=lambda: play_start(game)
    )
    button_start.place(x=300, y=48)

    mess_label = ttk.Label(game.root, textvariable=game.tk_vars["mess_var"])
    mess_label.place(x=16, y=48)

    button_undo = ttk.Button(
        game.root, text="undo", width=4, command=lambda: play_undo(game)
    )
    button_undo.place(x=18, y=BOARD_PX_SIZE + 90)
    button_redo = ttk.Button(
        game.root, text="redo", width=4, command=lambda: play_redo(game)
    )
    button_redo.place(x=90, y=BOARD_PX_SIZE + 90)
    button_load = ttk.Button(
        game.root, text="load", width=4, command=lambda: play_load(game)
    )
    button_load.place(x=162, y=BOARD_PX_SIZE + 90)
    button_save = ttk.Button(
        game.root, text="save", width=4, command=lambda: play_save(game)
    )
    button_save.place(x=234, y=BOARD_PX_SIZE + 90)

    txt_kifu = tkinter.Entry(
        width=42,
        textvariable=game.tk_vars["kifu_var"]
    )
    txt_kifu.place(x=18, y=BOARD_PX_SIZE + 120)

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

    if not game.get_turn().ai():
        x = math.floor(event.x / CELL_PX_SIZE)
        y = math.floor(event.y / CELL_PX_SIZE)
        if not game.board.is_movable_xy(x, y):
            return

        game.game_move(Position(x=x, y=y))  # 局面を進める
        if game.game_mode == GameState.END:
            return  # 対局終了していたら抜ける

    # 次の手番がコンピュータの場合
    game.proc_machine_turn()


def play_undo(game):
    # TODO:
    pass


def play_redo(game):
    # TODO:
    pass


def play_load(game):
    # TODO:
    pass


def play_save(game):
    # TODO:
    pass


# ------------------------
# メイン処理
# ------------------------
root = tkinter.Tk()
root.title("リバーシ 0.1")
tk_vars = {
    "black_var": tkinter.IntVar(),
    "white_var": tkinter.IntVar(),
    "mess_var": tkinter.StringVar(),
    "kifu_var": tkinter.StringVar()
}
# ウインドウサイズを指定
root.geometry('{}x{}'.format(BOARD_PX_SIZE + 32, BOARD_PX_SIZE + 180))

# 盤面キャンバスを作成
canvas_board = tkinter.Canvas(root, width=BOARD_PX_SIZE, height=BOARD_PX_SIZE)
# キャンバスがクリックされた時に呼び出す関数を設定
canvas_board.bind("<Button-1>", lambda e: click_board(e, game))

game = Game(canvas_board, root, tk_vars)
init_board(game)
game.redraw()        # 盤面を描画
game.disp_message()  # メッセージ表示

root.mainloop()     # GUIの待ち受けループ
