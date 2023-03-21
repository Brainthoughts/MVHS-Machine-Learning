import numpy as np
from numpy.typing import NDArray
from typing import Generator
from .player import Player
from .symbol import Symbol


class State:
    def __init__(self, board: NDArray):
        self.board = board
        self.player_turn = 0

    def get_hash(self) -> str:
        return self.__repr__()

    def evaluate(self) -> float:
        raise NotImplementedError

    def update(self, position: tuple, symbol: Symbol) -> None:
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError

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
