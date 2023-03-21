from .state import State
from .symbol import Symbol


class Player:
    def __init__(self, symbol: Symbol):
        self.symbol = symbol

    def play(self, state: State):
        pass