import copy
import math
import random
from abc import ABC
from typing import Tuple, Any


class Player(ABC):
    def __init__(self, player_id):
        self.player_id = player_id
        self.opponent_id = 1 + player_id % 2

    def next_move(self, board):
        pass


class GuiPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self._next_move = None

    def set_next_move(self, value):
        self._next_move = value

    def next_move(self, board):
        if board.is_valid_drop(self._next_move):
            return self._next_move


class CliPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)

    def next_move(self, board):
        next_col = int(input(f"Enter the next move for player {self.player_id}: "))
        return next_col


class RandomPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)

    def next_move(self, board):
        return random.choice(board.valid_moves(board.state))


class MiniMaxPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)

    def minimax(self, board, state, depth, maximising_player) -> Tuple[Any, int]:
        if board.game_over:
            if board.has_player_won(state, self.player_id):
                return None, 10**10
            if board.has_player_won(state, self.opponent_id):
                return None, -10**10
            else:
                return None, 0
        if depth == 0:
            score = board.score_for_player(state, self.player_id)
            return None, score

        column = random.choice(board.valid_moves(state))
        if maximising_player:
            value = -math.inf
            for col in board.valid_moves(state):
                new_state = board.eval_move(state, col, self.player_id)
                new_score = self.minimax(board, new_state, depth - 1, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
            return column, value

        if not maximising_player:
            value = math.inf
            for col in board.valid_moves(state):
                new_state = board.eval_move(state, col, self.opponent_id)
                new_score = self.minimax(board, new_state, depth - 1, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
            return column, value

    def next_move(self, board):
        col, minimax_score = self.minimax(board, board.state, 3, True)
        return col
