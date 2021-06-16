from __future__ import annotations

import curses

import numpy as np
from player import Player, CliPlayer

ROW_COUNT = 5
COL_COUNT = 7
WIN_LENGTH = 4


def get_next_zero_index(arr: np.array):
    return np.argmin(arr)


def evaluate_state_for_player(state: np.array, win_length, curr_player_id: int) -> int:
    score = 0
    strides = np.lib.stride_tricks.sliding_window_view(state, (win_length, win_length))
    for horizontal_stride in strides:
        for sub_matrix in horizontal_stride:
            score += evaluate_score_for_player_in_sub_matrix(sub_matrix, curr_player_id)
    return score


def evaluate_score_for_player_in_sub_matrix(arr: np.array, curr_player_id: int) -> int:
    score = 0
    for row in arr:
        score += score_array(row, curr_player_id)
    for col in arr.T:
        score += score_array(col, curr_player_id)
    score += score_array(np.diag(arr), curr_player_id)
    score += score_array(np.diag(np.fliplr(arr)), curr_player_id)
    return score


def score_array(arr: np.array, player_id):
    opp_player_id = 1 + player_id % 2
    score = 0
    if not (arr == opp_player_id).any():
        if np.count_nonzero(arr) == 4:
            score += 100
        elif np.count_nonzero(arr) == 3:
            score += 5
        elif np.count_nonzero(arr) == 2:
            score += 2
    if not (arr == player_id).any():
        if np.count_nonzero(arr) == 4:
            score -= 99
        if np.count_nonzero(arr) == 3:
            score -= 4
    return score


def check_sub_matrix_for_win(arr: np.array, player_id: int) -> bool:
    for row in arr:
        if (row == player_id).all():
            return True
    for col in arr.T:
        if (col == player_id).all():
            return True
    if (np.diag(arr) == player_id).all():
        return True
    if (np.diag(np.fliplr(arr)) == player_id).all():
        return True
    return False


class Board:
    def __init__(self, first_player: Player, second_player: Player, n_rows: int = ROW_COUNT, n_cols: int = COL_COUNT,
                 win_length: int = WIN_LENGTH):
        self.win_length = win_length
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.state = np.zeros((n_rows, n_cols), dtype=np.int8)
        self.current_player = first_player
        self.next_player = second_player
        self.game_over = False
        self.winner = None

    def __repr__(self):
        return str(np.flip(self.state, axis=0))

    def __eq__(self, other: Board):
        return (self.state == other.state).all() and (self.next_player == other.next_player)

    def is_valid_drop(self, col: int) -> bool:
        return np.isin(col, self.valid_moves(self.state))

    def _is_board_full(self) -> bool:
        return not (self.state == 0).any()

    def valid_moves(self, state):
        return np.where(state[self.n_rows - 1, :] == 0)[0]

    def score_for_player(self, state, player_id):
        return evaluate_state_for_player(state, self.win_length, player_id)

    @staticmethod
    def eval_move(state, col, player_id):
        s_copy = state.copy()
        zero_index = get_next_zero_index(s_copy[:, col])
        s_copy[zero_index, col] = player_id
        return s_copy

    def make_move(self):
        col = self.current_player.next_move(self)
        if self.is_valid_drop(col):
            zero_index = get_next_zero_index(self.state[:, col])
            self.state[zero_index, col] = self.current_player.player_id
            if self.has_player_won(self.state, self.current_player.player_id):
                self.game_over = True
                self.winner = self.current_player
            else:
                self.current_player, self.next_player = self.next_player, self.current_player
        if self._is_board_full():
            self.game_over = True

    def has_player_won(self, state, player_id) -> bool:
        strides = np.lib.stride_tricks.sliding_window_view(state, (self.win_length, self.win_length))
        for horizontal_stride in strides:
            for sub_matrix in horizontal_stride:
                if check_sub_matrix_for_win(sub_matrix, player_id):
                    return True
        return False
