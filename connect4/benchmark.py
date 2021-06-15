import time

from board import Board
from player import MiniMaxPlayer, RandomPlayer


def play(player_1, player_2):
    steps = 0
    board = Board(player_1, player_2)
    while not board.game_over:
        steps = steps + 1
        board.make_move()
    if board.winner == player_1:
        return True, steps
    else:
        return False, steps


def benchmark(player_1, player_2, name='', n_runs=10):
    def time_solve():
        start = time.time()
        player_1_won, steps = play(player_1, player_2)
        t = time.time() - start
        print(player_1_won, t, steps)
        return t, player_1_won

    wins, results = zip(*[time_solve() for _ in range(n_runs)])
    print("Won %d out of %d %s times (avg %.2f secs (%d Hz), max %.2f secs)." % (
        sum(results), n_runs, name, sum(wins) / n_runs, n_runs / sum(wins), max(wins)))


if __name__ == "__main__":
    benchmark(MiniMaxPlayer(1), RandomPlayer(2))
