from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .player import Player


class Symbol:
    def __init__(self, text: str):
        self.text: str = text
        self.owner: Player | None = None

    def __str__(self) -> str:
        return self.text

    def assign_owner(self, player: Player) -> None:
        self.owner = player
