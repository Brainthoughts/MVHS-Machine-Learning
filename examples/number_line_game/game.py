from __future__ import annotations

from collections import Counter

from examples.game_base import Game, Player, State, Symbol


class LineGame(Game):
    def __init__(self, players: list[Player], state: State):
        super().__init__(players, state)

    def evaluate_state(self) -> Counter[Player]:
        evaluation: Counter[Player] = Counter()
        idx: int
        spot: Symbol | None
        for idx, spot in enumerate(self.state.board):
            if spot and spot.owner:
                evaluation[spot.owner] += idx
        return evaluation

    def winner(self) -> Player | None:
        state_eval: Counter[Player] = self.evaluate_state()
        if len(state_eval.most_common()) != 0:
            return state_eval.most_common()[0][0]  # return highest scoring player
        else:
            return None

    def is_game_over(self) -> bool:
        return len(list(self.state.get_available_positions())) == 0
