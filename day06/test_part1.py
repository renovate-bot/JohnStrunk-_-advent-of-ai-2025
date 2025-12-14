"""Tests for day06 part1.py."""

from part1 import solve


def test_example():
    """Test the example from the puzzle description."""
    input_lines = [
        "123 328  51 64 ",
        " 45 64  387 23 ",
        "  6 98  215 314",
        "*   +   *   +  ",
    ]
    assert solve(input_lines) == 4277556


def test_real_input():
    """Test the real input for regression safety."""
    with open("input.txt") as f:
        input_lines = f.read().splitlines()
    result = solve(input_lines)
    assert result == 5381996914800
