import pickle
from pathlib import Path

import numpy as np

from examples.tic_tac_toe import HumanPlayer, TicTacToeSymbol, TicTacToeState, TicTacToe
from player import MinimaxPlayer, MinimaxBiasPlayer, MinimaxBiasReinforcementPlayer


BOARD_SIZE = 3
N_TO_WIN = 3
MAX_DEPTH = 10  # change to lower values the bigger the board gets, like 3 or 4 for a 5x5 board
if __name__ == "__main__":
    human: HumanPlayer = HumanPlayer(TicTacToeSymbol("o"))

    minimax: MinimaxPlayer = MinimaxPlayer(TicTacToeSymbol("x"), MAX_DEPTH)

    # minimax_bias: MinimaxBiasPlayer = MinimaxBiasPlayer(TicTacToeSymbol("x"), MAX_DEPTH)

    # move trained policy from reinforcement learning over to use it here
    # make sure this player and the player of the policy you copied have the same symbol (both 'x' or both 'o')
    # policy: dict[str, float] = pickle.load(open(Path("./player1_5x"), "rb"))
    # minimax_bias_reinforcement: MinimaxBiasReinforcementPlayer = MinimaxBiasReinforcementPlayer(TicTacToeSymbol("x"), MAX_DEPTH, trained_weights=policy)

    BOARD = np.empty((BOARD_SIZE, BOARD_SIZE), dtype=TicTacToeSymbol)
    start_state: TicTacToeState = TicTacToeState(BOARD)
    game: TicTacToe = TicTacToe([minimax, human], start_state, N_TO_WIN)

    game.play()
