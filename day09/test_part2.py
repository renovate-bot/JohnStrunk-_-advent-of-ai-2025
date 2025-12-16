"""Tests for Day 9 Part 2: Movie Theater."""

from pathlib import Path

from day09.part2 import (
    build_green_edges,
    find_largest_valid_rectangle,
    has_red_tile_strictly_inside,
    is_perimeter_valid,
    is_point_inside_polygon,
    is_tile_valid,
    parse_coordinates,
)


def test_parse_coordinates(tmp_path: Path) -> None:
    """Test parsing coordinates from a file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("1,2\n3,4\n5,6\n")

    coords = parse_coordinates(str(test_file))
    assert coords == [(1, 2), (3, 4), (5, 6)]


def test_build_green_edges() -> None:
    """Test building green tiles on edges."""
    # Simple square
    red_tiles = [(0, 0), (2, 0), (2, 2), (0, 2)]
    edges = build_green_edges(red_tiles)

    # Should have edges but not corners
    assert (1, 0) in edges  # Top edge
    assert (2, 1) in edges  # Right edge
    assert (1, 2) in edges  # Bottom edge
    assert (0, 1) in edges  # Left edge

    # Corners should not be in edges (they're red)
    assert (0, 0) not in edges
    assert (2, 0) not in edges
    assert (2, 2) not in edges
    assert (0, 2) not in edges


def test_is_point_inside_polygon() -> None:
    """Test point-in-polygon algorithm."""
    # Simple square from (0,0) to (4,4)
    square = [(0, 0), (4, 0), (4, 4), (0, 4)]

    # Points inside
    assert is_point_inside_polygon((2, 2), square)
    assert is_point_inside_polygon((1, 1), square)
    assert is_point_inside_polygon((3, 3), square)

    # Points outside
    assert not is_point_inside_polygon((5, 5), square)
    assert not is_point_inside_polygon((-1, 2), square)
    assert not is_point_inside_polygon((2, 5), square)


def test_is_tile_valid() -> None:
    """Test tile validation."""
    red_tiles = [(0, 0), (2, 0), (2, 2), (0, 2)]
    red_set = set(red_tiles)
    green_edges = build_green_edges(red_tiles)
    bbox = (0, 2, 0, 2)

    # Red tiles are valid
    assert is_tile_valid((0, 0), red_set, green_edges, red_tiles, bbox)

    # Green edge tiles are valid
    assert is_tile_valid((1, 0), red_set, green_edges, red_tiles, bbox)

    # Interior tiles are valid
    assert is_tile_valid((1, 1), red_set, green_edges, red_tiles, bbox)

    # Outside tiles are invalid
    assert not is_tile_valid((5, 5), red_set, green_edges, red_tiles, bbox)


def test_has_red_tile_strictly_inside() -> None:
    """Test checking for red tiles strictly inside rectangle."""
    red_tiles = [(0, 0), (5, 0), (5, 5), (0, 5), (2, 2)]

    # Rectangle with red tile strictly inside
    assert has_red_tile_strictly_inside((0, 0), (5, 5), red_tiles)

    # Rectangle with red tile on boundary (OK)
    assert not has_red_tile_strictly_inside((0, 0), (5, 0), red_tiles)

    # Rectangle with no red tiles inside
    assert not has_red_tile_strictly_inside((0, 0), (2, 0), red_tiles)


def test_is_perimeter_valid() -> None:
    """Test perimeter validation."""
    red_tiles = [(0, 0), (2, 0), (2, 2), (0, 2)]
    red_set = set(red_tiles)
    green_edges = build_green_edges(red_tiles)
    bbox = (0, 2, 0, 2)

    # Valid rectangle within polygon
    assert is_perimeter_valid((0, 0), (2, 2), red_set, green_edges, red_tiles, bbox)

    # Valid edge rectangle
    assert is_perimeter_valid((0, 0), (2, 0), red_set, green_edges, red_tiles, bbox)

    # Invalid rectangle extending outside
    assert not is_perimeter_valid((0, 0), (5, 5), red_set, green_edges, red_tiles, bbox)


def test_find_largest_valid_rectangle_example() -> None:
    """Test with the example from the puzzle."""
    red_tiles = [
        (7, 1),
        (11, 1),
        (11, 7),
        (9, 7),
        (9, 5),
        (2, 5),
        (2, 3),
        (7, 3),
    ]

    # The largest valid rectangle has area 24
    assert find_largest_valid_rectangle(red_tiles) == 24


def test_find_largest_valid_rectangle_small() -> None:
    """Test with a small simple polygon."""
    # Simple square
    red_tiles = [(0, 0), (3, 0), (3, 3), (0, 3)]

    # The largest rectangle should be the full square: 4x4 = 16
    result = find_largest_valid_rectangle(red_tiles)
    assert result == 16


def test_with_test_input() -> None:
    """Test with the actual test input file."""
    test_file = Path(__file__).parent / "test-input.txt"
    expected_file = Path(__file__).parent / "test-output-part2.txt"

    red_tiles = parse_coordinates(str(test_file))
    result = find_largest_valid_rectangle(red_tiles)

    expected = int(expected_file.read_text().strip())
    assert result == expected
