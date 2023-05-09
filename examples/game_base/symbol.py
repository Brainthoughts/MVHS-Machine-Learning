from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .player import Player


class Symbol:
    """
    Base class for symbols.
    A symbol is an object that is placed on the board which may or may not be owned by the player.
    It is usually represented by a character like "X" or "O".
    """
    def __init__(self, text: str) -> None:
        """
        :Example:
        >>> s = Symbol("X")

        :param text: The string representation of the symbol
        """
        self.text: str = text
        self.owner: Player | None = None

    def __str__(self) -> str:
        """
        :Example:
        >>> str(Symbol("X"))
        "X"

        :return: The string representation of the symbol.
        """
        return self.text

    def __repr__(self) -> str:
        return self.text

    def assign_owner(self, player: Player) -> None:
        """
        Assigns the symbol to the given player.
        :param player: The player to assign the symbol to
        :return:
        """
        self.owner = player
