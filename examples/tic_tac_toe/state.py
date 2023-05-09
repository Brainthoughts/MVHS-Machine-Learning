from __future__ import annotations

import numpy as np

from examples.game_base import State, Symbol


class TicTacToeState(State):
    def print_board(self) -> None:
        for i in range(self.board.shape[0]):
            print("-" * (4 * self.board.shape[1] + 1))
            out = "| "
            for j in range(self.board.shape[1]):
                token: Symbol | str | None = self.board[i, j] or " "
                out += str(token) + " | "
            print(out)

        print("-" * (4 * self.board.shape[1] + 1))

    def get_hash(self) -> str:
        return np.array2string(self.board.reshape(-1), max_line_width=int(np.inf))
