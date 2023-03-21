from .player import Player
from .state import State


class Game:
    def __init__(self, players: list[Player], state: State):
        self.state: State = state
        self.players: list[Player] = players

    def play(self) -> None:
        while not self.is_game_over():
            self.state.get_current_player(self.players).play(self.state)
            self.state.change_turn(self.players)
            if self.is_game_over():
                self.game_over()

    def winner(self) -> int | None:
        raise NotImplementedError

    def is_game_over(self) -> bool:
        return self.winner() is not None or sum(1 for _ in self.state.get_available_positions()) == 0

    def game_over(self):
        pass
