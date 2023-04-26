from __future__ import annotations

from collections import Counter

from examples.game_base import Player, State


class HumanPlayer(Player):
    def move(self, state: State) -> None:
        state.print_board()
        action: tuple[int] = self.chose_action()
        state.update(action, self.symbol)

    @staticmethod
    def chose_action() -> tuple[int]:
        choice: int = int(input("Spot: "))
        return (choice,)

    def finish_game(self, state: State, evaluation: Counter[Player], winner: Player | None) -> None:
        state.print_board()
        print(f'Game over: {winner.symbol if winner else "nobody"} wins')
        readable_evaluation: Counter[str] = Counter({str(player.symbol): score for player, score in evaluation.items()})
        print(f'Evaluation: {readable_evaluation}')
