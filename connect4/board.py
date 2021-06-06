from __future__ import annotations

import numpy as np

ROW_COUNT = 5
COL_COUNT = 7
WIN_LENGTH = 4


def get_next_zero_index(arr: np.array):
    return np.argmin(arr)


def check_sub_matrix_for_win(arr: np.array, player_value: int) -> bool:
    for row in arr:
        if (row == player_value).all():
            return True
    for col in arr.T:
        if (col == player_value).all():
            return True
    if (np.diag(arr) == player_value).all():
        return True
    if (np.diag(np.fliplr(arr)) == player_value).all():
        return True
    return False


class Board:
    def __init__(self, n_rows: int = ROW_COUNT, n_cols: int = COL_COUNT, win_length: int = WIN_LENGTH):
        self.win_length = win_length
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.state = np.zeros((n_rows, n_cols), dtype=np.int8)
        self.current_player = 1
        self.next_player = 2
        self.game_over = False

    def __repr__(self):
        return str(np.flip(self.state, axis=0))

    def __eq__(self, other: Board):
        return (self.state == other.state).all() and (self.next_player == other.next_player)

    def _is_valid_drop(self, col: int) -> bool:
        return self.state[self.n_rows - 1, col] == 0

    def make_move(self, col: int):
        zero_index = get_next_zero_index(self.state[:, col])
        self.state[zero_index, col] = self.current_player
        if self.has_current_player_won():
            self.game_over = True
        else:
            self.current_player, self.next_player = self.next_player, self.current_player

    def has_current_player_won(self) -> bool:
        strides = np.lib.stride_tricks.sliding_window_view(self.state, (self.win_length, self.win_length))
        for horizontal_stride in strides:
            for sub_matrix in horizontal_stride:
                if check_sub_matrix_for_win(sub_matrix, self.current_player):
                    return True
        return False


if __name__ == "__main__":
    board = Board()
    while not board.game_over:
        next_col = int(input(f"Enter the next move for {board.current_player}: "))
        board.make_move(next_col)
        print(board)
