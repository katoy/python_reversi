from enum import Enum


class Stone(Enum):
    SPACE = 0   # 空き
    BLACK = 1   # 黒石
    WHITE = -1  # 白石
    MARK = 9    # おける場所のマーク

    def invert(self):
        return Stone(self.value * (-1))

    def color(self):
        colors = {
            Stone.SPACE: "#00a000",
            Stone.BLACK: "black",
            Stone.WHITE: "white"
        }
        return colors[self]
