import random
import time
from abc import ABC


class Player(ABC):
    def __init__(self, player_id):
        self.player_id = player_id

    def next_move(self, board):
        pass


class GuiPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self._next_move = None

    def set_next_move(self, value):
        self._next_move = value

    def next_move(self, state):
        return self._next_move


class CliPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)

    def next_move(self, state):
        next_col = int(input(f"Enter the next move for player {self.player_id}: "))
        return next_col


class RandomPlayer(Player):
    def __init__(self, player_id, delay=False):
        super().__init__(player_id)
        self.delay = delay

    def next_move(self, state):
        no_cols = state.shape[-1]
        if self.delay:
            time.sleep(1)
        return random.randint(0, no_cols - 1)
