from __future__ import annotations

from collections import Counter
from typing import Any

import numpy as np
from numpy.typing import NDArray

from examples.game_base import Player, State, Symbol


class HumanPlayer(Player):
    def move(self, state: State) -> None:
        state.print_board()
        action: tuple[int, int] = self.chose_action()
        state.update(action, self.symbol)

    def chose_action(self) -> tuple[int, int]:
        choice: tuple[int, ...] = tuple(map(int, input("Coordinate like row, col: ").replace(" ", "").split(",")))
        return choice[0], choice[1]

    def finish_game(self, state: State, evaluation: Counter[Player], winner: Player | None) -> None:
        state.print_board()
        print(f'Game over: {winner.symbol if winner else "nobody"} wins')


class ReinforcementPlayer(Player):
    def __init__(self, symbol: Symbol, exp_rate: float = 0.3, learn_rate: float = .2,
                 decay_gamma: float = .9) -> None:
        super().__init__(symbol)
        self.states: list[NDArray[np.object_]] = []  # record all positions taken
        self.learn_rate = learn_rate
        self.exp_rate = exp_rate
        self.decay_gamma = decay_gamma
        self.states_value: dict[str, Any] = {}  # state -> value
