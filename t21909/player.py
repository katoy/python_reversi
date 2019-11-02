from enum import Enum
import ai_randum
import ai_minmax
import ai_alphabeta


class Player(Enum):
    HUMAN = 0
    # VIA_NETWORK = -1
    AI_RANDUM = 1
    AI_MINMAX = 2
    AI_ALPHABETA = 3

    def ai(self):
        if self.name == "AI_RANDUM":
            return ai_randum.AI()
        if self.name == "AI_MINMAX":
            return ai_minmax.AI()
        if self.name == "AI_ALPHABETA":
            return ai_alphabeta.AI()
        return None
