'''
Daniel Wen

This project is an implementation of the game Othello.
There are four player/opponent types: random choice, human choice,
moves chosen by a minimax algorithm, and moves chosen by an alpha-beta
algorithm.

The minimax and alpha-beta algirthms are opitmized such that they will always
win against a random choice opponent. To play, simply copy and past the following
board setup:

...........................OX......XO...........................

'''

import random

def main():
    inp = input("Input a starting state: ")
    print("Player Type Options: \"random\", \"human\", \"minimax\", \"alpha-beta\"")
    type1 = input("Input Player 1 type: ")
    type2 = input("Input Player 2 type: ")

    for i in range(0, 50):
        initial = Board(inp, type1, type2)
        initial.printBoard()
        initial.playGame(initial.player1, initial.player2)


class Player:
    symbol = ""
    positions = set()
    board = dict()
    type = ""
    directions = [-11, -10, -9, -1, 1, 9, 10, 11]
    possibleMoves = set()
    start = ""

    def __init__(self, b, state, s, t):
        self.symbol = s
        self.positions = set()
        self.start = state
        self.parent = b
        for i in range(0, len(state)):
            if state[i] == self.symbol:
                self.positions.add(i)
        self.board = state
        self.type = t

    def copy(self):
        return Player(self.parent, self.start, self.symbol, self.type)

    def findLegalMoves(self):
        self.possibleMoves = set()
        for pos in self.positions:
            for i in self.directions:
                temp = pos + i
                if self.board[temp] == "W" or self.board[temp] == self.symbol or self.board[temp] == ".":
                    continue
                while self.board[temp] != "W" and self.board[temp] != self.symbol and self.board[temp] != ".":
                    temp = temp + i
                if self.board[temp] == ".":
                    self.possibleMoves.add(temp)
        return self.possibleMoves

    def chooseMove(self):
        self.findLegalMoves()
        if len(self.possibleMoves) == 0:
            return -1
        elif self.type == "random":
            return random.choice(list(self.possibleMoves))
        elif self.type == "human":
            print("Possible moves: " + str(self.possibleMoves))
            move = input("Where will Player " + self.symbol + " move? ")
            return int(move)
        elif self.type == "minimax":
            return self.parent.minimax(self.symbol, None, self.parent, 0, 0)[1]
        else:
            return self.parent.alpha_beta_search(self.symbol, self.parent)

    def update(self, b,  state):
        self.parent = b
        self.positions = set()
        board = state
        for i in range(0, len(state)):
            if board[i] == self.symbol:
                self.positions.add(i)


class Board:
    turn = 0
    player1 = None
    player2 = None
    board = dict()

    def __init__(self, str, t1, t2):
        self.state = str
        if len(str) == 64:
            self.board = self.makeBoard(str)
        else:
            self.board = dict()
            for i in range(0, 100):
                self.board[i] = self.state[i]
        self.player1 = Player(self, self.board, "X", t1)
        self.player2 = Player(self, self.board, "O", t2)

    def makeBoard(self, string):
        ret = {}
        for i in range(0, 100):
            ret[i] = "."
        for i in range(0, 10):
            ret[i] = "W"
        for i in range(10, 90, 10):
            ret[i] = "W"
            ret[i + 9] = "W"
            for j in range(i + 1, i + 9):
                ret[j] = string[(int(i / 10) - 1) * 8 + j - i - 1]
        for i in range(90, 100):
            ret[i] = "W"
        return ret

    def printBoard(self):
        string = self.board
        for i in range(11, 90):
            if i % 10 == 0:
                print()
            if string[i] != "W":
                print(string[i], end=' ')
        print()

    def isComplete(self):
        set1 = self.player1.findLegalMoves()
        set2 = self.player2.findLegalMoves()
        if len(set1) == 0 and len(set2) == 0:
            return True
        if len(self.player1.positions) == 0 or len(self.player2.positions) == 0:
            return True
        return False

    def difference(self, char):
        if char == "X":
            char1 = "O"
        else:
            char1 = "X"
        count1 = 0
        count2 = 0
        for i in range(0, 100):
            if self.board[i] == char:
                count1 += 1
            elif self.board[i] == char1:
                count2 += 1
        return count1 - count2

    def updateBoard(self, move, symbol):
        directions = [-11, -10, -9, -1, 1, 9, 10, 11]
        self.board[move] = symbol
        for i in directions:
            temp = move + i
            current = set()
            while self.board[temp] != symbol and self.board[temp] != "W" and self.board[temp] != ".":
                current.add(temp)
                temp = temp + i
            if self.board[temp] == symbol:
                for c in current:
                    self.board[c] = symbol
        self.player1.update(self, self.board)
        self.player2.update(self, self.board)
        self.state = ""
        for i in range(0, len(self.board)):
            self.state += self.board[i]

    def playGame(self, player1, player2):
        turn = 0
        while not self.isComplete():
            if turn == 0:
                print("Player X's move: ")
                move1 = player1.chooseMove()
                if move1 == -1:
                    print("No possible moves, skip turn.")
                    turn = (turn + 1) % 2
                    continue
                self.updateBoard(move1, "X")
                turn = (turn + 1) % 2
            else:
                print("Player O's move: ")
                move2 = player2.chooseMove()
                if move2 == -1:
                    print("No possible moves, skip turn.")
                    turn = (turn + 1) % 2
                    continue
                self.updateBoard(move2, "O")
                turn = (turn + 1) % 2
            self.printBoard()
            countx = 0
            counto = 0
            for i in range(0, len(self.board)):
                if self.board[i] == "X":
                    countx += 1
                elif self.board[i] == "O":
                    counto += 1
        print("Score: " + str(countx) + " X pieces " + str(counto) + " O pieces")
        if countx == counto:
            print("It's a tie!")
        elif countx > counto:
            print("Player X wins!")
        else:
            print("Player O wins!")

    def generateChildren(self, char):
        if char == "X":
            return self.player1.findLegalMoves()
        else:
            return self.player2.findLegalMoves()

    def copy(self):
        return Board(self.state, self.player1.copy(), self.player2.copy())

    def newState(self, i, char):
        tboard = self.copy()
        tboard.updateBoard(i, char)
        return tboard

    def minimax(self, char, m, state, turn, end):
        if char == "X":
            char2 = "O"
        else:
            char2 = "X"
        if end - turn == 3:
            if state.startGame():
                return (state.startGameEval(char), m)
            return (state.difference(char), m)
        if end % 2 == 0 and char == "X" and len(state.player1.findLegalMoves()) == 0:
            return state.minimax(char, m, state, turn, end + 1)
        if end % 2 == 0 and char == "O" and len(state.player2.findLegalMoves()) == 0:
            return state.minimax(char, m, state, turn, end + 1)
        if end % 2 == 1 and char2 == "X" and len(state.player1.findLegalMoves()) == 0:
            return state.minimax(char, m, state, turn, end + 1)
        if end % 2 == 1 and char2 == "O" and len(state.player2.findLegalMoves()) == 0:
            return state.minimax(char, m, state, turn, end + 1)
        else:
            if end % 2 == 0:
                list = state.generateChildren(char)
                max = -9999
                maxindex = 0
                for i in list:
                    w = state.minimax(char, i, state.newState(i, char), turn, end + 1)[0]
                    if w > max:
                        max = w
                        maxindex = i
                #if maxindex == 0:
                    #return (-9999, m)
                return (max, maxindex)
            else:
                list = state.generateChildren(char2)
                min = 9999
                minindex = 0
                for i in list:
                    w = state.minimax(char, i, state.newState(i, char2), turn, end + 1)[0]
                    if w < min:
                        min = w
                        minindex = i
                #if minindex == 0:
                    #return (9999, m)
                return (min, minindex)

    def alphabeta(self, char, m, state, alpha, beta, turn, end):
        if char == "X":
            char2 = "O"
        else:
            char2 = "X"
        if end - turn == 4:
            if state.startGame():
                return (state.startGameEval(char), m)
            return (state.difference(char), m)
        if end % 2 == 0 and char == "X" and len(state.player1.findLegalMoves()) == 0:
            return state.alphabeta(char, m, state, alpha, beta, turn, end + 1)
        if end % 2 == 0 and char == "O" and len(state.player2.findLegalMoves()) == 0:
            return state.alphabeta(char, m, state, alpha, beta, turn, end + 1)
        if end % 2 == 1 and char2 == "X" and len(state.player1.findLegalMoves()) == 0:
            return state.alphabeta(char, m, state, alpha, beta, turn, end + 1)
        if end % 2 == 1 and char2 == "O" and len(state.player2.findLegalMoves()) == 0:
            return state.alphabeta(char, m, state, alpha, beta, turn, end + 1)
        else:
            if end % 2 == 0:
                list = state.generateChildren(char)
                maxindex = 0
                v = float("-inf")
                for i in list:
                    temp = state.alphabeta(char, i, state.newState(i, char), alpha, beta, turn, end + 1)
                    if temp[0] > v:
                        v = temp[0]
                        maxindex = i
                    if v > beta:
                        return (v, maxindex)
                return(v, maxindex)
            else:
                list = state.generateChildren(char2)
                minindex = 0
                v = float('inf')
                for i in list:
                    temp = state.alphabeta(char, i, state.newState(i, char2), alpha, beta, turn, end + 1)
                    if temp[0] < v:
                        v = temp[0]
                        minindex = i
                    if v < alpha:
                        return (v, minindex)
                return (v, minindex)

    def alpha_beta_search(self, char, state):
        v = state.alphabeta(char, None, state, float("-inf"), float("inf"), 0, 0)
        return v[1]

    def startGameEval(self, char):
        sides = [13, 14, 15, 16, 31, 41, 51, 61, 38, 48, 58, 68]
        count1 = 0
        count2 = 0
        if char == "X":
            char2 = "O"
        else:
            char2 = "X"
        for i in range(0, len(self.board)):
            if self.board[i] == char:
                count1 += 1
                if i == 11 or i == 18 or i == 81 or i == 88:
                    count1 += 100
                if i in sides:
                    count1 += 10
            elif self.board[i] == char2:
                count2 += 1
                if i == 11 or i == 18 or i == 81 or i == 88:
                    count2 += 100
                if i in sides:
                    count2 += 10
        if char == "X":
            count1 += 10 * len(self.player1.findLegalMoves())
            count2 += 10 * len(self.player2.findLegalMoves())
        else:
            count2 += 10 * len(self.player1.findLegalMoves())
            count1 += 10 * len(self.player2.findLegalMoves())
        return count1 - count2

    def startGame(self):
        count = 0
        for i in range(0, len(self.board)):
            if self.board[i] == "X" or self.board[i] == "O":
                count += 1
        return count < 58


if __name__ == '__main__':
    main()


