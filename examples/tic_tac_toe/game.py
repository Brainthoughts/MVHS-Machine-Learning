from ..game_base import BaseGame, BasePlayer
from .state import State

class TicTacToe(BaseGame):
    def __init__(self, players: list[BasePlayer], state: State, win_consecutive: int):
        super().__init__(players, state)
        self.win_consecutive: int = win_consecutive

    def winner(self) -> BasePlayer | None:
        # todo: make this work
        winner: BasePlayer | None = None
        self.check_rows()
        self.check_columns()
        self.check_diagonal_up()
        self.check_diagonal_down()
        return winner

    def check_rows(self):
        pass

    def check_columns(self):
        pass

    def check_diagonal_up(self):
        pass

    def check_diagonal_down(self):
        pass
