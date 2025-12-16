"""
Solution for Day 10, Part 2.

This module contains the solution for Part 2 of Day 10.
"""

from fractions import Fraction
from itertools import product
from typing import NamedTuple


def parse_input(input_data: str) -> list[tuple[list[int], list[tuple[int, ...]]]]:
    """
    Parse the input data into a list of machines.

    Args:
        input_data (str): The raw input data.

    Returns:
        list: A list of tuples, each containing the target joltage levels and button wiring.
    """
    machines: list[tuple[list[int], list[tuple[int, ...]]]] = []
    for line in input_data.strip().split("\n"):
        parts = line.split()
        # Extract joltage requirements (last item in {curly braces})
        joltage_str = next(p for p in reversed(parts) if p.startswith("{"))
        joltage = list(map(int, joltage_str[1:-1].split(",")))
        # Extract button wiring schematics
        buttons = [
            tuple(map(int, b[1:-1].split(","))) for b in parts if b.startswith("(")
        ]
        machines.append((joltage, buttons))
    return machines


class GaussianSolution(NamedTuple):
    """Result of Gaussian elimination."""

    A_: list[list[Fraction]]
    b_: list[Fraction]
    where: list[int]
    rank: int


def gaussian_elimination(
    A: list[list[Fraction]], b: list[Fraction]
) -> GaussianSolution | None:
    """
    Perform Gaussian elimination on the augmented matrix [A|b].

    Args:
        A: Coefficient matrix (n x m)
        b: Target vector (length n)

    Returns:
        GaussianSolution if solvable, None if inconsistent
    """
    n = len(A)  # number of equations
    m = len(A[0]) if A else 0  # number of variables

    # Create copies for row reduction
    A_ = [row[:] for row in A]
    b_ = b[:]

    # Track which column (variable) corresponds to which pivot row
    where = [-1] * m
    rank = 0

    for cidx in range(m):
        # Find pivot
        pivot_row = -1
        for ridx in range(rank, n):
            if A_[ridx][cidx] != 0:
                pivot_row = ridx
                break

        if pivot_row == -1:
            continue

        # Swap pivot row to current rank position
        A_[rank], A_[pivot_row] = A_[pivot_row], A_[rank]
        b_[rank], b_[pivot_row] = b_[pivot_row], b_[rank]
        where[cidx] = rank

        # Scale pivot row
        pivot = A_[rank][cidx]
        for j in range(m):
            A_[rank][j] /= pivot
        b_[rank] /= pivot

        # Eliminate column in other rows
        for ridx in range(n):
            if ridx == rank:
                continue
            factor = A_[ridx][cidx]
            if factor == 0:
                continue
            for j in range(m):
                A_[ridx][j] -= factor * A_[rank][j]
            b_[ridx] -= factor * b_[rank]

        rank += 1

    # Check for inconsistency (0 = non-zero)
    for ridx in range(rank, n):
        if b_[ridx] != 0:
            return None

    return GaussianSolution(A_, b_, where, rank)


def min_button_presses(target: list[int], buttons: list[tuple[int, ...]]) -> int:
    """
    Find minimum button presses to reach target joltage levels.

    Args:
        target: Target joltage levels for each counter
        buttons: List of button wirings (which counters each button affects)

    Returns:
        Minimum number of button presses, or -1 if unsolvable
    """
    n = len(target)  # number of counters
    m = len(buttons)  # number of buttons

    # Build coefficient matrix A (n x m)
    # A[i][j] = 1 if button j affects counter i, else 0
    A: list[list[Fraction]] = [[Fraction(0)] * m for _ in range(n)]
    for j, button in enumerate(buttons):
        for i in button:
            A[i][j] = Fraction(1)

    b = [Fraction(t) for t in target]

    # Solve using Gaussian elimination
    solution = gaussian_elimination(A, b)
    if solution is None:
        return -1

    # Find free variables (columns without pivots)
    free_vars = [i for i in range(m) if solution.where[i] == -1]

    # Try all combinations of free variables to find minimum with all non-negative values
    min_presses = None

    # Determine search range for free variables
    # Start with a reasonable upper bound based on max target value
    max_target = max(target) if target else 0
    search_range = max_target + 1

    for free_values in product(range(search_range), repeat=len(free_vars)):
        # Construct solution vector x
        x = [Fraction(0)] * m
        for idx, val in zip(free_vars, free_values):
            x[idx] = Fraction(val)

        # Back-substitute to find dependent variables
        valid = True
        for i in range(m):
            if solution.where[i] == -1:
                continue
            row = solution.where[i]
            val = solution.b_[row]
            for j in range(m):
                if j != i:
                    val -= solution.A_[row][j] * x[j]
            # Check if solution is non-negative integer
            if val < 0 or val.denominator != 1:
                valid = False
                break
            x[i] = val

        if not valid:
            continue

        # Calculate total presses
        total = sum(int(v) for v in x)
        if min_presses is None or total < min_presses:
            min_presses = total

    return min_presses if min_presses is not None else -1


def solve(input_data: str) -> int:
    """
    Solve the Day 10, Part 2 puzzle for all machines in the input.

    Args:
        input_data (str): The raw input data for all machines.

    Returns:
        int: The total minimum number of button presses for all machines, or -1 if any is unsolvable.
    """
    machines = parse_input(input_data)
    total_presses: int = 0
    for joltage, buttons in machines:
        presses = min_button_presses(joltage, buttons)
        if presses == -1:
            return -1
        total_presses += presses
    return total_presses


if __name__ == "__main__":
    with open("input.txt") as f:
        input_data = f.read()
    print(solve(input_data))
