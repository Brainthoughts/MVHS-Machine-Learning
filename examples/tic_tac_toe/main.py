import numpy as np

from examples.tic_tac_toe import HumanPlayer, Symbol, State, TicTacToe

if __name__ == '__main__':
    player1: HumanPlayer = HumanPlayer(Symbol('x'))
    player2: HumanPlayer = HumanPlayer(Symbol('o'))

    start_state: State = State(np.empty((3, 3), dtype=Symbol))
    game: TicTacToe = TicTacToe([player1, player2], start_state, 3)

    game.play()
