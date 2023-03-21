from __future__ import annotations
from typing import Generator, TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from .symbol import Symbol
    from .player import Player


class State:
    def __init__(self, board: NDArray):
        self.board = board
        self.player_turn = 0
        self.original_state = self.__getstate__()

    def __getstate__(self) -> dict:
        return self.__dict__

    def __setstate__(self, state: dict):
        self.__dict__.update(state)
        self.original_state = self.__getstate__()

    def get_hash(self) -> str:
        return self.__repr__()

    def evaluate(self) -> float:
        raise NotImplementedError

    def update(self, position: tuple, symbol: Symbol) -> None:
        self.board[position] = symbol

    def reset(self) -> None:
        self.__setstate__(self.original_state)

    def change_turn(self, players: list[Player]) -> None:
        self.player_turn += 1
        if self.player_turn >= len(players):
            self.player_turn = 0

    def get_current_player(self, players: list[Player]) -> Player:
        return players[self.player_turn]

    def get_available_positions(self) -> Generator[tuple[int]]:
        for position, value in np.ndenumerate(self.board):
            if value is None:
                yield position

    def print_board(self):
        raise NotImplementedError
