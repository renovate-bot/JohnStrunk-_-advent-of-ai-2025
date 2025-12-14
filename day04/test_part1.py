"""Test for day04 part1 solution."""

from day04.part1 import count_accessible_rolls


def test_accessible_rolls_sample():
    """Test the sample grid from the puzzle description."""
    sample = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@.",
    ]
    assert count_accessible_rolls(sample) == 13
