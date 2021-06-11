from board import Board
from player import CliPlayer, RandomPlayer


if __name__ == "__main__":
    board = Board(CliPlayer(1), RandomPlayer(2))
    print(board)
    while not board.game_over:
        board.make_move()
        print(board)
    if board.winner:
        print(f"Player {board.winner.player_id} has won", flush=True)
