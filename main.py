#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A simple Tic-Tac-Toe game."""
BOARD_SIZE_X = 3
BOARD_SIZE_Y = 3
EMPTY = ' '
TOKENS = ('X', 'O')

class Board:
    """Checker style board."""

    def __init__(self, size_x, size_y):
        self.size = int(size_x * size_y)
        self.grid = [[EMPTY] * size_x for _ in range(size_y)]

    def get_row(self, pos: int) -> int:
        return len(self.grid) - (pos - 1)//BOARD_SIZE_Y - 1

    @staticmethod
    def get_column(pos: int) -> int:
        return pos % BOARD_SIZE_X - 1

    def is_empty(self, pos: int) -> bool:
        return self.grid[self.get_row(pos)][self.get_column(pos)] == EMPTY

    def place_token(self, pos: int, token: str):
        self.grid[self.get_row(pos)][self.get_column(pos)] = token


def main():
  board = Board(BOARD_SIZE_X, BOARD_SIZE_Y)


if __name__ == '__main__':
    main()
