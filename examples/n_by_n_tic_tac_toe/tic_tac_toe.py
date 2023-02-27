import sys
import numpy as np
import pickle
"""
Set BOARD_SIZE and WIN_CONSECUTIVE to same values as they were trained with.
Set MAX_DEPTH to desired value. The larger it is the better the computer will play, BUT the time it takes 
to do so grows exponentially. For ever 1 you increase it by, it will take ~BOARD_SIZE^2 longer 
(so for a 5x5 grid it will take about 25 times longer for a number 1 bigger)
A reasonable value is around 3

Scroll down to the bottom to toggle on/off using minimax as well as set a custom starting board.
"""
BOARD_SIZE = 5
WIN_CONSECUTIVE = 4
MAX_DEPTH = 3
BIAS_MULTIPLIER = .01
player, opponent = 1, -1

class State:
    def __init__(self, p1, p2, board=np.zeros((BOARD_SIZE, BOARD_SIZE))):
        self.board = board
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHash = None
        # init p1 plays first
        self.playerSymbol = 1
        self.should_minimax = False

    # get unique hash of current board state
    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_SIZE * BOARD_SIZE))
        return self.boardHash

    def winner(self):
        # row
        for row in range(BOARD_SIZE):
            consecutive: int = 0
            for col in range(BOARD_SIZE):
                val = self.board[row, col]
                if val == 0:
                    consecutive = 0
                elif consecutive == 0:
                    consecutive += val
                elif consecutive * val > 0:  # same sign so count up/down
                    consecutive += val
                else:  # opposite sign so switch to current symbol
                    consecutive = val

                if consecutive >= WIN_CONSECUTIVE:
                    self.isEnd = True
                    return 1
                elif consecutive <= -WIN_CONSECUTIVE:
                    self.isEnd = True
                    return -1
        # col
        for col in range(BOARD_SIZE):
            consecutive: int = 0
            for row in range(BOARD_SIZE):
                val = self.board[row, col]
                if val == 0:
                    consecutive = 0
                elif consecutive == 0:
                    consecutive += val
                elif consecutive * val > 0:  # same sign so count up/down
                    consecutive += val
                else:  # opposite sign so switch to current symbol
                    consecutive = val

                if consecutive >= WIN_CONSECUTIVE:
                    self.isEnd = True
                    return 1
                elif consecutive <= -WIN_CONSECUTIVE:
                    self.isEnd = True
                    return -1
        # diagonal slope down
        for row in range(BOARD_SIZE - (WIN_CONSECUTIVE - 1)):  # all possible diag lines
            consecutive: int = 0
            for i in range(BOARD_SIZE - row):
                val = self.board[row + i, i]
                if val == 0:
                    consecutive = 0
                elif consecutive == 0:
                    consecutive += val
                elif consecutive * val > 0:  # same sign so count up/down
                    consecutive += val
                else:  # opposite sign so switch to current symbol
                    consecutive = val

                if consecutive >= WIN_CONSECUTIVE:
                    self.isEnd = True
                    return 1
                elif consecutive <= -WIN_CONSECUTIVE:
                    self.isEnd = True
                    return -1

            if row != 0:
                consecutive = 0
                for i in range(BOARD_SIZE - row):
                    val = self.board[i, row + i]
                    if val == 0:
                        consecutive = 0
                    elif consecutive == 0:
                        consecutive += val
                    elif consecutive * val > 0:  # same sign so count up/down
                        consecutive += val
                    else:  # opposite sign so switch to current symbol
                        consecutive = val

                    if consecutive >= WIN_CONSECUTIVE:
                        self.isEnd = True
                        return 1
                    elif consecutive <= -WIN_CONSECUTIVE:
                        self.isEnd = True
                        return -1

        # diagonal slope up
        for row in range(BOARD_SIZE - (WIN_CONSECUTIVE - 1)):  # all possible diag lines
            consecutive: int = 0
            for i in range(BOARD_SIZE - row):
                val = self.board[BOARD_SIZE - row - i - 1, i]
                if val == 0:
                    consecutive = 0
                elif consecutive == 0:
                    consecutive += val
                elif consecutive * val > 0:  # same sign so count up/down
                    consecutive += val
                else:  # opposite sign so switch to current symbol
                    consecutive = val

                if consecutive >= WIN_CONSECUTIVE:
                    self.isEnd = True
                    return 1
                elif consecutive <= -WIN_CONSECUTIVE:
                    self.isEnd = True
                    return -1

            if row != 0:
                consecutive = 0
                for i in range(BOARD_SIZE - row):
                    val = self.board[BOARD_SIZE - row - i, i + 1]
                    if val == 0:
                        consecutive = 0
                    elif consecutive == 0:
                        consecutive += val
                    elif consecutive * val > 0:  # same sign so count up/down
                        consecutive += val
                    else:  # opposite sign so switch to current symbol
                        consecutive = val

                    if consecutive >= WIN_CONSECUTIVE:
                        self.isEnd = True
                        return 1
                    elif consecutive <= -WIN_CONSECUTIVE:
                        self.isEnd = True
                        return -1

        # tie
        # no available positions
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return None
        # not end
        self.isEnd = False
        return 0

    def availablePositions(self):
        positions = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i, j] == 0:
                    positions.append((i, j))  # need to be tuple
        return positions

    def updateState(self, position):
        self.board[position] = self.playerSymbol
        # switch to another player
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    # only when game ends
    def giveReward(self):
        result = self.winner()
        # backpropagate reward
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(-.8)
        elif result == -1:
            self.p1.feedReward(-.8)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)

    # board reset
    def reset(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    def play(self, rounds=sys.maxsize):
        for i in range(rounds):
            if i % 1000 == 0:
                print("Rounds {}".format(i))
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                # take action and upate board state
                self.updateState(p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)
                # check board status if it is end

                win = self.winner()
                if win is not None:
                    # self.showBoard()
                    # ended with p1 either win or draw
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    # Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)

                    win = self.winner()
                    if win is not None:
                        # self.showBoard()
                        # ended with p2 either win or draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    # play with human
    def play2(self):
        while not self.isEnd:
            # Player 1
            positions = self.availablePositions()
            p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
            # take action and upate board state
            self.updateState(p1_action)
            self.showBoard()
            # check board status if it is end
            win = self.winner()
            if win != 0:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                # Player 2
                positions = self.availablePositions()
                p2_action = self.p2.chooseAction(positions)

                self.updateState(p2_action)
                self.showBoard()
                win = self.winner()
                if win != 0:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break

    def showBoard(self):
        # p1: x  p2: o
        for i in range(0, BOARD_SIZE):
            print('-' * (4 * BOARD_SIZE + 1))
            out = '| '
            for j in range(0, BOARD_SIZE):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-' * (4 * BOARD_SIZE + 1))


class Player:
    def __init__(self, name, exp_rate=0.3, lr=.2, use_minimax=True):
        self.name = name
        self.states = []  # record all positions taken
        self.lr = lr
        self.exp_rate = exp_rate
        self.use_minimax = use_minimax
        self.decay_gamma = 0.9
        self.states_value = {}  # state -> value

    def getHash(self, board):
        boardHash = str(board.reshape(BOARD_SIZE * BOARD_SIZE))
        return boardHash

    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            if self.use_minimax:
                minimaxed_result = None
                action = None
                for p in positions:
                    current_board[p] = player
                    result, bias = minimax(st, MAX_DEPTH, -np.Infinity, np.Infinity, False)
                    current_board[p] = 0

                    if result is not None:
                        if minimaxed_result is None:
                            minimaxed_result = result + bias
                            action = p
                        elif result + bias > minimaxed_result:
                            minimaxed_result = result + bias
                            action = p
                print(action)
                if st.should_minimax:
                    print(f"Minimax: {minimaxed_result}")
                    return action

            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                # print("value", value)
                if value >= value_max:
                    value_max = value
                    action = p
            print(f'Reinforcement Learning: {value_max}')
        return action

    # append a hash state
    def addState(self, state):
        self.states.append(state)

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def chooseAction(self, positions):
        while True:
            row = int(input("Input your action row:"))
            col = int(input("Input your action col:"))
            action = (row, col)
            if action in positions:
                return action

    # append a hash state
    def addState(self, state):
        pass

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        pass

    def reset(self):
        pass


def minimax(state: State, depth, alpha, beta, maximizing_player):
    bias = 0
    winner = state.winner()
    if depth == 0 or winner != 0:
        if winner is not None and winner != 0:
            state.should_minimax = True
            bias += winner*BIAS_MULTIPLIER
        return winner, bias

    if maximizing_player:
        max_eval = -np.Infinity
        for position in state.availablePositions():
            state.board[position] = player
            evaluated, delta_bias = minimax(state, depth - 1, alpha, beta, False)
            bias += delta_bias
            state.board[position] = 0
            if evaluated is not None:
                evaluated *= .9
                max_eval = max(max_eval, evaluated)
                alpha = max(alpha, evaluated)
            if beta <= alpha:
                break
        return max_eval if max_eval != -np.Infinity else None, bias

    else:
        min_eval = np.Infinity
        for position in state.availablePositions():
            state.board[position] = opponent
            evaluated, delta_bias = minimax(state, depth - 1, alpha, beta, True)
            bias += delta_bias
            state.board[position] = 0
            if evaluated is not None:
                evaluated *= .9
                min_eval = min(min_eval, evaluated)
                beta = min(beta, evaluated)
            if beta <= alpha:
                break
        return min_eval if min_eval != np.Infinity else None, bias

    # minimax(currentPosition, 3, -∞, +∞, true)


if __name__ == "__main__":
    # choose whether the computer should use minimax or rely solely on reinforcement learning
    p1 = Player("computer", exp_rate=0, use_minimax=True)

    print('Loading Policy')
    p1.loadPolicy("policy_p1")
    p2 = HumanPlayer("human")

    game_board = np.array([  # start with a custom board
        [1, -1, 1, 1, -1],
        [1, 1, -1, -1, 1],
        [1, -1, -1, 1, 0],
        [-1, 1, -1, -1, 0],
        [0, 1, 1, -1, -1]
    ])

    # st = State(p1, p2, board=game_board)  # uncomment this to start with a custom board set above
    st = State(p1, p2)  # comment this out if using custom board
    print('Thinking')
    st.play2()
