from __future__ import annotations

import numpy as np

from examples.game_base import State, Symbol


class LineGameState(State):
    def print_board(self) -> None:
        print("-" * (4 * self.board.shape[0] + 1))
        out1 = "| "
        out2 = "| "
        for i in range(self.board.shape[0]):
            token: Symbol | str | None = self.board[i] or " "
            out1 += str(token) + " | "
            out2 += str(i) + " | "
        print(out1)
        print("-" * (4 * self.board.shape[0] + 1))
        print(out2)
        print("-" * (4 * self.board.shape[0] + 1))

    def get_hash(self) -> str:
        return np.array2string(self.board.reshape(-1), max_line_width=int(np.inf))
