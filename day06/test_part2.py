"""Tests for day06 part2.py."""

from day06.part2 import solve


def test_example():
    """Test the example from the part 2 description."""
    input_lines = [
        "123 328  51 64 ",
        " 45 64  387 23 ",
        "  6 98  215 314",
        "*   +   *   +  ",
    ]
    assert solve(input_lines) == 3263827


def test_real_input():
    """Test the real input for regression safety."""
    with open("day06/input.txt") as f:
        input_lines = f.read().splitlines()
    result = solve(input_lines)
    assert result == 9627174150897
