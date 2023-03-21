from ..game_base import BaseGame, BasePlayer, BaseState


class TicTacToe(BaseGame):
    def __init__(self, players: list[BasePlayer], state: BaseState, win_consecutive: int):
        super().__init__(players, state)
        self.win_consecutive: int = win_consecutive

    def winner(self) -> BasePlayer | None:
        pass

    def check_rows(self):
        pass

    def check_columns(self):
        pass

    def check_diagonal_up(self):
        pass

    def check_diagonal_down(self):
        pass

    def game_over(self):
        pass
