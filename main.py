#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A simple Tic-Tac-Toe game."""
BOARD_SIZE_X = 3
BOARD_SIZE_Y = 3
EMPTY = ' '
TOKENS = ('X', 'O')
H_SEPERATOR = '|'
V_SEPERATOR = '-'


class Board:
    """Checker style board."""

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.size = int(size_x * size_y)
        self.grid = [[EMPTY] * size_x for _ in range(size_y)]

    def get_row(self, pos: int) -> int:
        return len(self.grid) - (pos - 1)//self.size_y - 1

    def get_column(self, pos: int) -> int:
        return pos % self.size_x - 1

    def is_empty(self, pos: int) -> bool:
        return self.grid[self.get_row(pos)][self.get_column(pos)] == EMPTY

    def place_token(self, pos: int, token: str):
        self.grid[self.get_row(pos)][self.get_column(pos)] = token


class ConsoleInterface:
    """Console user interface."""

    def __init__(self, h_sep, v_sep):
        self.h_sep = h_sep
        self.v_sep = v_sep

    def print_board(self, board: Board):
        rows = [f' {self.h_sep} '.join(row) for row in board.grid]
        h_line = ''.join([self.v_sep * len(rows[0])])
        board_str = f'\n{h_line}\n'.join(rows)
        print(board_str)

    @staticmethod
    def read_token(max_val, min_val=1) -> int:
        while True:
            user_input = input('Place your token: ')
            try:
                token_pos = int(user_input)
                if not min_val <= token_pos <= max_val:
                    print(f'Token has to be placed in range {min_val} to ' +
                          f'{max_val}. Try again.')
                else:
                    return token_pos
            except ValueError:
                print('This is not a Number. Try again.')

    @staticmethod
    def print_is_blocked():
        print('Already blocked. Try again.')

    @staticmethod
    def print_has_won():
        print('You win.')


def main():
    board = Board(BOARD_SIZE_X, BOARD_SIZE_Y)
    ci = ConsoleInterface(H_SEPERATOR, V_SEPERATOR)


if __name__ == '__main__':
    main()
