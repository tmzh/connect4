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


def evaluate_score_for_player_in_sub_matrix(mat: np.array, curr_player_id: int) -> int:
    arrays = get_all_blocks_in_matrix(mat)
    score = sum(map(lambda a: score_block(a.tolist(), curr_player_id), arrays))
    return score


def get_all_blocks_in_matrix(arr):
    rows = [arr[x, :] for x in range(arr.shape[0])]
    cols = [arr[:, x] for x in range(arr.shape[1])]
    d1 = np.diag(arr)
    d2 = np.diag(np.fliplr(arr))
    blocks = [*rows, *cols, d1, d2]
    return blocks


def score_block(block: list, player_id):
    opp_player_id = 1 + player_id % 2
    score = 0
    player_blocks = block.count(player_id)
    opp_blocks = block.count(opp_player_id)
    win_length = len(block)

    if player_blocks == win_length:
        score += 100
    elif player_blocks == win_length - 1 and opp_blocks == 0:
        score += 5
    elif player_blocks == win_length - 2 and opp_blocks == 0:
        score += 2
    elif opp_blocks == win_length:
        score -= 99
    elif opp_blocks == win_length - 1 and player_blocks == 0:
        score -= 4
    return score


def check_sub_matrix_for_win(mat: np.array, player_id: int) -> bool:
    blocks = get_all_blocks_in_matrix(mat)
    for arr in blocks:
        if arr.tolist().count(player_id) == len(arr):
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
        self.n_moves = 0
        self._game_over = False
        self.winner = None

    def __repr__(self):
        return str(np.flip(self.state, axis=0))

    def __eq__(self, other: Board):
        return (self.state == other.state).all() and (self.next_player == other.next_player)

    @property
    def game_over(self):
        if self._is_board_full():
            self._game_over = True
        return self._game_over 

    @game_over.setter
    def game_over(self, value):
        self._game_over = value


    def is_valid_drop(self, col: int) -> bool:
        return np.isin(col, self.valid_moves(self.state))

    def _is_board_full(self) -> bool:
        return not (self.state == 0).any()

    def valid_moves(self, state):
        return np.where(state[self.n_rows - 1, :] == 0)[0]

    def score_for_player(self, state, player_id):
        return evaluate_state_for_player(state, self.win_length, player_id)

    def eval_move(self, state, col, player_id):
        s_copy = state.copy()
        zero_index = get_next_zero_index(s_copy[:, col])
        s_copy[zero_index, col] = player_id
        return s_copy

    def make_move(self):
        col = self.current_player.next_move(self)
        if self.is_valid_drop(col):
            zero_index = get_next_zero_index(self.state[:, col])
            self.state[zero_index, col] = self.current_player.player_id
            self.n_moves += 1
            if self.has_player_won(self.state, self.current_player.player_id):
                self.game_over = True
                self.winner = self.current_player
            else:
                self.current_player, self.next_player = self.next_player, self.current_player

    def has_player_won(self, state, player_id) -> bool:
        strides = np.lib.stride_tricks.sliding_window_view(state, (self.win_length, self.win_length))
        for horizontal_stride in strides:
            for sub_matrix in horizontal_stride:
                if check_sub_matrix_for_win(sub_matrix, player_id):
                    return True
        return False
