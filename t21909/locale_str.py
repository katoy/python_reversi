from stone import Stone
from player import Player


class LocaleStr:
    JA_NAMES = {
        Stone.WHITE: "白", Stone.BLACK: "黒",
        Player.HUMAN: "人間", Player.AI_RANDUM: "コンピュータ(ランダム)",
        # Player.VIA_NETWORK: "ネット対戦", Player.MINMAX: "(minmax)",
        "Play_First": "先手●", "Play_Second": "後手○"
    }
