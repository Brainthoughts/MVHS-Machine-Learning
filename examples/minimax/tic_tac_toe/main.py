import numpy as np

from examples.tic_tac_toe import HumanPlayer, TicTacToeSymbol, TicTacToeState, TicTacToe
from player import MinimaxPlayer


BOARD_SIZE = 3
N_TO_WIN = 3
MAX_DEPTH = 10
if __name__ == "__main__":
    player1: MinimaxPlayer = MinimaxPlayer(TicTacToeSymbol("x"), MAX_DEPTH)
    player2: HumanPlayer = HumanPlayer(TicTacToeSymbol("o"))

    BOARD = np.empty((BOARD_SIZE, BOARD_SIZE), dtype=TicTacToeSymbol)
    start_state: TicTacToeState = TicTacToeState(BOARD)
    game: TicTacToe = TicTacToe([player1, player2], start_state, N_TO_WIN)

    game.play()
