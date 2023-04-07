from pathlib import Path

import numpy as np
from examples.tic_tac_toe import TicTacToeSymbol, TicTacToeState, TicTacToe
from player import ReinforcementPlayer

BOARD_SIZE = 3
N_TO_WIN = 3
if __name__ == "__main__":
    # player1: HumanPlayer = HumanPlayer(TicTacToeSymbol("x"))
    # player2: HumanPlayer = HumanPlayer(TicTacToeSymbol("o"))
    player1: ReinforcementPlayer = ReinforcementPlayer(TicTacToeSymbol("x"))
    player2: ReinforcementPlayer = ReinforcementPlayer(TicTacToeSymbol("o"))

    p1_policy: Path = Path("./player1")
    p2_policy: Path = Path("./player2")

    print("Loading policies")
    player1.load_policy(p1_policy)
    player2.load_policy(p2_policy)

    BOARD = np.empty((BOARD_SIZE, BOARD_SIZE), dtype=TicTacToeSymbol)
    start_state: TicTacToeState = TicTacToeState(BOARD)
    game: TicTacToe = TicTacToe([player1, player2], start_state, N_TO_WIN)

    print("Starting play")
    for i in range(10):
        game.play(1000)
        print(f"Finished {(i+1)*1000} rounds")

    player1.save_policy(p1_policy)
    player2.save_policy(p2_policy)
