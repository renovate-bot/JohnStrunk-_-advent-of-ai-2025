"""Tests for Day 9 Part 1: Movie Theater."""

from pathlib import Path

from day09.part1 import (
    calculate_rectangle_area,
    find_largest_rectangle,
    parse_coordinates,
)


def test_calculate_rectangle_area():
    """Test rectangle area calculation with inclusive counting."""
    # Square: (2-0+1) x (2-0+1) = 3 x 3 = 9
    assert calculate_rectangle_area((0, 0), (2, 2)) == 9

    # Rectangle: (4-1+1) x (5-1+1) = 4 x 5 = 20
    assert calculate_rectangle_area((1, 1), (4, 5)) == 20

    # Same point: (0+1) x (0+1) = 1 x 1 = 1
    assert calculate_rectangle_area((5, 5), (5, 5)) == 1

    # Vertical line: (0+1) x (10-1+1) = 1 x 10 = 10
    assert calculate_rectangle_area((3, 1), (3, 10)) == 10

    # Horizontal line: (10-1+1) x (0+1) = 10 x 1 = 10
    assert calculate_rectangle_area((1, 5), (10, 5)) == 10

    # Negative coordinates: (6+1) x (8+1) = 7 x 9 = 63
    assert calculate_rectangle_area((-2, -3), (4, 5)) == 63

    # Order shouldn't matter (absolute values): (5+1) x (5+1) = 36
    assert calculate_rectangle_area((10, 10), (5, 5)) == 36
    assert calculate_rectangle_area((5, 5), (10, 10)) == 36


def test_find_largest_rectangle_example():
    """Test with the example from the puzzle."""
    coordinates = [
        (7, 1),
        (11, 1),
        (11, 7),
        (9, 7),
        (9, 5),
        (2, 5),
        (2, 3),
        (7, 3),
    ]

    # The largest rectangle has area 50 (between 2,5 and 11,1)
    # Width = (11-2+1) = 10, Height = (5-1+1) = 5, Area = 50
    assert find_largest_rectangle(coordinates) == 50


def test_find_largest_rectangle_small():
    """Test with a small set of coordinates."""
    # Two points that are 3 apart horizontally and 4 apart vertically
    # Inclusive: (3+1) * (4+1) = 4*5 = 20
    coordinates = [(0, 0), (3, 4)]
    assert find_largest_rectangle(coordinates) == 20


def test_find_largest_rectangle_same_points():
    """Test with identical points (zero area)."""
    coordinates = [(5, 5), (5, 5)]
    assert find_largest_rectangle(coordinates) == 1  # Inclusive: 1*1


def test_find_largest_rectangle_collinear():
    """Test with points on the same horizontal line."""
    coordinates = [(1, 5), (3, 5), (7, 5)]
    # Largest is between (1,5) and (7,5): (7-1+1) * (5-5+1) = 7*1 = 7
    assert find_largest_rectangle(coordinates) == 7


def test_parse_coordinates(tmp_path: Path) -> None:
    """Test parsing coordinates from a file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("1,2\n3,4\n5,6\n")

    coords = parse_coordinates(str(test_file))
    assert coords == [(1, 2), (3, 4), (5, 6)]


def test_parse_coordinates_with_empty_lines(tmp_path: Path) -> None:
    """Test parsing with empty lines."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("1,2\n\n3,4\n\n\n")

    coords = parse_coordinates(str(test_file))
    assert coords == [(1, 2), (3, 4)]


def test_with_test_input():
    """Test with the actual test input file."""
    test_file = Path(__file__).parent / "test-input.txt"
    expected_file = Path(__file__).parent / "test-output.txt"

    coordinates = parse_coordinates(str(test_file))
    result = find_largest_rectangle(coordinates)

    expected = int(expected_file.read_text().strip())
    assert result == expected
