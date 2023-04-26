from pathlib import Path

import numpy as np

from examples.number_line_game import HumanPlayer, LineGameSymbol, LineGameState, LineGame
from examples.reinforcement_learning.number_line_game.player import ReinforcementPlayer

BOARD_SIZE = 10
if __name__ == "__main__":
    # player1: HumanPlayer = HumanPlayer(LineGameSymbol("x"))
    # player2: HumanPlayer = HumanPlayer(LineGameSymbol("o"))
    player1: ReinforcementPlayer = ReinforcementPlayer(LineGameSymbol("x"))
    player2: ReinforcementPlayer = ReinforcementPlayer(LineGameSymbol("o"))

    p1_policy: Path = Path("./player1")
    p2_policy: Path = Path("./player2")

    # print("Loading policies")  # enable this once policies have been created
    # player1.load_policy(p1_policy)
    # player2.load_policy(p2_policy)

    BOARD = np.empty(BOARD_SIZE, dtype=LineGameSymbol)
    start_state: LineGameState = LineGameState(BOARD)
    game: LineGame = LineGame([player1, player2], start_state)

    print("Starting play")
    for i in range(10):
        game.play(1000)
        print(f"Finished {(i+1)*1000} rounds")

    player1.save_policy(p1_policy)
    player2.save_policy(p2_policy)
