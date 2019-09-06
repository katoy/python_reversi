from enum import Enum


class GameState(Enum):
    # ゲームの状態 開始待ち / 対局中 / 対局終了
    STAY = 1
    PLAYING = 2
    END = 3
