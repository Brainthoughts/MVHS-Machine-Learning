from __future__ import annotations

from collections.abc import Generator
from copy import deepcopy
from typing import TYPE_CHECKING, Any

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:  # prevents circular imports
    from .symbol import Symbol
    from .player import Player
    from .game import Game


class State:
    """
    Abstract class for the state of the game.
    Represents the state of the game.
    """
    def __init__(self, board: NDArray[np.object_]) -> None:
        """
        :param board: An n-dimensional numpy array
        """
        self.board: NDArray[np.object_] = board
        self.player_turn: int = 0
        self.game: Game | None = None
        self.original_state = self.__getstate__()

    def __getstate__(self) -> dict[str, Any]:
        """
        :return: A dictionary of the state object
        """
        return deepcopy(self.__dict__)

    def __setstate__(self, state: dict[str, Any]) -> None:
        """

        :param state: A dictionary of the state object
        :return:
        """
        assert self.game is not None, "Game instance not set"
        game: Game = self.game
        self.__dict__ = state
        self.original_state = self.__getstate__()
        self.game = game

    def set_game(self, game: Game) -> None:
        """
        Sets the game instance for the state.
        :param game: The instance of the game being played
        :return: 
        """
        self.game = game

    def get_hash(self) -> str:
        """
        :return: A hash of the state
        """
        raise NotImplementedError

    def update(self, position: tuple[Any, ...], symbol: Symbol | None) -> None:
        """
        Updates the state of the board.
        :param position: The position to update
        :param symbol: The symbol to update the position with
        :return:
        """
        self.board[position] = symbol

    def reset(self) -> None:
        """
        Resets the state to its original state.
        :return:
        """
        self.__setstate__(self.original_state)

    def change_turn(self, players: list[Player]) -> None:
        """
        Called to change the current turn
        :param players: A list of Players
        :return:
        """
        self.player_turn += 1
        if self.player_turn >= len(players):
            self.player_turn = 0

    def get_current_player(self) -> Player:
        """
        :return: Current Player
        """
        assert self.game is not None, "Game instance not set"
        return self.game.players[self.player_turn]

    def get_available_positions(self) -> Generator[tuple[int, ...], None, None]:
        """
        Get open board positions
        :return: A generator of available positions on the board
        """
        for position, value in np.ndenumerate(self.board):
            if value is None:
                yield position

    def print_board(self) -> None:
        """
        Prints the board in a human-readable format
        :return:
        """
        raise NotImplementedError
