from .state import State
from ..game_base import BasePlayer


class HumanPlayer(BasePlayer):
    def play(self, state: State):
        state.print_board()
        action: tuple = self.chose_action()
        state.update(action, self.symbol)

    def chose_action(self) -> tuple:
        return tuple(map(int, input('Coordinate like row, col: ').replace(' ', '').split(',')))
