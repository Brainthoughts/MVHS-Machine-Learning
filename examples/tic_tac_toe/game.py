from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from typing import cast

import numpy as np

from examples.game_base import Game, Player, State, Symbol


class TicTacToe(Game):
    def __init__(self, players: list[Player], state: State, win_consecutive: int) -> None:
        super().__init__(players, state)
        self.win_consecutive: int = win_consecutive

    def evaluate_state(self) -> Counter[Player]:
        evaluation: Counter[Player] = Counter()
        evaluation += self._evaluate_selection(self.state.board)
        evaluation += self._evaluate_selection(self.state.board.T)
        evaluation += self._evaluate_selection([np.diag(self.state.board, k=offset) for offset in
                                                range(-(self.state.board.shape[0] - self.win_consecutive),
                                                      self.state.board.shape[0] - self.win_consecutive + 1)])
        evaluation += self._evaluate_selection([np.diag(np.fliplr(self.state.board), k=offset) for offset in
                                                range(-(self.state.board.shape[0] - self.win_consecutive),
                                                      self.state.board.shape[0] - self.win_consecutive + 1)])
        return evaluation

    def _update_counter(self, spot: Symbol, consecutive: int, last_value: Symbol | None) -> tuple[int, Symbol]:
        if spot and spot is last_value:
            consecutive += 1
        elif spot:
            consecutive = 1
        else:
            consecutive = 0
        return consecutive, spot

    def _evaluate_selection(self, selection: Iterable[Iterable[Symbol]]) -> Counter[Player]:
        consecutive: int = 0
        last_value: Symbol | None = None
        evaluation: Counter[Player] = Counter()
        for row in selection:
            for spot in row:
                consecutive, last_value = self._update_counter(spot, consecutive, last_value)
                if consecutive >= self.win_consecutive:
                    evaluation[cast(Player, spot.owner)] += 1  # cast needed for type checking
            consecutive = 0
        return evaluation

    def winner(self) -> Player | None:
        state_eval: Counter[Player] = self.evaluate_state()
        if len(state_eval.most_common()) != 0:
            return state_eval.most_common()[0][0]
        else:
            return None
