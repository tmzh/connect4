from board import Board, get_next_zero_index, check_sub_matrix_for_win, evaluate_state_for_player
import numpy as np
import pytest

from player import CliPlayer, GuiPlayer


def test_create_board_using_defaults():
    test_board = Board(CliPlayer(1), CliPlayer(2))
    assert (test_board.state == np.zeros((5, 7), dtype=np.int8)).all()
    assert test_board.current_player.player_id == 1
    assert test_board.next_player.player_id == 2


def test_create_custom_board():
    test_board = Board(CliPlayer(1), CliPlayer(2), n_rows=9, n_cols=9)
    assert (test_board.state == np.zeros((9, 9), dtype=np.int8)).all()


def test_is_drop_valid():
    test_board = Board(CliPlayer(1), CliPlayer(2), n_rows=2, n_cols=2)

    assert test_board.is_valid_drop(0)

    test_board.state[0] = 1
    assert test_board.is_valid_drop(0)

    test_board.state[:, 0] = 1
    assert test_board.is_valid_drop(1)
    assert not test_board.is_valid_drop(0)

    test_board.state = np.ones((2, 2))
    assert not test_board.is_valid_drop(0)


def test_make_move(monkeypatch):
    test_board = Board(CliPlayer(1), CliPlayer(2), n_rows=3, n_cols=3, win_length=3)
    monkeypatch.setattr('player.CliPlayer.next_move', lambda x, y: 2)

    test_board.state[:, 1] = np.array([1, 0, 0], dtype=np.int8)
    test_board.state[:, 2] = np.array([2, 1, 0], dtype=np.int8)

    test_board.make_move()

    assert (test_board.state == np.array([[0, 1, 2],
                                          [0, 0, 1],
                                          [0, 0, 1]], dtype=np.int8)).all()


def test_make_move_ignores_invalid_moves(monkeypatch):
    test_board = Board(CliPlayer(1), CliPlayer(2), n_rows=3, n_cols=3, win_length=3)
    monkeypatch.setattr('player.CliPlayer.next_move', lambda x, y: 2)

    test_board.state[:, 2] = np.array([2, 1, 2], dtype=np.int8)

    test_board.make_move()

    assert (test_board.state == np.array([[0, 0, 2],
                                          [0, 0, 1],
                                          [0, 0, 2]], dtype=np.int8)).all()


def test_current_player_win_scenario():
    test_board = Board(CliPlayer(1), CliPlayer(2), n_rows=3, n_cols=3, win_length=2)

    test_board.state[:, 0] = np.array([1, 1, 0], dtype=np.int8)

    assert test_board.has_player_won(test_board.state, 1)


def test_when_board_is_full_game_ends_with_no_winner(monkeypatch):
    test_board = Board(CliPlayer(1), CliPlayer(2), n_rows=3, n_cols=3, win_length=2)
    test_board.state = np.ones((3, 3))
    monkeypatch.setattr('player.CliPlayer.next_move', lambda x, y: 2)

    test_board.make_move()

    assert test_board.game_over
    assert not test_board.winner


@pytest.mark.parametrize("arr, last_non_zero", [
    (np.array([2, 1, 0]), 2),
    (np.array([2, 0, 0]), 1),
    (np.array([0, 0, 0]), 0)
])
def test_get_last_zero_index(arr, last_non_zero):
    assert get_next_zero_index(arr) == last_non_zero


@pytest.mark.parametrize("arr, player_value", [
    (np.array([[1, 1, 1],
               [0, 0, 0],
               [0, 0, 0]]), 1),
    (np.array([[1, 0, 0],
               [1, 0, 0],
               [1, 0, 0]]), 1),
    (np.array([[1, 0, 0],
               [0, 1, 0],
               [0, 0, 1]]), 1),
    (np.array([[0, 0, 1],
               [0, 1, 0],
               [1, 0, 0]]), 1),
])
def test_sub_matrix_wins_are_matched(arr, player_value):
    assert check_sub_matrix_for_win(arr, player_value)


@pytest.mark.parametrize("state, player_value", [
    (np.array([[1, 1, 1, 1],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]), 100),
    (np.array([[1, 0, 0, 0],
               [1, 0, 0, 0],
               [0, 0, 0, 0],
               [1, 0, 0, 0]]), 5),
    (np.array([[1, 0, 0, 0],
               [0, 1, 1, 0],
               [0, 1, 1, 0],
               [0, 0, 0, 0]]), 15),
    (np.array([[0, 0, 0, 2],
               [0, 0, 2, 0],
               [0, 2, 0, 0],
               [2, 0, 0, 0]]), -99),
])
def test_evaluate_state_for_player(state, player_value):
    assert evaluate_state_for_player(state, 4, 1) == player_value


if __name__ == "__main__":
    pytest.main()
