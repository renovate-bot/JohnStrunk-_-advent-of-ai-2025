#!/usr/bin/env python3
"""Day 9 Part 1: Movie Theater - Find largest rectangle from red tile corners."""

import sys


def parse_coordinates(filename: str) -> list[tuple[int, int]]:
    """Parse coordinate pairs from input file."""
    coordinates = []
    with open(filename) as f:
        for raw_line in f:
            line = raw_line.strip()
            if line:
                x, y = map(int, line.split(","))
                coordinates.append((x, y))
    return coordinates


def calculate_rectangle_area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """Calculate area of rectangle with opposite corners at p1 and p2.

    Tiles are discrete grid positions, so we count inclusively.
    """
    x1, y1 = p1
    x2, y2 = p2
    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    return width * height


def find_largest_rectangle(coordinates: list[tuple[int, int]]) -> int:
    """Find the largest rectangle area using any two tiles as opposite corners."""
    max_area = 0
    n = len(coordinates)

    for i in range(n):
        for j in range(i + 1, n):
            area = calculate_rectangle_area(coordinates[i], coordinates[j])
            max_area = max(max_area, area)

    return max_area


def main() -> None:
    """Read input and find the largest rectangle area."""
    if len(sys.argv) != 2:  # noqa: PLR2004
        print("Usage: python part1.py <input_file>", file=sys.stderr)
        sys.exit(1)

    coordinates = parse_coordinates(sys.argv[1])
    result = find_largest_rectangle(coordinates)
    print(result)


if __name__ == "__main__":
    main()
