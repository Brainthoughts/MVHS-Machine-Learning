from ..game_base import BaseState, BaseSymbol


class State(BaseState):
    def evaluate(self) -> float:
        score: float = 0
        score += self.evaluate_rows()
        score += self.evaluate_columns()
        score += self.evaluate_diagonal_up()
        score += self.evaluate_diagonal_down()
        return score

def print_board(self):
        for i in range(self.board.shape[0]):
            print('-' * (4 * self.board.shape[1] + 1))
            out = '| '
            for j in range(self.board.shape[1]):
                token: BaseSymbol | None = self.board[i, j] or ' '
                out += str(token) + ' | '
            print(out)
        print('-' * (4 * self.board.shape[1] + 1))

def evaluate_rows():
    pass
    # for row in range(BOARD_SIZE):
    #     consecutive: int = 0
    #     for col in range(BOARD_SIZE):
    #         val = self.board[row, col]
    #         if val == 0:
    #             consecutive = 0
    #         elif consecutive == 0:
    #             consecutive += val
    #         elif consecutive * val > 0:  # same sign so count up/down
    #             consecutive += val
    #         else:  # opposite sign so switch to current symbol
    #             consecutive = val
    #
    #         if consecutive >= WIN_CONSECUTIVE:
    #             self.isEnd = True
    #             return 1
    #         elif consecutive <= -WIN_CONSECUTIVE:
    #             self.isEnd = True
    #             return -1