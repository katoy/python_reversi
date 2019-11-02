from stone import Stone
from player import Player


class LocaleStr:
    NAMES = {
        "ja": {
            Stone.WHITE: "○", Stone.BLACK: "●",
            Player.HUMAN: "人間",
            Player.AI_RANDUM: "マシン(ランダム)",
            # Player.VIA_NETWORK: "ネット対戦",
            Player.AI_MINMAX: "(minmax)",
            Player.AI_ALPHABETA: "(αβ)",
            "Play_First": "先手●", "Play_Second": "後手○",
            "Label_start_game": "対局開始",
            "Label_end_game": "対局終了"
        }
    }

    @classmethod
    def names(cls, key):
        return LocaleStr.NAMES["ja"][key]
