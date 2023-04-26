import numpy as np

from examples.number_line_game import HumanPlayer, LineGameSymbol, LineGameState, LineGame

BOARD_SIZE = 10
if __name__ == "__main__":
    player1: HumanPlayer = HumanPlayer(LineGameSymbol("x"))
    player2: HumanPlayer = HumanPlayer(LineGameSymbol("o"))

    BOARD = np.empty(BOARD_SIZE, dtype=LineGameSymbol)
    start_state: LineGameState = LineGameState(BOARD)
    game: LineGame = LineGame([player1, player2], start_state)

    game.play()
