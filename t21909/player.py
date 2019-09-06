from enum import Enum
import ai_randum


class Player(Enum):
    HUMAN = 0
    # VIA_NETWORK = -1
    AI_RANDUM = 1
    # AI_MINMAX = 2
    # AI_ALPHA = 3

    def get_ai(self):
        if self.name == "AI_RANDUM":
            return ai_randum.AI()
