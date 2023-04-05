from __future__ import annotations

from typing import TYPE_CHECKING, Counter, Any

if TYPE_CHECKING:
    from .state import State
    from .symbol import Symbol


class Player:
    def __init__(self, symbol: Symbol):
        self.symbol = symbol
        symbol.owner = self

    def move(self, state: State) -> None:
        raise NotImplementedError

    def finish_game(self, board: State, evaluation: Counter[Player], winner: Player | None) -> None:
        raise NotImplementedError

    def choose_action(self) -> tuple[Any]:
        raise NotImplementedError
