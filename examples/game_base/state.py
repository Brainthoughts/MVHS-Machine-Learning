from __future__ import annotations

from copy import deepcopy
from typing import Generator, TYPE_CHECKING, Any

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from .symbol import Symbol
    from .player import Player
    from .game import Game


class State:
    def __init__(self, board: NDArray):
        self.board: NDArray = board
        self.player_turn: int = 0
        self.game: Game | None = None
        self.original_state = self.__getstate__()

    def __getstate__(self) -> dict[str, Any]:
        return deepcopy(self.__dict__)

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__ = state
        self.original_state = self.__getstate__()

    def set_game(self, game: Game) -> None:
        self.game = game

    def get_hash(self) -> str:
        return self.__repr__()

    def update(self, position: tuple[Any], symbol: Symbol) -> None:
        self.board[position] = symbol

    def reset(self) -> None:
        self.__setstate__(self.original_state)

    def change_turn(self, players: list[Player]) -> None:
        self.player_turn += 1
        if self.player_turn >= len(players):
            self.player_turn = 0

    def get_current_player(self, players: list[Player]) -> Player:
        return players[self.player_turn]

    def get_available_positions(self) -> Generator[tuple[int, ...], None, None]:
        for position, value in np.ndenumerate(self.board):
            if value is None:
                yield position

    def print_board(self) -> None:
        for i in range(self.board.shape[0]):
            print('-' * (4 * self.board.shape[1] + 1))
            out = '| '
            for j in range(self.board.shape[1]):
                token: Symbol | str | None = self.board[i, j] or ' '
                out += str(token) + ' | '
            print(out)

        print('-' * (4 * self.board.shape[1] + 1))
