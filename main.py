#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A simple Tic-Tac-Toe game."""
from abc import ABC, abstractmethod
from typing import List
import os

BOARD_SIZE_X = 3
BOARD_SIZE_Y = 3
EMPTY_TOKEN = ' '
PLAYER_TOKENS = ('X', 'O')
H_SEPERATOR = '|'
V_SEPERATOR = '-'


class Board:
    """Checker style board."""

    def __init__(self, size_x, size_y, empty_token):
        self.size_x = size_x
        self.size_y = size_y
        self.size = int(size_x * size_y)
        self.empty_token = empty_token
        self.grid = [[self.empty_token] * size_x for _ in range(size_y)]

    def get_row(self, pos: int) -> int:
        return len(self.grid) - (pos - 1)//self.size_y - 1

    def get_column(self, pos: int) -> int:
        return pos % self.size_x - 1

    def is_empty(self, pos: int) -> bool:
        return (self.grid[self.get_row(pos)][self.get_column(pos)] ==
                self.empty_token)

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


class WinningCondition(ABC):

    @abstractmethod
    def has_won(self, board: Board) -> bool:
        pass


def completed(tokens, empty_token):
    return len(tokens) == 1 and empty_token not in tokens


class RowCompleted(WinningCondition):

    def has_won(self, board: Board) -> bool:
        for row in board.grid:
            if completed(set(row), board.empty_token):
                return True
        return False


class ColumnCompleted(WinningCondition):

    def _column_content(self, board: Board, column: int) -> set:
        content = []
        for row in range(board.size_y):
            content.append(board.grid[row][column])
        return set(content)

    def has_won(self, board: Board) -> bool:
        for column in range(board.size_x):
            column_content = self._column_content(board, column)
            if completed(set(column_content), board.empty_token):
                return True
        return False


class GridDimensionError(Exception):
    pass


class DiagonalComplete(WinningCondition):

    def _get_left_to_right(self, grid: List[List[int]]) -> set:
        values = []
        for i in range(len(grid)):
            values.append(grid[i][i])
        return set(values)

    def _right_to_left(self, grid: List[List[int]]) -> set:
        values = []
        for i in range(len(grid)):
            pos = len(grid) - i - 1
            values.append(grid[i][pos])
        return set(values)

    def has_won(self, board: Board) -> bool:
        if not board.size_x == board.size_y:
            raise GridDimensionError("only use with n x n grid")
        left_to_right = self._get_left_to_right(board.grid)
        right_to_left = self._right_to_left(board.grid)
        return (completed(left_to_right, board.empty_token) or
                completed(right_to_left, board.empty_token))


class TicTacToe:
    """Handles the game logic."""

    def __init__(self, board: Board, ci: ConsoleInterface,
                 rules: List[WinningCondition], tokens: List[str]):
        self.board = board
        self.ci = ci
        self.rules = rules
        self.tokens = tokens

    def make_turn(self, count):
        while True:
            pos = self.ci.read_token(self.board.size)
            if self.board.is_empty(pos):
                self.board.place_token(
                    pos, self.tokens[count % len(self.tokens)])
                self.ci.print_board(self.board)
                break
            self.ci.print_is_blocked()

    def has_won(self):
        for rule in self.rules:
            if rule.has_won(self.board):
                return True
        return False

    def run(self):
        self.ci.print_board(self.board)
        for i in range(self.board.size):
            self.make_turn(count=i)
            if self.has_won():
                self.ci.print_has_won()
                break


def main():
    board = Board(BOARD_SIZE_X, BOARD_SIZE_Y, EMPTY_TOKEN)
    ci = ConsoleInterface(H_SEPERATOR, V_SEPERATOR)
    rules = [RowCompleted(), ColumnCompleted(), DiagonalComplete()]
    game = TicTacToe(board, ci, rules, PLAYER_TOKENS)
    game.run()


if __name__ == '__main__':
    main()
