from collections import Counter

import numpy as np

from examples.game_base import Player, Symbol, State


class MinimaxPlayer(Player):
    def __init__(self, symbol: Symbol, max_depth: int) -> None:
        super().__init__(symbol)
        self.max_depth: int = max_depth

    def move(self, state: State) -> None:
        max_eval: float = -np.Infinity
        action: tuple[int, int]
        for next_position in state.get_available_positions():
            state.update(next_position, self.symbol)
            evaluation: Counter[Player] = minimax(state, self.max_depth - 1, state.player_turn + 1)
            state.update(next_position, None)
            if max_eval < (new_max_eval := max(max_eval, 2*evaluation[self] - evaluation.total())):
                max_eval = new_max_eval
                action = next_position

        state.update(action, self.symbol)

    def finish_game(self, board: State, evaluation: Counter[Player], winner: Player | None) -> None:
        pass


def minimax(state: State, depth: int, playing_player_num: int) -> Counter[Player]:
    if depth == 0 or state.game.is_game_over():
        static_eval: Counter[Player] = state.game.evaluate_state()
        return static_eval

    playing_player: Player = state.game.players[playing_player_num % len(state.game.players)]  # todo make this less bad
    max_eval = -np.Infinity
    final_evaluation: Counter[Player] = Counter()
    for next_position in state.get_available_positions():
        state.update(next_position, playing_player.symbol)
        evaluation = minimax(state, depth - 1, playing_player_num + 1)
        state.update(next_position, None)
        if max_eval < (new_max_eval := max(max_eval, 2*evaluation[playing_player] - evaluation.total())):
            max_eval = new_max_eval
            final_evaluation = evaluation

    return final_evaluation
