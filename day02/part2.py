"""Day 2 Part 2 solution.

Puzzle: See puzzle-part2.txt for description
Input: input.txt
"""

import os
import sys

MIN_REPEAT = 2


def is_invalid_id(id_str: int) -> bool:
    """
    Check if an ID is invalid by determining if it consists of a repeated sequence of digits.

    An ID is invalid if it is made only of some sequence of digits repeated at least twice.
    For example: 12341234 (1234 two times), 123123123 (123 three times), etc.

    Args:
        id_str (int): The ID to check.

    Returns:
        bool: True if the ID is invalid, False otherwise.
    """
    s = str(id_str)
    n = len(s)
    for sublen in range(1, n // 2 + 1):
        if n % sublen == 0:
            # Must be repeated at least MIN_REPEAT times
            if n // sublen < MIN_REPEAT:
                continue
            seq = s[:sublen]
            if seq * (n // sublen) == s:
                return True
    return False


def count_invalid_ids_in_range(start: int, end: int) -> int:
    """
    Count and sum all invalid IDs in a given range.

    Args:
        start (int): Start of the range (inclusive).
        end (int): End of the range (inclusive).

    Returns:
        int: The sum of all invalid IDs in the range.
    """
    count = 0
    for i in range(start, end + 1):
        if is_invalid_id(i):
            count += i
    return count


def main() -> None:
    """
    Process input, sum invalid IDs, and print the result.

    Accepts input file as a command-line argument, defaults to input.txt in the same directory.
    """
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(input_path) as f:
        ranges = f.read().strip().split(",")
    total = 0
    for r in ranges:
        if "-" in r:
            start, end = map(int, r.split("-"))
            total += count_invalid_ids_in_range(start, end)
        else:
            val = int(r)
            if is_invalid_id(val):
                total += val
    print(total)


if __name__ == "__main__":
    main()
