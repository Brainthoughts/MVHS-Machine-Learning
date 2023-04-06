from __future__ import annotations

from typing import TYPE_CHECKING

from examples.game_base import State

if TYPE_CHECKING:
    from .symbol import TicTacToeSymbol


class TicTacToeState(State):
    def print_board(self) -> None:
        for i in range(self.board.shape[0]):
            print("-" * (4 * self.board.shape[1] + 1))
            out = "| "
            for j in range(self.board.shape[1]):
                token: TicTacToeSymbol | str | None = self.board[i, j] or " "
                out += str(token) + " | "
            print(out)

        print("-" * (4 * self.board.shape[1] + 1))
