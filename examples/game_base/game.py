from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # prevents circular imports
    from .player import Player
    from .state import State


class Game:
    """
    Abstract class for a game.
    The Game class is the main class of the game. It is responsible for the game logic.
    """

    def __init__(self, players: list[Player], state: State) -> None:
        """

        :param players: The list of players in the game.
        :param state: The initial state of the game.

        :Example:

        >>> game = Game(players, state)
        """

        self.state: State = state
        self.state.set_game(self)
        self.players: list[Player] = players

    def play(self, rounds: int = 1) -> None:
        """
        :param rounds: The number of rounds to play the game. Default is 1.
        :return:

        This method plays the game for the given number of rounds.

        :Example:

        >>> game = Game(players, state)
        >>> game.play()

        :Example:

        >>> game = Game(players, state)
        >>> game.play(2)
        """
        for _round_num in range(rounds):
            while not self.is_game_over():
                self.state.get_current_player().move(self.state)
                self.state.change_turn(self.players)
            self.game_over()

    def evaluate_state(self) -> Counter[Player]:
        """
        Evaluates the current state of the game into a Counter of the players and their scores.

        :Example:

        >>> game = Game(players, state)
        >>> game.evaluate_state()
        Counter({player1: 1, player2: 0})

        :return: A Counter of the players and their scores.
        """
        raise NotImplementedError

    def winner(self) -> Player | None:
        """
        Returns the winner of the game.

        :Example:

        >>> game = Game(players, state)
        >>> game.winner()
        player1

        :return: The winner of the game or None if there is no winner yet.
        """
        raise NotImplementedError

    def is_game_over(self) -> bool:
        """
        Returns True if the game is over, False otherwise.

        :Example:

        >>> game = Game(players, state)
        >>> game.is_game_over()
        False

        :return: True if the game is over, False otherwise.
        """
        return self.winner() is not None or len(list(self.state.get_available_positions())) == 0

    def game_over(self) -> None:
        """
        This method is called automatically when the game is over. It is responsible for calling the finish_game method
        of all players.

        :return:
        """
        for player in self.players:
            player.finish_game(self.state, self.evaluate_state(), self.winner())
        self.state.reset()
