from ..game_base import BaseState
from .symbol import Symbol


class State(BaseState):
    def update(self, position: tuple, symbol: Symbol) -> None:
        self.board[position] = symbol

    def reset(self) -> None:
        pass

    def evaluate(self) -> float:
        pass

    def print_board(self):
        for i in range(self.board.shape[0]):
            print('-' * (4 * self.board.shape[1] + 1))
            out = '| '
            for j in range(self.board.shape[1]):
                token = self.board[i, j] or ' '
                out += token + ' | '
            print(out)
        print('-' * (4 * self.board.shape[1] + 1))
