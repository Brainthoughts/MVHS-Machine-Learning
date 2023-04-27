from __future__ import annotations

from collections import Counter

from examples.game_base import Player, State


class HumanPlayer(Player):
    def move(self, state: State) -> None:
        state.print_board()
        action: tuple[int, int] = self.chose_action()
        state.update(action, self.symbol)

    @staticmethod
    def chose_action() -> tuple[int, int]:
        choice: tuple[int, ...] = tuple(map(int, input("Coordinate like row, col: ").replace(" ", "").split(",")))
        return choice[0], choice[1]

    def finish_game(self, state: State, evaluation: Counter[Player], winner: Player | None) -> None:
        state.print_board()
        print(f'Game over: {winner.symbol if winner else "nobody"} wins')
