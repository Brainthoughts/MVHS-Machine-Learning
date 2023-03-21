from .player import Player


class Symbol:
    def __init__(self, text: str):
        self.text = text
        self.owner = None

    def __str__(self) -> str:
        return self.text

    def assign_owner(self, player: Player) -> None:
        self.owner = player
