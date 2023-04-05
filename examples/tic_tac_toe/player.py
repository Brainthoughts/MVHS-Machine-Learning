from __future__ import annotations

from typing import Counter, Any

from examples.game_base import Player
from .state import TicTacToeState
from .symbol import TicTacToeSymbol


class HumanPlayer(Player):
    def move(self, state: TicTacToeState) -> None:
        state.print_board()
        action: tuple = self.chose_action()
        state.update(action, self.symbol)

    def chose_action(self) -> tuple:
        return tuple(map(int, input('Coordinate like row, col: ').replace(' ', '').split(',')))

    def finish_game(self, state: TicTacToeState, evaluation: Counter[Player], winner: Player | None):
        state.print_board()
        print(f'Game over: {winner.symbol if winner else "nobody"} wins')


class ReinforcementPlayer(Player):
    def __init__(self, symbol: TicTacToeSymbol, exp_rate: float = 0.3, learn_rate: float = .2, decay_gamma: float = .9):
        super().__init__(symbol)
        self.states: list = []  # record all positions taken
        self.learn_rate = learn_rate
        self.exp_rate = exp_rate
        self.decay_gamma = decay_gamma
        self.states_value: dict[str, Any] = {}  # state -> value
