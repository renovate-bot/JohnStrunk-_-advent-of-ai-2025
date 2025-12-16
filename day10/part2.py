"""
Solution for Day 10, Part 2.

This module contains the solution for Part 2 of Day 10.
"""

import random
from fractions import Fraction
from itertools import product
from typing import NamedTuple

# Constants for optimization
MAX_EXHAUSTIVE_FREE_VARS = 3
MAX_HEURISTIC_COMBINATIONS = 50000
MAX_HEURISTIC_SEARCH_RANGE = 100
MAX_FREE_VAR_DIVISOR = 300
TWO_FREE_VARS = 2
THREE_FREE_VARS = 3
SEARCH_BOUND_TWO_VARS = 300
SEARCH_BOUND_THREE_VARS = 100
SEARCH_BOUND_MANY_VARS = 500


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


def _solve_unique_system(solution: GaussianSolution, m: int) -> int:
    """Solve system with unique solution (no free variables)."""
    x = [Fraction(0)] * m
    for i in range(m):
        if solution.where[i] == -1:
            continue
        row = solution.where[i]
        val = solution.b_[row]
        for j in range(m):
            if j != i:
                val -= solution.A_[row][j] * x[j]
        if val < 0 or val.denominator != 1:
            return -1
        x[i] = val
    return int(sum(x))


def _try_free_variable_assignment(
    free_values: tuple[int, ...],
    free_vars: list[int],
    solution: GaussianSolution,
    m: int,
) -> int | None:
    """Try a specific assignment of free variables and return total presses if valid."""
    x = [Fraction(0)] * m
    for idx, val in zip(free_vars, free_values):
        x[idx] = Fraction(val)

    for i in range(m):
        if solution.where[i] == -1:
            continue
        row = solution.where[i]
        val = solution.b_[row]
        for j in range(m):
            if j != i:
                val -= solution.A_[row][j] * x[j]
        if val < 0 or val.denominator != 1:
            return None
        x[i] = val

    return int(sum(x))


def _exhaustive_search(
    free_vars: list[int],
    solution: GaussianSolution,
    m: int,
    search_range: int,
) -> int | None:
    """Perform exhaustive search over free variable space."""
    min_presses = None
    for free_values in product(range(search_range), repeat=len(free_vars)):
        result = _try_free_variable_assignment(free_values, free_vars, solution, m)
        if result is not None and (min_presses is None or result < min_presses):
            min_presses = result
    return min_presses


def _heuristic_search(
    free_vars: list[int],
    solution: GaussianSolution,
    m: int,
    max_search: int,
) -> int | None:
    """Perform heuristic random search over free variable space."""
    random.seed(42)
    tried = {tuple([0] * len(free_vars))}
    min_presses = None
    attempts = 0

    while attempts < MAX_HEURISTIC_COMBINATIONS:
        free_values = tuple(
            random.randint(0, min(MAX_HEURISTIC_SEARCH_RANGE, max_search))
            for _ in free_vars
        )
        if free_values in tried:
            continue
        tried.add(free_values)
        attempts += 1

        result = _try_free_variable_assignment(free_values, free_vars, solution, m)
        if result is not None and (min_presses is None or result < min_presses):
            min_presses = result

    return min_presses


def _calculate_search_bound(
    solution: GaussianSolution, free_vars: list[int], m: int, target: list[int]
) -> int:
    """Calculate a smart upper bound for free variable search based on basic solution."""
    # Get basic solution to see how far off we are
    x_basic = [Fraction(0)] * m
    for i in range(m):
        if solution.where[i] == -1:
            continue
        row = solution.where[i]
        val = solution.b_[row]
        for j in range(m):
            if j != i:
                val -= solution.A_[row][j] * x_basic[j]
        x_basic[i] = val

    # Find the most negative value (how much we need to compensate)
    min_val = min((v for v in x_basic if v < 0), default=Fraction(0))

    # Upper bound is based on:
    # 1. How much we need to add to make negatives positive
    # 2. The maximum target value
    max_target = max(target) if target else 0
    compensation_needed = abs(int(min_val)) if min_val < 0 else 0

    # Use the max of compensation needed and target-based estimate
    return max(compensation_needed + 50, max_target // max(len(free_vars), 1) + 50)


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

    if not free_vars:
        return _solve_unique_system(solution, m)

    # Try basic solution with all free variables = 0
    basic = _try_free_variable_assignment(
        tuple([0] * len(free_vars)), free_vars, solution, m
    )
    min_presses = basic

    # Calculate smart search bound
    search_bound = _calculate_search_bound(solution, free_vars, m, target)
    # Cap at 100 for 3 free vars (1M combinations), lower for more
    if len(free_vars) == THREE_FREE_VARS:
        search_bound = min(search_bound, SEARCH_BOUND_THREE_VARS)
    elif len(free_vars) == TWO_FREE_VARS:
        search_bound = min(search_bound, SEARCH_BOUND_TWO_VARS)
    else:
        search_bound = min(search_bound, SEARCH_BOUND_MANY_VARS)

    if len(free_vars) <= MAX_EXHAUSTIVE_FREE_VARS:
        # Exhaustive search for small number of free variables
        result = _exhaustive_search(free_vars, solution, m, search_bound)
        if result is not None and (min_presses is None or result < min_presses):
            min_presses = result
    else:
        # Heuristic search for many free variables
        result = _heuristic_search(free_vars, solution, m, search_bound)
        if result is not None and (min_presses is None or result < min_presses):
            min_presses = result

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
