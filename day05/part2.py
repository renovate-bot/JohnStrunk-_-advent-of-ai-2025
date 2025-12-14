"""
Day 5 - Part 2 Solution.

Counts the number of unique ingredient IDs considered fresh by any of the given ranges.
"""


def parse_ranges(filename):
    """Parse ranges from the input file."""
    ranges = []
    with open(filename) as f:
        for file_line in f:
            line = file_line.strip()
            if not line:
                continue
            if "-" in line:
                start, end = map(int, line.split("-"))
                ranges.append((start, end))
    return ranges


def merge_ranges(ranges):
    """Merge overlapping or adjacent ranges."""
    # Sort ranges by start
    ranges.sort()
    merged = []
    for start, end in ranges:
        if not merged or start > merged[-1][1] + 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def count_fresh_ids(ranges):
    """Count the total number of unique fresh ingredient IDs."""
    merged = merge_ranges(ranges)
    return sum(end - start + 1 for start, end in merged)


if __name__ == "__main__":
    import sys

    MIN_ARGS = 2
    if len(sys.argv) < MIN_ARGS:
        print("Usage: uv run day05/part2.py <input_file>")
        sys.exit(1)
    filename = sys.argv[1]
    ranges = parse_ranges(filename)
    print(count_fresh_ids(ranges))
