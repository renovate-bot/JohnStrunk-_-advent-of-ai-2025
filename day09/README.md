# Day 9: Movie Theater

## Part 1: Finding the Largest Rectangle

### Problem Summary

Given a grid of tiles where some are red (marked by coordinates), find the
largest rectangle that can be formed using any two red tiles as opposite
corners.

### Approach

The solution uses a brute-force approach:

1. **Parse Input**: Read all red tile coordinates from the input file.

2. **Calculate Rectangle Areas**: For each pair of tiles, calculate the area
   of the rectangle formed when those two tiles are opposite corners.

3. **Find Maximum**: Track and return the maximum area found.

### Key Insight: Inclusive Counting

The critical insight from the puzzle examples is that tiles are discrete grid
positions, and rectangles count tiles **inclusively**. This means:

- A rectangle from position (2,5) to (11,1) includes all positions from x=2
  to x=11 (10 tiles) and y=1 to y=5 (5 tiles)
- The formula is: `area = (|x2 - x1| + 1) x (|y2 - y1| + 1)`

Examples from the puzzle:

- Between (2,5) and (9,7): (9-2+1) x (7-5+1) = 8 x 3 = **24**
- Between (7,1) and (11,7): (11-7+1) x (7-1+1) = 5 x 7 = **35**
- Between (7,3) and (2,3): (7-2+1) x (3-3+1) = 6 x 1 = **6**
- Between (2,5) and (11,1): (11-2+1) x (5-1+1) = 10 x 5 = **50** (largest)

### Algorithm Complexity

- **Time Complexity**: O(n²) where n is the number of red tiles, since we
  check all pairs.
- **Space Complexity**: O(n) to store the coordinates.

For the input size (496 coordinates), this results in about 122,760
comparisons, which is easily manageable.

### Implementation Details

The solution is organized into three main functions:

1. `parse_coordinates(filename)`: Reads and parses coordinate pairs from the
   input file.
2. `calculate_rectangle_area(p1, p2)`: Calculates the inclusive area between
   two points.
3. `find_largest_rectangle(coordinates)`: Iterates through all pairs to find
   the maximum area.

### Running the Solution

```bash
uv run day09/part1.py day09/input.txt
```

### Testing

Tests cover:

- Rectangle area calculation with various coordinate configurations
- The example from the puzzle description
- Edge cases (same points, collinear points, negative coordinates)
- Parsing with empty lines

Run tests with:

```bash
uv run pytest day09/test_part1.py -v
```
