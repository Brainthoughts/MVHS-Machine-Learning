import sys
import numpy as np
import pickle
"""
Set BOARD_SIZE and WIN_CONSECUTIVE to desired values and train. The bigger the board, the longer it will take to 
train. 50k-100k rounds of training is enough for 3x3 board and can even play a full game successfully. However, 
we are combining reinforcement learning with a modified minimax to allow larger boards to play well even without 
exorbitant amounts of training. 100k-200k is good enough for the first few moves of a 5x5 board with 4 consecutive
before minimax takes over. Feel free to test out your own values.

To start training, simply run the program for the desired number of rounds and 'ctrl+c' or stop the program through 
the editor. It will load and save progress automatically. Then run tic_tac_toe.py to play against the computer.
"""
BOARD_SIZE = 5
WIN_CONSECUTIVE = 4
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
    def __init__(self, name, exp_rate=0.3, lr=.2):
        self.name = name
        self.states = []  # record all positions taken
        self.lr = lr
        self.exp_rate = exp_rate
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


if __name__ == "__main__":
    # play with human
    p1 = Player("p1", exp_rate=0.3)
    p2 = Player("p2", exp_rate=0.3)
    print('Loading Policy')
    # p1.loadPolicy("policy_p1")
    # p2.loadPolicy("policy_p2")

    st = State(p1, p2)
    st.play(1000)
    # try:
    #     print("training...")
    #     while True:
    #         st.play(10000)  # give number of games or empty for maxint
    #         p1.savePolicy()
    #         p2.savePolicy()
    # except KeyboardInterrupt:
    #     p1.savePolicy()
    #     p2.savePolicy()
    #     print("saved")
    #     sys.exit(0)