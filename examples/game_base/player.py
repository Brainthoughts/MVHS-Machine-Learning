from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # prevents circular imports
    from .state import State
    from .symbol import Symbol


class Player:
    """
    Abstract class for a player.
    """
    def __init__(self, symbol: Symbol) -> None:
        """
        :param symbol: The symbol of the player
        """
        self.symbol = symbol
        symbol.owner = self

    def move(self, state: State) -> None:
        """
        Called when it is this player's turn to move.
        :param state: The state of the game. Should be updated in this method.
        :return:
        """
        raise NotImplementedError

    def finish_game(self, board: State, evaluation: Counter[Player], winner: Player | None) -> None:
        """
        Called when the game is over.
        :param board: The state of the game.
        :param evaluation: The evaluation of the game.
        :param winner: The winner of the game.
        :return:
        """
        raise NotImplementedError
