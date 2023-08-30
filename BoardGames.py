########################################
# CS63: Artificial Intelligence, Final Project
# Spring 2022, Swarthmore College
########################################
# File from CS63 Lab 4
########################################

RED   = u"\033[1;31m"
BLUE  = u"\033[1;34m"
RESET = u"\033[0;0m"
CIRCLE = u"\u25CF"
KING = u"\u25B2"

RED_DISK = RED + CIRCLE + RESET
BLUE_DISK = BLUE + CIRCLE + RESET
RED_KING = RED + KING + RESET
BLUE_KING = BLUE + KING + RESET

class _base_game:

    def __repr__(self):
        if self._repr is None:
            self._repr = "\n".join(" ".join(map(self._print_char, row)) for row in self.board)
            self._repr += "   " + self._print_char(self.turn) + " to move\n"
        return self._repr

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(repr(self))
        return self._hash

    def _print_char(self, i):
        if i == 1:
            return BLUE_DISK
        if i == -1:
            return RED_DISK
        if i == 2:
            return BLUE_KING
        if i == -2:
            return RED_KING
        return u'\u00B7' # empty cell
