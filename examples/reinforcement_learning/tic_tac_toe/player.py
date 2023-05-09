import pickle
from collections import Counter, defaultdict
from pathlib import Path
from random import choice
from typing import cast
from collections.abc import Generator

import numpy as np

from examples.game_base import Player, Symbol, State


class ReinforcementPlayer(Player):
    def __init__(self, symbol: Symbol, exp_rate: float = 0.3, learn_rate: float = .2,
                 decay_gamma: float = .9) -> None:
        super().__init__(symbol)
        self.states: list[str] = []  # record all positions taken
        self.learn_rate = learn_rate
        self.exp_rate = exp_rate
        self.decay_gamma = decay_gamma
        self.states_value: defaultdict[str, float] = defaultdict(float)

    def move(self, state: State) -> None:
        action: tuple[int, int]
        if np.random.default_rng().uniform(0, 1.) < self.exp_rate:
            action = cast(tuple[int, int], choice(list(state.get_available_positions())))
        else:
            action = self.reinforcement_move(state)
        state.update(action, self.symbol)
        self.states.append(state.get_hash())

    def reinforcement_move(self, state: State) -> tuple[int, int]:
        positions: Generator[tuple[int, ...], None, None] = state.get_available_positions()
        highest_eval: float = -np.inf
        action: tuple[int, int]
        for position in positions:
            state.update(position, self.symbol)
            if highest_eval < (new_eval := self.states_value.get(state.get_hash()) or 0):
                highest_eval = new_eval
                action = position[0], position[1]
            state.update(position, None)

        return action

    def finish_game(self, board: State, evaluation: Counter[Player], winner: Player | None) -> None:
        reward: float = evaluation[self] - (evaluation[winner] if winner and self is not winner else 0)
        for state in reversed(self.states):
            self.states_value[state] += self.learn_rate * reward
            reward *= self.decay_gamma
        self.states = []

    def save_policy(self, path: Path) -> None:
        with open(path, "wb") as file:
            pickle.dump(self.states_value, file)

    def load_policy(self, path: Path) -> None:
        with open(path, "rb") as file:
            self.states_value.update(pickle.load(file))
