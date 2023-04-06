from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .player import Player
    from .state import State


class Game:
    def __init__(self, players: list[Player], state: State) -> None:
        self.state: State = state
        self.state.set_game(self)
        self.players: list[Player] = players

    def play(self, rounds: int = 1) -> None:
        for _round_num in range(rounds):
            while not self.is_game_over():
                self.state.get_current_player(self.players).move(self.state)
                self.state.change_turn(self.players)
            self.game_over()

    def evaluate_state(self) -> Counter[Player]:
        raise NotImplementedError

    def winner(self) -> Player | None:
        raise NotImplementedError

    def is_game_over(self) -> bool:
        return self.winner() is not None or sum(1 for _ in self.state.get_available_positions()) == 0

    def game_over(self) -> None:
        for player in self.players:
            player.finish_game(self.state, self.evaluate_state(), self.winner())
        self.state.reset()
