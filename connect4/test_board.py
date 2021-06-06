from board import Board, get_next_zero_index, check_sub_matrix_for_win
import numpy as np
import pytest


def test_create_board_using_defaults():
    test_board = Board()
    assert (test_board.state == np.zeros((5, 7), dtype=np.int8)).all()
    assert test_board.next_player == 2


def test_create_custom_board():
    test_board = Board(9, 9)
    assert (test_board.state == np.zeros((9, 9), dtype=np.int8)).all()
    assert test_board.next_player == 2


def test_is_drop_valid():
    test_board = Board(2, 2)

    assert test_board._is_valid_drop(0)

    test_board.state[0] = 1
    assert test_board._is_valid_drop(0)

    test_board.state[:, 0] = 1
    assert test_board._is_valid_drop(1)
    assert not test_board._is_valid_drop(0)

    test_board.state = np.ones((2, 2))
    assert not test_board._is_valid_drop(0)


def test_make_move():
    test_board = Board(3, 3, 3)

    test_board.state[:, 1] = np.array([1, 0, 0], dtype=np.int8)
    test_board.state[:, 2] = np.array([2, 1, 0], dtype=np.int8)

    test_board.make_move(col=1)
    test_board.make_move(col=2)

    assert (test_board.state == np.array([[0, 1, 2],
                                          [0, 1, 1],
                                          [0, 0, 2]], dtype=np.int8)).all()


def test_current_player_win_scenario():
    test_board = Board(3, 3, 2)

    test_board.state[:, 0] = np.array([1, 1, 0], dtype=np.int8)

    assert test_board.has_current_player_won()


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


if __name__ == "__main__":
    pytest.main()
