from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING
from collections.abc import Iterable

import numpy as np

from examples.game_base import Game

if TYPE_CHECKING:
    from .player import Player
    from .state import TicTacToeState
    from .symbol import TicTacToeSymbol


class TicTacToe(Game):
    def __init__(self, players: list[Player], state: TicTacToeState, win_consecutive: int) -> None:
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

    def _update_counter(self, spot: TicTacToeSymbol, consecutive: int, last_value: TicTacToeSymbol | None) -> tuple[
        int, TicTacToeSymbol]:
        if spot and spot is last_value:
            consecutive += 1
        elif spot:
            consecutive = 1
        else:
            consecutive = 0
        return consecutive, spot

    def _evaluate_selection(self, selection: Iterable[Iterable[TicTacToeSymbol]]) -> Counter[Player]:
        consecutive: int = 0
        last_value: TicTacToeSymbol | None = None
        evaluation: Counter[Player] = Counter()
        for row in selection:
            for spot in row:
                consecutive, last_value = self._update_counter(spot, consecutive, last_value)
                if consecutive >= self.win_consecutive:
                    evaluation[spot.owner] += 1
            consecutive = 0
        return evaluation

    def winner(self) -> Player | None:
        state_eval: Counter[Player] = self.evaluate_state()
        if len(state_eval.most_common()) != 0:
            return state_eval.most_common()[0][0]
        else:
            return None
