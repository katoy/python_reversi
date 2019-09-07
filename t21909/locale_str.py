from stone import Stone
from player import Player


class LocaleStr:
    NAMES = {
        "ja": {
            Stone.WHITE: "○", Stone.BLACK: "●",
            Player.HUMAN: "人間", Player.AI_RANDUM: "コンピュータ(ランダム)",
            # Player.VIA_NETWORK: "ネット対戦", Player.MINMAX: "(minmax)",
            "Play_First": "先手●", "Play_Second": "後手○"
        }
    }

    @classmethod
    def names(cls, key):
        return LocaleStr.NAMES["ja"][key]
