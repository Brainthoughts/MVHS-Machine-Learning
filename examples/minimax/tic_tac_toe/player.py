from collections import Counter
from random import choice

import numpy as np

from examples.game_base import Player, Symbol, State


class MinimaxPlayer(Player):
    def __init__(self, symbol: Symbol, max_depth: int) -> None:
        super().__init__(symbol)
        self.max_depth: int = max_depth

    def move(self, state: State) -> None:
        max_eval: float = -np.Infinity
        action: tuple[int, ...]
        should_minimax: bool = False
        for next_position in state.get_available_positions():
            state.update(next_position, self.symbol)
            evaluation: Counter[Player] = self.minimax(state, self.max_depth - 1, state.player_turn + 1)
            if evaluation.total() != 0:  # if it found absolutely nothing just pick a random spot
                should_minimax = True
            state.update(next_position, None)
            if max_eval < (new_max_eval := max(max_eval, 2 * evaluation[self] - evaluation.total())):
                max_eval = new_max_eval
                action = next_position

        if not should_minimax:
            action = choice(list(state.get_available_positions()))
        print(f"Minimax: {max_eval}")
        state.update(action, self.symbol)

    def finish_game(self, board: State, evaluation: Counter[Player], winner: Player | None) -> None:
        pass

    def minimax(self, state: State, depth: int, playing_player_num: int) -> Counter[Player]:
        assert state.game is not None
        if depth == 0 or state.game.is_game_over():
            static_eval: Counter[Player] = state.game.evaluate_state()
            return static_eval

        playing_player: Player = state.game.players[
            playing_player_num % len(state.game.players)]  # todo make this less bad
        max_eval = -np.Infinity
        final_evaluation: Counter[Player] = Counter()
        for next_position in state.get_available_positions():
            state.update(next_position, playing_player.symbol)
            evaluation = self.minimax(state, depth - 1, playing_player_num + 1)
            state.update(next_position, None)
            if max_eval < (new_max_eval := max(max_eval, 2 * evaluation[playing_player] - evaluation.total())):
                max_eval = new_max_eval
                final_evaluation = evaluation

        return final_evaluation


class MinimaxBiasPlayer(MinimaxPlayer):
    def __init__(self, symbol: Symbol, max_depth: int, bias_multiplier: float = .01) -> None:
        super().__init__(symbol, max_depth)
        self.bias_multiplier: float = bias_multiplier

    def move(self, state: State) -> None:
        max_eval: float = -np.Infinity
        action: tuple[int, ...]
        should_minimax: bool = False
        for next_position in state.get_available_positions():
            state.update(next_position, self.symbol)
            evaluation: Counter[Player] = self.minimax(state, self.max_depth - 1, state.player_turn + 1)
            if evaluation.total() != 0:  # if it found absolutely nothing just pick a random spot
                should_minimax = True
            state.update(next_position, None)
            if max_eval < (new_max_eval := max(max_eval, 2 * evaluation[self] - evaluation.total())):
                max_eval = new_max_eval
                action = next_position
        print(f"Minimax: {max_eval}")

        if not should_minimax:
            action = choice(list(state.get_available_positions()))

        state.update(action, self.symbol)
        # state.print_board()

    def minimax(self, state: State, depth: int, playing_player_num: int) -> Counter[Player]:
        assert state.game is not None
        if depth == 0 or state.game.is_game_over():
            static_eval: Counter[Player] = state.game.evaluate_state()
            return static_eval

        playing_player: Player = state.game.players[
            playing_player_num % len(state.game.players)]  # todo make this less bad
        max_eval = -np.Infinity
        final_evaluation: Counter[Player] = Counter()
        bias: Counter[Player] = Counter()
        for next_position in state.get_available_positions():
            state.update(next_position, playing_player.symbol)
            evaluation = self.minimax(state, depth - 1, playing_player_num + 1)
            bias += evaluation
            state.update(next_position, None)
            if max_eval < (new_max_eval := max(max_eval, 2 * evaluation[playing_player] - evaluation.total())):
                max_eval = new_max_eval
                final_evaluation = evaluation

        for key in bias.keys():
            bias[key] *= self.bias_multiplier

        return final_evaluation + bias
