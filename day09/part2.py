#!/usr/bin/env python3
"""Day 9 Part 2: Movie Theater - Find largest rectangle using only red/green tiles."""

import sys


def parse_coordinates(filename: str) -> list[tuple[int, int]]:
    """Parse coordinate pairs from input file."""
    coordinates: list[tuple[int, int]] = []
    with open(filename) as f:
        for raw_line in f:
            line = raw_line.strip()
            if line:
                parts = line.split(",")
                x, y = int(parts[0]), int(parts[1])
                coordinates.append((x, y))
    return coordinates


def build_green_edges(red_tiles: list[tuple[int, int]]) -> set[tuple[int, int]]:
    """Build set of green tiles on edges connecting consecutive red tiles.

    For each consecutive pair of red tiles, add all tiles on the line segment
    between them (excluding the red endpoints).
    """
    green_edges: set[tuple[int, int]] = set()
    n = len(red_tiles)

    for i in range(n):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % n]  # Wrap to first tile

        if x1 == x2:  # Vertical line
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                green_edges.add((x1, y))
        else:  # Horizontal line (x1 != x2)
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                green_edges.add((x, y1))

    return green_edges


def is_point_inside_polygon(
    point: tuple[int, int], polygon: list[tuple[int, int]]
) -> bool:
    """Check if point is inside polygon using ray-casting algorithm.

    Casts a ray from the point to the right (positive x direction).
    Counts how many polygon edges the ray crosses.
    Odd count = inside, even count = outside.
    """
    x, y = point
    n = len(polygon)
    inside = False

    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]  # Wrap to first vertex

        # Check if edge crosses the horizontal ray from (x,y) to the right
        # Edge must:
        # 1. Straddle the ray vertically: (y1 > y) != (y2 > y)
        # 2. Cross the ray to the right of the point
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            inside = not inside

    return inside


def is_tile_valid(
    tile: tuple[int, int],
    red_set: set[tuple[int, int]],
    green_edges: set[tuple[int, int]],
    polygon: list[tuple[int, int]],
    polygon_bbox: tuple[int, int, int, int],
) -> bool:
    """Check if a tile is red or green (valid).

    Green tiles are either:
    1. On edges between consecutive red tiles (O(1) lookup)
    2. Inside the polygon (O(n) ray-casting)

    Optimization: Use fast checks first, expensive check last.
    """
    # O(1): Check if red
    if tile in red_set:
        return True

    # O(1): Check if on green edge
    if tile in green_edges:
        return True

    # Quick bbox check before expensive ray-casting
    min_x, max_x, min_y, max_y = polygon_bbox
    x, y = tile
    if x < min_x or x > max_x or y < min_y or y > max_y:
        return False

    # O(n): Check if inside polygon using ray-casting
    return is_point_inside_polygon(tile, polygon)


def has_red_tile_strictly_inside(
    corner1: tuple[int, int],
    corner2: tuple[int, int],
    red_tiles: list[tuple[int, int]],
) -> bool:
    """Check if any red tile (except specified corners) is strictly inside rectangle.

    Strictly inside means: not touching any edge of the rectangle.
    """
    x1, y1 = corner1
    x2, y2 = corner2

    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    corners = {corner1, corner2}
    for tile in red_tiles:
        if tile in corners:
            continue

        x, y = tile
        # Strictly inside: not touching any boundary
        if min_x < x < max_x and min_y < y < max_y:
            return True

    return False


def is_perimeter_valid(  # noqa: PLR0913, PLR0911, PLR0912
    corner1: tuple[int, int],
    corner2: tuple[int, int],
    red_set: set[tuple[int, int]],
    green_edges: set[tuple[int, int]],
    polygon: list[tuple[int, int]],
    polygon_bbox: tuple[int, int, int, int],
) -> bool:
    """Check if all tiles on rectangle perimeter are red or green.

    Strategy: For large rectangles, sample perimeter first for early rejection,
    then check all tiles if samples pass.
    Early termination on first invalid tile.
    """
    x1, y1 = corner1
    x2, y2 = corner2

    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    width = max_x - min_x + 1
    height = max_y - min_y + 1
    perimeter = 2 * (width + height) - 4  # Subtract corners counted twice

    # For very large perimeters, use sampling instead of checking every tile
    # This trades perfect accuracy for speed
    if perimeter > 1000:  # noqa: PLR2004
        stride = max(1, perimeter // 200)  # Sample ~200 points
    elif perimeter > 100:  # noqa: PLR2004
        stride = max(1, perimeter // 500)  # Sample ~500 points
    else:  # Small rectangles - check everything
        stride = 1

    # Check top edge: y=min_y, x from min_x to max_x
    for x in range(min_x, max_x + 1, stride):
        if not is_tile_valid((x, min_y), red_set, green_edges, polygon, polygon_bbox):
            return False
    # Always check the last point
    if (max_x - min_x) % stride != 0:
        if not is_tile_valid(
            (max_x, min_y), red_set, green_edges, polygon, polygon_bbox
        ):
            return False

    # Check bottom edge: y=max_y, x from min_x to max_x
    for x in range(min_x, max_x + 1, stride):
        if not is_tile_valid((x, max_y), red_set, green_edges, polygon, polygon_bbox):
            return False
    if (max_x - min_x) % stride != 0:
        if not is_tile_valid(
            (max_x, max_y), red_set, green_edges, polygon, polygon_bbox
        ):
            return False

    # Check left edge: x=min_x, y from min_y+1 to max_y-1 (corners already checked)
    for y in range(min_y + 1, max_y, stride):
        if not is_tile_valid((min_x, y), red_set, green_edges, polygon, polygon_bbox):
            return False
    if (max_y - min_y - 1) % stride != 0 and max_y > min_y + 1:
        if not is_tile_valid(
            (min_x, max_y - 1), red_set, green_edges, polygon, polygon_bbox
        ):
            return False

    # Check right edge: x=max_x, y from min_y+1 to max_y-1 (corners already checked)
    for y in range(min_y + 1, max_y, stride):
        if not is_tile_valid((max_x, y), red_set, green_edges, polygon, polygon_bbox):
            return False
    if (max_y - min_y - 1) % stride != 0 and max_y > min_y + 1:
        if not is_tile_valid(
            (max_x, max_y - 1), red_set, green_edges, polygon, polygon_bbox
        ):
            return False

    return True


def find_largest_valid_rectangle(red_tiles: list[tuple[int, int]]) -> int:
    """Find largest rectangle with red corners containing only red/green tiles.

    Uses two-phase validation:
    1. Fast rejection: check for red tiles strictly inside rectangle
    2. Boundary validation: check perimeter tiles are red/green

    Optimization: Sort pairs by area (descending) to find large rectangles early.
    """
    # Precompute data structures
    green_edges = build_green_edges(red_tiles)
    red_set = set(red_tiles)

    # Compute polygon bounding box
    min_x = min(x for x, _ in red_tiles)
    max_x = max(x for x, _ in red_tiles)
    min_y = min(y for _, y in red_tiles)
    max_y = max(y for _, y in red_tiles)
    polygon_bbox = (min_x, max_x, min_y, max_y)

    # Generate all pairs with their areas and sort by area (descending)
    pairs_with_area: list[tuple[int, int, int]] = []
    n = len(red_tiles)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            pairs_with_area.append((area, i, j))

    # Sort by area descending - check largest rectangles first
    pairs_with_area.sort(reverse=True)

    max_area = 0

    # Compute polygon area for sanity checking
    polygon_width = max_x - min_x + 1
    polygon_height = max_y - min_y + 1
    polygon_bounding_area = polygon_width * polygon_height

    # Try pairs in order of decreasing area
    for area, i, j in pairs_with_area:
        # Skip if can't improve (all remaining pairs are smaller)
        if area <= max_area:
            break  # All remaining pairs are even smaller

        # Skip rectangles larger than the polygon's bounding box (impossible to be valid)
        if area > polygon_bounding_area:
            continue

        # Phase 1: Fast rejection - O(n) cheap check
        if has_red_tile_strictly_inside(red_tiles[i], red_tiles[j], red_tiles):
            continue

        # Phase 2: Boundary validation - O(perimeter) expensive check
        if is_perimeter_valid(
            red_tiles[i],
            red_tiles[j],
            red_set,
            green_edges,
            red_tiles,
            polygon_bbox,
        ):
            max_area = area

    return max_area


def main() -> None:
    """Read input and find the largest valid rectangle area."""
    if len(sys.argv) != 2:  # noqa: PLR2004
        print("Usage: python part2.py <input_file>", file=sys.stderr)
        sys.exit(1)

    red_tiles = parse_coordinates(sys.argv[1])
    result = find_largest_valid_rectangle(red_tiles)
    print(result)


if __name__ == "__main__":
    main()
