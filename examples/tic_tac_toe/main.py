import numpy as np

from examples.tic_tac_toe import HumanPlayer, TicTacToeSymbol, TicTacToeState, TicTacToe

BOARD_SIZE = 3
N_TO_WIN = 3
if __name__ == "__main__":
    player1: HumanPlayer = HumanPlayer(TicTacToeSymbol("x"))
    player2: HumanPlayer = HumanPlayer(TicTacToeSymbol("o"))

    BOARD = np.empty((BOARD_SIZE, BOARD_SIZE), dtype=TicTacToeSymbol)
    start_state: TicTacToeState = TicTacToeState(BOARD)
    game: TicTacToe = TicTacToe([player1, player2], start_state, N_TO_WIN)

    game.play()
