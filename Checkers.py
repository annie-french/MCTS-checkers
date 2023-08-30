########################################
# CS63: Artificial Intelligence, Final Project
# Spring 2022, Swarthmore College
# Annie French and Gyan Bains
########################################
# A class for a checkers board and game
########################################

import numpy as np

from BoardGames import _base_game

RED   = u"\033[1;31m"
BLUE  = u"\033[1;34m"
RESET = u"\033[0;0m"
CIRCLE = u"\u25CF"

RED_DISK = RED + CIRCLE + RESET
BLUE_DISK = BLUE + CIRCLE + RESET

class Checkers(_base_game):
    """Implements the game Checkers.

    Attributes:
    board: An array in which +1 represents a blue piece, -1 represents a red
           piece, and 0 represents an empty space.
    turn:  Indicates which player will move next. +1 for the blue (downward-
           moving) player. -1 for the red (upward-moving) player."""
    def __init__(self, size=6, game=None):
        #board only set up for 6x6 board, will generalize later
        if game is None: # create new game
            assert size > 1
            self.board = np.zeros([size, size], dtype=int)
            for i in range(0,size):
                if i %2 == 0:
                    self.board[0][i] = 1
                    self.board[-2][i] = -1
                    #self.board[2][i] = 1 #adds third row of pieces

                if i %2 == 1:
                    self.board[1][i] = 1
                    self.board[-1][i] = -1
                    #self.board[-3][i]= -1 # adds third row of pieces
            self.turn = 1
        else: # copy existing game
            self.board = game.board.copy()
            self.turn = game.turn

        self._moves = None
        self._terminal = None
        self._winner = None
        self._repr = None
        self._hash = None
        self.p1_pieces = size # +1 player
        self.p2_pieces = size # -1 player

    def makeMove(self, move):
        """Returns a new Checkers instance in which move has been played.

        A valid move is a triple (row, col, dir), where row and col indicate
        the position of the piece that is moving, and dir can be -1,+1,-2, or +2,
        indicating which of the possible columns the piece moves
        to. If the direction is -2 or +2, the piece jumps over an opponent's piece
        and captures it. For example if it is the +1 player's turn, (2,1,-1) would mean that
        the piece in row 2, column 1 moves to row 3 column 0. On player -1's
        turn, the same move would mean moving to row 1, column 0 (because
        player +1's pieces move down, while player -1's pieces move up)."""
        row, col, vdelta, hdelta = move #hdelta is movement horizontally and vdelta is movement vertically
        new_game = Checkers(game=self)
        value = self.board[row,col]
        new_game.board[row + vdelta, col + hdelta] = value
        new_game.board[row, col] = 0
        if hdelta == 2 or hdelta == -2: #capture opponent's piece
            new_game.board[row + int(vdelta/2), col + int(hdelta/2)] = 0
            if self.turn == 1:
                self.p2_pieces -= 1
            else:
                self.p1_pieces -= 1
        if (self.turn == 1 and row + vdelta == self.board.shape[0]-1) or (self.turn == -1 and row + vdelta == 0):
            new_game.board[row + vdelta, col + hdelta] = self.turn*2
        new_game.turn *= -1
        return new_game

#The @property decorator makes it so that you can access self.availableMoves
#as a field instead of calling self.availableMoves() as a function.
    @property
    def availableMoves(self):
        """List of legal moves for the current player."""
        if self._moves is None:
            self._moves = []

        #    #non-king pieces
        #     for row,col in zip(*np.where(self.board == self.turn)):
        #         r = row + self.turn
        #         if (r < 0) or (r >= self.board.shape[0]):
        #             continue
        #         if (self.turn == 1 and row < self.board.shape[0]-1) or (self.turn == -1 and row > 0):
        #             if col > 0 and self.board[r, col-1] == 0:
        #                 self._moves.append((row, col, self.turn,-1)) #move left
        #             if col < self.board.shape[0]-1 and self.board[r, col+1] == 0:
        #                 self._moves.append((row,col,self.turn,1)) #move right
        #         if (self.turn == 1 and row < self.board.shape[0]-2) or (self.turn == -1 and row > 1):
        #             if col > 1 and self.board[r+self.turn,col-2] == 0 and self.board[r+self.turn,col-1]==-1:
        #                 self._moves.append((row,col,2*self.turn,-2)) #jump left
        #             if col < self.board.shape[0]-2 and self.board[r+self.turn,col+2] == 0 and self.board[r+self.turn,col+1]==-1:
        #                     self._moves.append((row,col,2*self.turn,2)) #jump right
        #
        #
        #     #king pieces
        #     for row,col in zip(*np.where(self.board == self.turn*2)):
        #         if (r < 0) or (r >= self.board.shape[0]):
        #             continue
        #         if row > 0:
        #             if col > 0 and self.board[row -1, col-1] == 0:
        #                 self._moves.append((row, col, -1,-1)) #move up left
        #             if col < self.board.shape[0]-1 and self.board[row-1, col+1] == 0:
        #                 self._moves.append((row,col,-1,1)) #move up right
        #         if row < self.board.shape[0]-1:
        #             if col > 0 and self.board[row + 1, col-1] == 0:
        #                 self._moves.append((row, col, 1,-1)) #move down left
        #             if col < self.board.shape[0]-1 and self.board[row+1, col+1] == 0:
        #                 self._moves.append((row,col,1,1)) #move down right
        #         if row > 1:
        #             if col > 1 and self.board[row-2,col-2] == 0 and self.board[row-1,col-1]==-self.turn:
        #                 self._moves.append((row,col,-2,-2)) #jump up left
        #             if col < self.board.shape[0]-2 and self.board[row-2,col+2] == 0 and self.board[row-1,col+1]==-self.turn:
        #                 self._moves.append((row,col,-2,2)) #jump up right
        #         if row < self.board.shape[0]-2:
        #             if col > 1 and self.board[row+2,col-2] == 0 and self.board[row+1,col-1]==-self.turn:
        #                 self._moves.append((row,col,2,-2)) #jump down left
        #             if col < self.board.shape[0]-2 and self.board[row+2,col+2] == 0 and self.board[row+1,col+1]==-self.turn:
        #                 self._moves.append((row,col,2,2)) #jump down right
        #
        #
        # return self._moves

           #non-king pieces
            for row,col in zip(*np.where(self.board == self.turn)):
                r = row + self.turn
                if (r < 0) or (r >= self.board.shape[0]):
                    continue
                if self.turn == 1:
                    if row < self.board.shape[0]-1:
                        if col > 0 and self.board[r, col-1] == 0:
                            self._moves.append((row, col, 1,-1)) #move left
                        if col < self.board.shape[0]-1 and self.board[r, col+1] == 0:
                            self._moves.append((row,col,1,1)) #move right
                    if row < self.board.shape[0]-2:
                        if col > 1 and self.board[row+2,col-2] == 0 and self.board[row+1,col-1]<=-1:
                            self._moves.append((row,col,2,-2)) #jump left
                        if col < self.board.shape[0]-2 and self.board[row+2,col+2] == 0 and self.board[row+1,col+1]<=-1:
                            self._moves.append((row,col,2,2)) #jump right
                elif self.turn == -1:
                    if row > 0:
                        if col > 0 and self.board[r, col-1] == 0:
                            self._moves.append((row, col, -1,-1)) #move left
                        if col < self.board.shape[0]-1 and self.board[r, col+1] == 0:
                            self._moves.append((row,col,-1,1)) #move right
                    if row > 1:
                        if col > 1 and self.board[row-2,col-2] == 0 and self.board[row-1,col-1]>=1:
                            self._moves.append((row,col,-2,-2)) #jump left
                        if col < self.board.shape[0]-2 and self.board[row-2,col+2] == 0 and self.board[row-1,col+1]>=1:
                            self._moves.append((row,col,-2,2)) #jump right

            #king pieces
            for row,col in zip(*np.where(self.board == self.turn*2)):
                if row < self.board.shape[0]-1:
                    if col > 0 and self.board[row+1,col-1] == 0:
                        self._moves.append((row,col,1,-1)) #move increasing left
                    if col < self.board.shape[0]-1 and self.board[row + 1,col+1]==0:
                        self._moves.append((row,col,1,1)) #move increasing right
                if row < self.board.shape[0]-2:
                    if col > 1 and self.board[row+2,col-2] == 0 and (self.board[row+1,col-1]==-self.turn or self.board[row+1,col-1]==(-self.turn*2)) :
                        self._moves.append((row,col,2,-2)) #jump increasing left
                    if col < self.board.shape[0]-2 and self.board[row+2,col+2]==0 and (self.board[row+1,col+1]==-self.turn or self.board[row+1,col+1]==(-self.turn*2)) :
                        self._moves.append((row,col,2,2)) #jump increasing right
                        return self._moves
                if row > 0:
                    if col > 0 and self.board[row-1,col-1] == 0:
                        self._moves.append((row,col,-1,-1)) #move decreasing left
                    if col < self.board.shape[0]-1 and self.board[row-1,col+1] == 0:
                        self._moves.append((row,col,-1,1)) #move decreasing right
                if row > 1:
                    if col > 1 and self.board[row-2,col-2] == 0 and (self.board[row-1,col-1]==-self.turn or self.board[row-1,col-1]==(-self.turn*2)) :
                        self._moves.append((row,col,-2,-2)) #jump decreasing left
                    if col < self.board.shape[0]-2 and self.board[row-2,col+2] == 0 and (self.board[row-1,col+1]==-self.turn or self.board[row-1,col+1]==(-self.turn*2)) :
                        self._moves.append((row,col,-2,2)) #jump decreasing right
        return self._moves

    @property
    def isTerminal(self):
        """Boolean indicating whether the game has ended."""
        if self._terminal is None:
            if self.p1_pieces == 0 or self.p2_pieces == 0:
                self._terminal = True
            elif self.availableMoves == []:
                self._terminal = True
            else:
                self._terminal = False
        return self._terminal

    @property
    def winner(self):
        """
        TODO
        """
        """+1 if the first player (maximizer) has won. -1 if the second player
        (minimizer) has won. 0 if the game is a draw. Raises an AttributeError
        if accessed on a non-terminal state."""
        if not self.isTerminal:
            raise AttributeError("Non-terminal states have no winner.")
        if self._winner is None:
            if self.turn == 1 and self.availableMoves == []:
                self._winner = -1
            else:
                self._winner = 1
        return self._winner
