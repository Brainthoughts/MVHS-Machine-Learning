from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .state import State
    from .symbol import Symbol


class Player:
    def __init__(self, symbol: Symbol):
        self.symbol = symbol

    def play(self, state: State):
        pass

    def win(self):
        print(f'Player {self.symbol} wins!')
    def choose_action(self):
        pass