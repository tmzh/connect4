import time

from board import Board
from player import MiniMaxPlayer, RandomPlayer
from sklearn.utils import shuffle
import pandas as pd
from scipy import stats

class Benchmark:
    def __init__(self, player, name='', n_runs=100):
        self.player = player
        self.opponent = RandomPlayer(2)
        self.n_runs = n_runs

    def save(self, result):
        result.to_pickle(f'{self.name}.pkl')

    def load(self):
        return pd.DataFrame.frm_pickle(f'{self.name}.pkl')

    def play(self):
        player_1, player_2 = shuffle([self.player, self.opponent])
        board = Board(player_1, player_2)
        while not board.game_over:
            board.make_move()
        if board.winner == self.player:
            return "won", board.n_moves
        if board.winner == self.opponent:
            return "lost", board.n_moves
        else:
            return "draw", board.n_moves

    def run(self):
        def time_solve():
            start = time.time()
            result, steps = self.play()
            t = time.time() - start
            return t, result, steps
        durations, results, steps = zip(*[time_solve() for _ in range(self.n_runs)])
        return pd.DataFrame({'durations': durations, 'results': results, 'steps': steps})
    
    def plot(self, output):
        results = output['results']
        durations = output['durations']
        steps = output['steps']
        wins = results.count("won")
        losses = results.count("lost")
        print("Won %d out of %d times. Lost %d times (avg %.2f secs (%d Hz), max %.2f secs)." % (
            wins, self.n_runs, losses, wins / self.n_runs, self.n_runs / sum(durations), max(durations)))
        steps_desc = stats.describe(steps)
        print("No. of steps", steps_desc)
        plt.hist(steps, bins=range(40), density=True)
        plt.xlabel('Number of Turns to win')
        plt.ylabel('Fraction of games')
        plt.title(f'Simulated lengths of connect4 games for {name}')


if __name__ == "__main__":
    b = Benchmark(MiniMaxPlayer(1))
