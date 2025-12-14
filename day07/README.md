
# Day 7: Laboratories (Part 1)

## Problem Summary

Given a grid representing a tachyon manifold, a beam enters at 'S' and moves
downward. It passes through '.' and splits at '^' into left and right beams.
Count the total number of splits until all beams exit or are stopped.

## Approach

- Parse the grid and locate 'S'.
- Simulate the downward beam, splitting at '^' into left/right beams.
- Track visited positions to avoid infinite loops.
- Count each split event.

## Challenges

- Ensuring beams do not split infinitely or revisit the same cell.
- Handling edge cases at grid boundaries.

## Testing

- Verified with the sample from the puzzle (21 splits).
- Main input is tested via part1.py and pytest.

## Usage

Run the solution:

```sh
uv run day07/part1.py
```

Run tests:

```sh
uv run -m pytest day07/test_part1.py
```
