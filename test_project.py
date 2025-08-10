import math
import pytest
from project import calculate_trajectory, check_score, HOOP_MIN_X, HOOP_MAX_X

def test_calculate_trajectory_length():
    traj = calculate_trajectory(45, 20)
    assert len(traj) > 0
    assert abs(traj[0][0] - 0) < 0.1
    assert abs(traj[0][1] - 14) < 0.1

def test_calculate_trajectory_bounds():
    traj = calculate_trajectory(30, 15)
    for x, y in traj:
        assert 0 <= x <= 39
        assert 0 <= y <= 14

def test_check_score_true():
    hoop_x = 25
    positions = [(hoop_x, 5), (hoop_x + 1, 5), (hoop_x + 2, 5)]
    assert check_score(positions, hoop_x) is True

def test_check_score_false():
    hoop_x = 25
    positions = [(hoop_x - 1, 5), (hoop_x + 3, 5), (hoop_x, 6)]
    assert check_score(positions, hoop_x) is False

def test_hoop_position_limits():
    assert HOOP_MIN_X >= 0
    assert HOOP_MAX_X < 40
    assert HOOP_MAX_X > HOOP_MIN_X
